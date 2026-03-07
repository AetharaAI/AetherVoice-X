from __future__ import annotations

from ..schemas.requests import ASRTriageRequest
from ..schemas.responses import TriageResult


DOMAIN_RULES = {
    "electrical_emergency": {
        "triggers": ["sparking", "burning smell", "panel hot", "breaker", "smoke", "buzzing", "arcing"],
        "recommended_action": "Escalate to emergency after-hours dispatch immediately.",
    },
    "hvac_after_hours": {
        "triggers": ["no heat", "no cooling", "furnace", "ac out", "leak"],
        "recommended_action": "Queue same-night HVAC callback and verify occupancy risk.",
    },
    "plumbing_emergency": {
        "triggers": ["burst pipe", "overflow", "sewage", "flooding", "water heater leaking"],
        "recommended_action": "Dispatch emergency plumbing response and advise water shutoff if safe.",
    },
    "locksmith_urgent": {
        "triggers": ["locked out", "child locked", "car lockout", "break in"],
        "recommended_action": "Escalate to urgent locksmith dispatch.",
    },
    "restoration_dispatch": {
        "triggers": ["water damage", "fire damage", "mold", "storm damage"],
        "recommended_action": "Trigger restoration intake and capture insurance details.",
    },
    "security_alarm_intake": {
        "triggers": ["alarm", "intruder", "glass break", "panic"],
        "recommended_action": "Escalate to security response and verify callback number.",
    },
}


class TriageService:
    async def classify(self, request_id: str, payload: ASRTriageRequest) -> TriageResult:
        transcript = payload.transcript.lower()
        rule = DOMAIN_RULES.get(payload.domain, DOMAIN_RULES["electrical_emergency"])
        hits = [trigger for trigger in rule["triggers"] if trigger in transcript]
        if any(term in transcript for term in ("smoke", "fire", "burning", "sparking", "arcing")):
            classification = "emergency"
            priority = 0.98
        elif hits:
            classification = "urgent"
            priority = 0.84
        elif len(transcript.split()) < 4:
            classification = "unclear"
            priority = 0.32
        else:
            classification = "standard"
            priority = 0.51
        analysis = (
            f"Sentinel scaffold matched {len(hits)} trigger(s) in the {payload.domain} profile."
            if hits
            else f"Sentinel scaffold found no domain trigger in the {payload.domain} profile."
        )
        return TriageResult(
            request_id=request_id,
            classification=classification,
            priority=priority,
            analysis=analysis,
            recommended_action=rule["recommended_action"],
            requires_human_review=classification in {"emergency", "urgent", "unclear"},
        )
