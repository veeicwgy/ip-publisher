from __future__ import annotations

from ..planner.keyword_planner import build_keyword_plan, keyword_hits


def audit_keywords(request: dict, draft: dict) -> tuple[float, list[dict], list[dict]]:
    plan = build_keyword_plan(request)
    title = draft.get("title", "")
    body = draft.get("body_markdown", "")
    blockers: list[dict] = []
    warnings: list[dict] = []
    title_hits = keyword_hits(title, plan["primary_keywords"])
    body_hits = keyword_hits(body, plan["primary_keywords"])
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
    primary_score = len(body_hits) / max(len(plan["primary_keywords"]), 1)
    return primary_score, blockers, warnings
