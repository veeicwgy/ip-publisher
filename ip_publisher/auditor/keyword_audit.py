from __future__ import annotations

from ..kb.normalize import extract_keywords
from ..planner.keyword_planner import build_keyword_plan, keyword_hits


def audit_keywords(request: dict, draft: dict) -> tuple[float, list[dict], list[dict], dict]:
    plan = build_keyword_plan(request)
    title = draft.get("title", "")
    summary = draft.get("summary", "")
    body = draft.get("body_markdown", "")
    blockers: list[dict] = []
    warnings: list[dict] = []
    title_hits = keyword_hits(title, plan["primary_keywords"])
    body_hits = keyword_hits(body, plan["primary_keywords"])
    summary_hits = keyword_hits(summary, plan["primary_keywords"])
    missing = [keyword for keyword in plan["primary_keywords"] if keyword not in body_hits]
    for keyword in missing:
        blockers.append(
            {
                "code": "MISSING_PRIMARY_KEYWORD",
                "message": f"正文未覆盖主关键词：{keyword}",
                "location": "body",
                "suggestion": "补充对应段落，明确把该关键词写进正文。",
            }
        )
    for keyword in plan["primary_keywords"]:
        if keyword not in title_hits:
            warnings.append(
                {
                    "code": "TITLE_KEYWORD_WEAK",
                    "message": f"标题未覆盖主关键词：{keyword}",
                    "location": "title",
                    "suggestion": "优先让标题至少命中一个主关键词。",
                }
            )
        if keyword not in summary_hits:
            warnings.append(
                {
                    "code": "SUMMARY_KEYWORD_WEAK",
                    "message": f"简介未覆盖主关键词：{keyword}",
                    "location": "summary",
                    "suggestion": "让简介也命中主关键词，方便搜索和大模型摘要抽取。",
                }
            )
    for term in plan["forbidden_terms"]:
        if term and term in body:
            blockers.append(
                {
                    "code": "FORBIDDEN_TERM",
                    "message": f"正文包含禁用词：{term}",
                    "location": "body",
                    "suggestion": "删除禁用词或改写为更稳妥的表达。",
                }
            )
    hotspot = request.get("hotspot") or {}
    hotspot_terms = extract_keywords(" ".join(part for part in [hotspot.get("title", ""), hotspot.get("summary", "")] if part))
    hotspot_hits = [term for term in hotspot_terms if term.lower() in "\n".join([title, summary, body]).lower()]
    if hotspot_terms and not hotspot_hits:
        blockers.append(
            {
                "code": "HOTSPOT_NOT_COVERED",
                "message": "热点线索没有出现在标题、简介或正文里。",
                "location": "hotspot",
                "suggestion": "让热点词至少命中标题、简介或正文之一，避免主题漂移。",
            }
        )
    primary_score = (
        len(set(title_hits + body_hits + summary_hits)) / max(len(plan["primary_keywords"]), 1)
        + (1.0 if not hotspot_terms else min(len(hotspot_hits) / len(hotspot_terms), 1.0))
    ) / 2
    metrics = {
        "primary_keywords_in_title": len(title_hits),
        "primary_keywords_in_summary": len(summary_hits),
        "hotspot_hit": 1 if hotspot_hits else 0,
    }
    return primary_score, blockers, warnings, metrics
