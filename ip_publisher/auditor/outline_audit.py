from __future__ import annotations


def audit_outline(request: dict, draft: dict) -> tuple[float, list[dict], list[dict]]:
    required = (request.get("outline") or {}).get("must_include_sections") or []
    section_headings = {section["heading"] for section in draft.get("sections", [])}
    blockers: list[dict] = []
    warnings: list[dict] = []
    missing = [heading for heading in required if heading not in section_headings]
    for heading in missing:
        blockers.append(
            {
                "code": "MISSING_OUTLINE_SECTION",
                "message": f"缺少必含小节：{heading}",
                "location": "outline",
                "suggestion": "按 request.outline.must_include_sections 重新生成结构。",
            }
        )
    score = 1.0 if not required else (len(required) - len(missing)) / len(required)
    return score, blockers, warnings
