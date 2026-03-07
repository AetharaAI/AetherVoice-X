from __future__ import annotations

from aether_common.auth import ensure_scopes


def require_scopes(*scopes: str):
    def checker(auth):
        ensure_scopes(auth, scopes)
        return auth

    return checker
