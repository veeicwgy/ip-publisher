from __future__ import annotations


def build_keyword_plan(request: dict) -> dict:
    seo = request.get("seo", {})
    return {
        "primary_keywords": seo.get("primary_keywords", []),
        "secondary_keywords": seo.get("secondary_keywords", []),
        "forbidden_terms": seo.get("forbidden_terms", []),
    }


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    lowered = text.lower()
    return [keyword for keyword in keywords if keyword.lower() in lowered]
