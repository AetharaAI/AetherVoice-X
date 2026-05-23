from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
import stripe

from aether_common.postgres import PostgresPool
from aether_common.settings import Settings


ACTIVE_SUBSCRIPTION_STATUSES = {"active", "trialing"}
ACTIVE_ENTITLEMENT_STATUSES = {"active", "trial"}
PAID_PLAN_STATUSES = {"active", "founder"}


@dataclass
class EntitlementSnapshot:
    install_id: str
    entitlement_status: str
    plan_slug: str | None
    free_seconds_granted: int
    free_seconds_used: int
    free_seconds_remaining: int
    can_transcribe: bool
    checkout_pending: bool

    def to_payload(self, session_token: str | None = None) -> dict[str, Any]:
        return {
            "install_id": self.install_id,
            "session_token": session_token,
            "entitlement_status": self.entitlement_status,
            "plan_slug": self.plan_slug,
            "free_seconds_granted": self.free_seconds_granted,
            "free_seconds_used": self.free_seconds_used,
            "free_seconds_remaining": self.free_seconds_remaining,
            "can_transcribe": self.can_transcribe,
            "checkout_pending": self.checkout_pending,
        }


class ScriberService:
    def __init__(self, db: PostgresPool, settings: Settings) -> None:
        self.db = db
        self.settings = settings
        if settings.scriber_stripe_secret_key:
            stripe.api_key = settings.scriber_stripe_secret_key

    async def ensure_schema(self) -> None:
        statements = [
            """
            CREATE TABLE IF NOT EXISTS scriber_installs (
              install_id TEXT PRIMARY KEY,
              first_seen_app_version TEXT,
              last_seen_app_version TEXT,
              platform TEXT NOT NULL DEFAULT 'linux',
              email TEXT,
              stripe_customer_id TEXT,
              last_checkout_session_id TEXT,
              free_seconds_granted INT NOT NULL DEFAULT 1800,
              created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
              updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
              last_seen_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scriber_entitlements (
              install_id TEXT PRIMARY KEY REFERENCES scriber_installs(install_id) ON DELETE CASCADE,
              plan_slug TEXT NOT NULL,
              status TEXT NOT NULL,
              stripe_customer_id TEXT,
              stripe_subscription_id TEXT,
              stripe_checkout_session_id TEXT,
              cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
              current_period_end TIMESTAMPTZ,
              created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
              updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scriber_checkout_sessions (
              checkout_session_id TEXT PRIMARY KEY,
              install_id TEXT NOT NULL REFERENCES scriber_installs(install_id) ON DELETE CASCADE,
              plan_slug TEXT NOT NULL,
              status TEXT NOT NULL DEFAULT 'open',
              checkout_url TEXT,
              created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
              updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
              completed_at TIMESTAMPTZ
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scriber_usage_ledger (
              ledger_id TEXT PRIMARY KEY,
              install_id TEXT NOT NULL REFERENCES scriber_installs(install_id) ON DELETE CASCADE,
              session_id TEXT,
              metric TEXT NOT NULL,
              quantity_seconds INT NOT NULL,
              source TEXT NOT NULL DEFAULT 'gateway',
              created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """,
        ]
        for statement in statements:
            await self.db.execute(statement)

    async def touch_install(self, install_id: str, *, app_version: str | None, platform: str | None) -> None:
        now = datetime.now(UTC)
        await self.db.execute(
            """
            INSERT INTO scriber_installs (
              install_id, first_seen_app_version, last_seen_app_version, platform, free_seconds_granted, created_at, updated_at, last_seen_at
            ) VALUES (
              %(install_id)s, %(app_version)s, %(app_version)s, %(platform)s, %(free_seconds_granted)s, %(now)s, %(now)s, %(now)s
            )
            ON CONFLICT (install_id) DO UPDATE SET
              last_seen_app_version = COALESCE(EXCLUDED.last_seen_app_version, scriber_installs.last_seen_app_version),
              platform = COALESCE(EXCLUDED.platform, scriber_installs.platform),
              updated_at = %(now)s,
              last_seen_at = %(now)s
            """,
            {
                "install_id": install_id,
                "app_version": app_version,
                "platform": platform or "linux",
                "free_seconds_granted": self.settings.scriber_free_minutes * 60,
                "now": now,
            },
        )

    async def get_snapshot(self, install_id: str) -> EntitlementSnapshot:
        install = await self.db.fetch_one(
            """
            SELECT install_id, free_seconds_granted
            FROM scriber_installs
            WHERE install_id = %(install_id)s
            """,
            {"install_id": install_id},
        )
        if install is None:
            raise ValueError(f"Unknown install_id: {install_id}")

        usage = await self.db.fetch_one(
            """
            SELECT COALESCE(SUM(quantity_seconds), 0) AS used_seconds
            FROM scriber_usage_ledger
            WHERE install_id = %(install_id)s AND metric = 'asr_audio_seconds'
            """,
            {"install_id": install_id},
        ) or {"used_seconds": 0}

        entitlement = await self.db.fetch_one(
            """
            SELECT plan_slug, status, cancel_at_period_end, current_period_end
            FROM scriber_entitlements
            WHERE install_id = %(install_id)s
            """,
            {"install_id": install_id},
        )

        pending_checkout = await self.db.fetch_one(
            """
            SELECT checkout_session_id
            FROM scriber_checkout_sessions
            WHERE install_id = %(install_id)s AND status = 'open'
            ORDER BY created_at DESC
            LIMIT 1
            """,
            {"install_id": install_id},
        )

        free_seconds_granted = int(install["free_seconds_granted"])
        free_seconds_used = max(int(usage["used_seconds"] or 0), 0)
        free_seconds_remaining = max(free_seconds_granted - free_seconds_used, 0)

        if entitlement and str(entitlement["status"]) in PAID_PLAN_STATUSES:
            return EntitlementSnapshot(
                install_id=install_id,
                entitlement_status="active",
                plan_slug=str(entitlement["plan_slug"]),
                free_seconds_granted=free_seconds_granted,
                free_seconds_used=free_seconds_used,
                free_seconds_remaining=free_seconds_remaining,
                can_transcribe=True,
                checkout_pending=pending_checkout is not None,
            )

        if free_seconds_remaining > 0:
            return EntitlementSnapshot(
                install_id=install_id,
                entitlement_status="trial",
                plan_slug=None,
                free_seconds_granted=free_seconds_granted,
                free_seconds_used=free_seconds_used,
                free_seconds_remaining=free_seconds_remaining,
                can_transcribe=True,
                checkout_pending=pending_checkout is not None,
            )

        status = str(entitlement["status"]) if entitlement else "paywalled"
        normalized_status = "paywalled" if status in {"open", "incomplete", "expired"} else status
        return EntitlementSnapshot(
            install_id=install_id,
            entitlement_status=normalized_status,
            plan_slug=str(entitlement["plan_slug"]) if entitlement else None,
            free_seconds_granted=free_seconds_granted,
            free_seconds_used=free_seconds_used,
            free_seconds_remaining=0,
            can_transcribe=False,
            checkout_pending=pending_checkout is not None,
        )

    def issue_session_token(self, snapshot: EntitlementSnapshot) -> str | None:
        if not snapshot.can_transcribe:
            return None
        expires_at = datetime.now(UTC) + timedelta(seconds=self.settings.scriber_session_token_ttl_seconds)
        payload = {
            "sub": f"scriber-install:{snapshot.install_id}",
            "tenant_id": self.settings.default_tenant_id,
            "auth_type": "scriber_install",
            "install_id": snapshot.install_id,
            "plan_slug": snapshot.plan_slug or "trial",
            "scopes": ["voice:asr"],
            "exp": expires_at,
        }
        return jwt.encode(payload, self.settings.jwt_secret, algorithm="HS256")

    async def attach_install_to_session(self, session_id: str, install_id: str) -> None:
        await self.db.execute(
            """
            UPDATE voice_sessions
            SET metadata = metadata || %(metadata_patch)s::jsonb
            WHERE id = %(session_id)s
            """,
            {
                "session_id": session_id,
                "metadata_patch": json.dumps({"scriber_install_id": install_id}),
            },
        )

    async def finalize_session_usage(self, session_id: str) -> EntitlementSnapshot | None:
        existing = await self.db.fetch_one(
            """
            SELECT install_id
            FROM scriber_usage_ledger
            WHERE session_id = %(session_id)s AND metric = 'asr_audio_seconds'
            """,
            {"session_id": session_id},
        )
        if existing:
            return await self.get_snapshot(str(existing["install_id"]))

        session = await self.db.fetch_one(
            """
            SELECT
              id,
              started_at,
              ended_at,
              metadata->>'scriber_install_id' AS scriber_install_id
            FROM voice_sessions
            WHERE id = %(session_id)s
            """,
            {"session_id": session_id},
        )
        if not session or not session.get("scriber_install_id"):
            return None

        started_at = session["started_at"]
        ended_at = session["ended_at"] or datetime.now(UTC)
        elapsed_seconds = max(1, math.ceil((ended_at - started_at).total_seconds()))
        install_id = str(session["scriber_install_id"])
        await self.db.execute(
            """
            INSERT INTO scriber_usage_ledger (
              ledger_id, install_id, session_id, metric, quantity_seconds, source
            ) VALUES (
              %(ledger_id)s, %(install_id)s, %(session_id)s, 'asr_audio_seconds', %(quantity_seconds)s, 'gateway'
            )
            ON CONFLICT (ledger_id) DO NOTHING
            """,
            {
                "ledger_id": f"ledger:{session_id}",
                "install_id": install_id,
                "session_id": session_id,
                "quantity_seconds": elapsed_seconds,
            },
        )
        return await self.get_snapshot(install_id)

    async def create_checkout_session(self, install_id: str, plan_slug: str, app_version: str | None = None) -> dict[str, str]:
        if not self.settings.scriber_stripe_secret_key:
            raise ValueError("SCRIBER_STRIPE_SECRET_KEY is not configured.")
        price_id = self._price_id_for_plan(plan_slug)
        if not price_id:
            raise ValueError(f"No Stripe price configured for plan '{plan_slug}'.")

        await self.touch_install(install_id, app_version=app_version, platform="linux")
        mode = "payment" if plan_slug == "founder" else "subscription"
        session = stripe.checkout.Session.create(
            mode=mode,
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=f"{self.settings.scriber_checkout_success_url}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=self.settings.scriber_checkout_cancel_url,
            client_reference_id=install_id,
            allow_promotion_codes=True,
            metadata={
                "product": "scriber",
                "install_id": install_id,
                "plan_slug": plan_slug,
            },
        )
        now = datetime.now(UTC)
        await self.db.execute(
            """
            INSERT INTO scriber_checkout_sessions (
              checkout_session_id, install_id, plan_slug, status, checkout_url, created_at, updated_at
            ) VALUES (
              %(checkout_session_id)s, %(install_id)s, %(plan_slug)s, 'open', %(checkout_url)s, %(now)s, %(now)s
            )
            ON CONFLICT (checkout_session_id) DO UPDATE SET
              checkout_url = EXCLUDED.checkout_url,
              updated_at = %(now)s
            """,
            {
                "checkout_session_id": session.id,
                "install_id": install_id,
                "plan_slug": plan_slug,
                "checkout_url": session.url,
                "now": now,
            },
        )
        await self.db.execute(
            """
            UPDATE scriber_installs
            SET last_checkout_session_id = %(checkout_session_id)s, updated_at = %(now)s
            WHERE install_id = %(install_id)s
            """,
            {
                "install_id": install_id,
                "checkout_session_id": session.id,
                "now": now,
            },
        )
        return {"checkout_url": session.url, "checkout_session_id": session.id}

    async def handle_webhook(self, payload: bytes, signature: str | None) -> None:
        if not self.settings.scriber_stripe_secret_key or not self.settings.scriber_stripe_webhook_secret:
            raise ValueError("Stripe webhook settings are incomplete.")
        if not signature:
            raise ValueError("Missing Stripe signature header.")

        event = stripe.Webhook.construct_event(payload=payload, sig_header=signature, secret=self.settings.scriber_stripe_webhook_secret)
        event_type = event["type"]
        data = event["data"]["object"]

        if event_type == "checkout.session.completed":
            await self._mark_checkout_completed(data)
            return

        if event_type == "customer.subscription.updated":
            await self._upsert_subscription_state(data)
            return

        if event_type == "customer.subscription.deleted":
            await self._upsert_subscription_state(data, forced_status="canceled")
            return

        if event_type == "invoice.payment_failed":
            subscription_id = data.get("subscription")
            if subscription_id:
                await self._set_subscription_status(str(subscription_id), "past_due")

    async def _mark_checkout_completed(self, session: Any) -> None:
        install_id = session.get("client_reference_id") or (session.get("metadata") or {}).get("install_id")
        plan_slug = (session.get("metadata") or {}).get("plan_slug", "pro")
        if not install_id:
            return
        now = datetime.now(UTC)
        customer_id = session.get("customer")
        email = ((session.get("customer_details") or {}).get("email")) or session.get("customer_email")
        await self.touch_install(install_id, app_version=None, platform="linux")
        await self.db.execute(
            """
            UPDATE scriber_installs
            SET email = COALESCE(%(email)s, email),
                stripe_customer_id = COALESCE(%(stripe_customer_id)s, stripe_customer_id),
                updated_at = %(now)s
            WHERE install_id = %(install_id)s
            """,
            {
                "install_id": install_id,
                "email": email,
                "stripe_customer_id": customer_id,
                "now": now,
            },
        )
        await self.db.execute(
            """
            UPDATE scriber_checkout_sessions
            SET status = 'completed',
                updated_at = %(now)s,
                completed_at = %(now)s
            WHERE checkout_session_id = %(checkout_session_id)s
            """,
            {
                "checkout_session_id": session["id"],
                "now": now,
            },
        )
        if plan_slug == "founder":
            await self.db.execute(
                """
                INSERT INTO scriber_entitlements (
                  install_id, plan_slug, status, stripe_customer_id, stripe_checkout_session_id, created_at, updated_at
                ) VALUES (
                  %(install_id)s, 'founder', 'founder', %(stripe_customer_id)s, %(checkout_session_id)s, %(now)s, %(now)s
                )
                ON CONFLICT (install_id) DO UPDATE SET
                  plan_slug = 'founder',
                  status = 'founder',
                  stripe_customer_id = COALESCE(EXCLUDED.stripe_customer_id, scriber_entitlements.stripe_customer_id),
                  stripe_checkout_session_id = EXCLUDED.stripe_checkout_session_id,
                  updated_at = %(now)s
                """,
                {
                    "install_id": install_id,
                    "stripe_customer_id": customer_id,
                    "checkout_session_id": session["id"],
                    "now": now,
                },
            )
            return

        subscription_id = session.get("subscription")
        if subscription_id:
            subscription = stripe.Subscription.retrieve(subscription_id)
            await self._upsert_subscription_state(subscription, install_id=install_id, checkout_session_id=session["id"])

    async def _upsert_subscription_state(
        self,
        subscription: Any,
        *,
        install_id: str | None = None,
        checkout_session_id: str | None = None,
        forced_status: str | None = None,
    ) -> None:
        metadata = subscription.get("metadata") or {}
        resolved_install_id = install_id or metadata.get("install_id")
        if not resolved_install_id:
            existing = await self.db.fetch_one(
                """
                SELECT install_id
                FROM scriber_entitlements
                WHERE stripe_subscription_id = %(subscription_id)s
                """,
                {"subscription_id": subscription["id"]},
            )
            if existing:
                resolved_install_id = str(existing["install_id"])
        if not resolved_install_id:
            return

        now = datetime.now(UTC)
        line_items = subscription.get("items", {}).get("data", [])
        price_id = line_items[0].get("price", {}).get("id") if line_items else None
        plan_slug = self._plan_for_price_id(price_id) or metadata.get("plan_slug") or "pro"
        status = forced_status or subscription.get("status") or "active"
        current_period_end_raw = subscription.get("current_period_end")
        current_period_end = (
            datetime.fromtimestamp(current_period_end_raw, tz=UTC)
            if isinstance(current_period_end_raw, (int, float))
            else None
        )
        await self.db.execute(
            """
            INSERT INTO scriber_entitlements (
              install_id, plan_slug, status, stripe_customer_id, stripe_subscription_id, stripe_checkout_session_id,
              cancel_at_period_end, current_period_end, created_at, updated_at
            ) VALUES (
              %(install_id)s, %(plan_slug)s, %(status)s, %(stripe_customer_id)s, %(stripe_subscription_id)s, %(stripe_checkout_session_id)s,
              %(cancel_at_period_end)s, %(current_period_end)s, %(now)s, %(now)s
            )
            ON CONFLICT (install_id) DO UPDATE SET
              plan_slug = EXCLUDED.plan_slug,
              status = EXCLUDED.status,
              stripe_customer_id = COALESCE(EXCLUDED.stripe_customer_id, scriber_entitlements.stripe_customer_id),
              stripe_subscription_id = EXCLUDED.stripe_subscription_id,
              stripe_checkout_session_id = COALESCE(EXCLUDED.stripe_checkout_session_id, scriber_entitlements.stripe_checkout_session_id),
              cancel_at_period_end = EXCLUDED.cancel_at_period_end,
              current_period_end = EXCLUDED.current_period_end,
              updated_at = %(now)s
            """,
            {
                "install_id": resolved_install_id,
                "plan_slug": plan_slug,
                "status": status,
                "stripe_customer_id": subscription.get("customer"),
                "stripe_subscription_id": subscription["id"],
                "stripe_checkout_session_id": checkout_session_id,
                "cancel_at_period_end": bool(subscription.get("cancel_at_period_end", False)),
                "current_period_end": current_period_end,
                "now": now,
            },
        )

    async def _set_subscription_status(self, subscription_id: str, status: str) -> None:
        await self.db.execute(
            """
            UPDATE scriber_entitlements
            SET status = %(status)s, updated_at = %(updated_at)s
            WHERE stripe_subscription_id = %(subscription_id)s
            """,
            {
                "status": status,
                "updated_at": datetime.now(UTC),
                "subscription_id": subscription_id,
            },
        )

    def _price_id_for_plan(self, plan_slug: str) -> str | None:
        mapping = {
            "founder": self.settings.scriber_founder_price_id,
            "pro": self.settings.scriber_pro_price_id,
            "studio": self.settings.scriber_studio_price_id,
        }
        return mapping.get(plan_slug)

    def _plan_for_price_id(self, price_id: str | None) -> str | None:
        if not price_id:
            return None
        for plan_slug, configured_price_id in {
            "founder": self.settings.scriber_founder_price_id,
            "pro": self.settings.scriber_pro_price_id,
            "studio": self.settings.scriber_studio_price_id,
        }.items():
            if configured_price_id == price_id:
                return plan_slug
        return None
