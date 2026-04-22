from __future__ import annotations


def audit_structure(request: dict, draft: dict, thresholds: dict) -> tuple[float, list[dict], list[dict]]:
    structure = request.get("structure") or {}
    signals = draft.get("structure_signals") or {}
    blockers: list[dict] = []
    warnings: list[dict] = []

    checks = {
        "OPENING_VALUE_MISSING": (
            structure.get("opening_value_required", False),
            signals.get("opening_mentions_product", False)
            and signals.get("opening_mentions_value", False)
            and signals.get("opening_within_100_chars", False),
            "导语需要在 100 字内明确产品名和核心价值主张。",
        ),
        "QA_SECTION_MISSING": (
            structure.get("qa_required", False),
            signals.get("qa_section_present", False),
            "文章需要用 Q&A 组织关键知识点，方便 AI 与搜索系统提取。",
        ),
        "COMPARISON_TABLE_MISSING": (
            structure.get("comparison_table_required", False),
            signals.get("comparison_table_present", False),
            "文章需要包含对比表格，而不是只有纯叙述。",
        ),
        "ENTITY_LABELS_MISSING": (
            structure.get("entity_labels_required", False),
            signals.get("entity_labels_present", False),
            "文章需要显式标注产品、关键词、热点、目标人群等实体。",
        ),
        "CODE_EXAMPLE_MISSING": (
            structure.get("code_example_required", False),
            signals.get("code_example_present", False),
            "技术内容需要给出可复现的完整代码示例。",
        ),
    }

    required_checks = 0
    passed_checks = 0
    for code, (required, passed, message) in checks.items():
        if not required:
            continue
        required_checks += 1
        if passed:
            passed_checks += 1
            continue
        blockers.append(
            {
                "code": code,
                "message": message,
                "location": "structure",
                "suggestion": "调整文章结构后重新生成，再进入审核流程。",
            }
        )

    ai_friendly_score = float(signals.get("ai_friendly_score", 0.0))
    if structure.get("ai_friendly_required", False) and ai_friendly_score < thresholds["min_ai_structure_score"]:
        warnings.append(
            {
                "code": "AI_STRUCTURE_WEAK",
                "message": "文章结构对 AI 检索与摘要仍偏弱，建议补强标题层级与问题导向结构。",
                "location": "structure",
                "suggestion": "确保存在 H1/H2/H3，并将关键信息放在前 100 字、Q&A 和表格里。",
            }
        )

    if required_checks == 0:
        return ai_friendly_score, blockers, warnings
    return (passed_checks / required_checks + ai_friendly_score) / 2, blockers, warnings
