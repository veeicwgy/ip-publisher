from __future__ import annotations

DEFAULT_OUTLINE = ["核心结论", "知识库价值", "审核引擎", "Phase 1 边界"]


def build_outline(request: dict) -> list[dict]:
    outline = request.get("outline") or {}
    headings = outline.get("must_include_sections") or DEFAULT_OUTLINE
    brief = outline.get("brief", "")
    return [
        {
            "heading": heading,
            "intent": brief or f"围绕 {heading} 组织可信内容",
        }
        for heading in headings
    ]
