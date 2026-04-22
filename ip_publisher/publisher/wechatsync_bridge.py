from __future__ import annotations

from pathlib import Path


def build_sync_command(task_id: str, platform: str, adapter: str) -> str:
    article_path = Path("outputs") / task_id / "platforms" / f"{platform}.md"
    return f"wechatsync sync {article_path.as_posix()} -p {adapter}"


def bridge_notes() -> list[str]:
    return [
        "Wechatsync 依赖浏览器扩展读取你自己的已登录态，不托管账号密码。",
        "默认通过平台 Web 编辑器同源接口写入草稿，发布前仍建议人工终审。",
        "Phase 1 只输出直发就绪信息；真正执行同步前必须先确保 audit_report.status == pass。",
    ]
