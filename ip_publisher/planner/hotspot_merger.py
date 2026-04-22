from __future__ import annotations


def merge_hotspot_brief(request: dict) -> str:
    hotspot = request.get("hotspot") or {}
    title = hotspot.get("title", "")
    summary = hotspot.get("summary", "")
    if not (title or summary):
        return ""
    return " / ".join(part for part in [title, summary] if part)
