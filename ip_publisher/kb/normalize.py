from __future__ import annotations

import re
from datetime import datetime, timezone


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_heading(text: str) -> str:
    cleaned = normalize_text(text)
    return cleaned.lstrip("#").strip() or "未命名小节"


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.strip().lower())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "item"


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def extract_keywords(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]{2,}", text)
