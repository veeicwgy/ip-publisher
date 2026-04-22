from __future__ import annotations

import json
from pathlib import Path


def _article_markdown(request: dict, draft: dict, audit_report: dict) -> str:
    lines = [
        f"# {draft['title']}",
        "",
        f"- Task ID: {request['task_id']}",
        f"- 审核状态: {audit_report['status']}",
        f"- Overall Score: {audit_report['scores']['overall']:.2f}",
        "",
        "## 摘要",
        "",
        draft.get("summary", ""),
        "",
        "## 主稿",
        "",
        draft.get("body_markdown", "").strip(),
        "",
        "## 平台版本",
    ]
    for platform, variant in draft.get("platform_variants", {}).items():
        lines.extend(
            [
                "",
                f"### {platform}",
                "",
                f"**标题**：{variant['title']}",
                "",
                variant["body_markdown"].strip(),
            ]
        )
    if audit_report.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend([f"- {item['code']}: {item['message']}" for item in audit_report["blockers"]])
    if audit_report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend([f"- {item['code']}: {item['message']}" for item in audit_report["warnings"]])
    return "\n".join(lines).strip() + "\n"


def write_artifacts(output_root: Path, request: dict, draft: dict, audit_report: dict) -> dict:
    task_dir = output_root / request["task_id"]
    task_dir.mkdir(parents=True, exist_ok=True)
    request_path = task_dir / "request.json"
    draft_path = task_dir / "draft.json"
    audit_path = task_dir / "audit_report.json"
    article_path = task_dir / "article.md"
    request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
    draft_path.write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8")
    audit_path.write_text(json.dumps(audit_report, ensure_ascii=False, indent=2), encoding="utf-8")
    article_path.write_text(_article_markdown(request, draft, audit_report), encoding="utf-8")
    return {
        "request": str(request_path),
        "draft": str(draft_path),
        "audit_report": str(audit_path),
        "article": str(article_path),
    }
