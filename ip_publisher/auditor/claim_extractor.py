from __future__ import annotations


def extract_claims(draft: dict) -> list[dict]:
    return draft.get("claims", [])
