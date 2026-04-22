from __future__ import annotations

from copy import deepcopy

from .wechatsync_bridge import bridge_notes


def build_publish_package(request: dict, draft: dict) -> dict:
    publisher = (request.get("publish") or {}).get("publisher", "none")
    return {
        "package_version": "1.1",
        "publisher": publisher,
        "audit_gate": {
            "required_status": "pass",
            "status": "pending",
            "can_publish": False,
            "next_action": "manual_review",
        },
        "review_checklist": [
            "标题、简介、正文至少命中主关键词。",
            "热点词或选题线索至少出现在标题、简介或正文之一。",
            "关键声明必须能回溯到知识库 chunk_id。",
            "AI 友好结构必须包含 H1/H2/H3、Q&A、对比表格与实体标注。",
            "如果走 Wechatsync，同步目标默认为草稿，不直接正式发布。",
        ],
        "publisher_notes": bridge_notes() if publisher == "wechatsync" else ["当前只输出发布包，不执行直发。"],
        "platform_payloads": deepcopy(draft.get("platform_variants", {})),
    }


def finalize_publish_package(package: dict, audit_report: dict) -> dict:
    finalized = deepcopy(package)
    finalized["audit_gate"] = {
        "required_status": "pass",
        "status": audit_report["status"],
        "can_publish": audit_report["status"] == "pass",
        "next_action": audit_report["next_action"],
    }
    return finalized
