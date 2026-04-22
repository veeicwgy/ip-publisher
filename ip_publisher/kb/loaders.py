from __future__ import annotations

import json
import re
from pathlib import Path

from .normalize import normalize_heading, normalize_text, now_utc_iso, slugify


def _markdown_sections(text: str) -> list[dict]:
    sections: list[dict] = []
    heading = "导言"
    bucket: list[str] = []
    index = 1

    def flush() -> None:
        nonlocal bucket, heading, index
        content = normalize_text("\n".join(bucket))
        if not content:
            return
        sections.append(
            {
                "section_id": f"sec-{index}",
                "heading": normalize_heading(heading),
                "text": content,
            }
        )
        index += 1
        bucket = []

    for line in text.splitlines():
        if re.match(r"^\s{0,3}#{1,6}\s+", line):
            flush()
            heading = line
            continue
        bucket.append(line)
    flush()
    return sections


def _html_to_text(text: str) -> str:
    stripped = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    stripped = re.sub(r"<style[\s\S]*?</style>", " ", stripped, flags=re.I)
    stripped = re.sub(r"<[^>]+>", "\n", stripped)
    return normalize_text(stripped)


def _load_markdown(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title = next((line.lstrip("#").strip() for line in text.splitlines() if line.startswith("#")), path.stem)
    return {
        "doc_id": slugify(path.stem),
        "source_type": "markdown",
        "source_uri": str(path),
        "title": title,
        "tags": slugify(path.stem).split("-"),
        "updated_at": now_utc_iso(),
        "sections": _markdown_sections(text),
    }


def _load_html(path: Path) -> dict:
    text = _html_to_text(path.read_text(encoding="utf-8"))
    return {
        "doc_id": slugify(path.stem),
        "source_type": "html",
        "source_uri": str(path),
        "title": path.stem,
        "tags": slugify(path.stem).split("-"),
        "updated_at": now_utc_iso(),
        "sections": _markdown_sections(text),
    }


def _coerce_json_doc(payload: dict, fallback_stem: str) -> dict:
    sections = payload.get("sections", [])
    if sections and isinstance(sections[0], dict) and "text" in sections[0]:
        return {
            "doc_id": payload.get("doc_id", slugify(fallback_stem)),
            "source_type": payload.get("source_type", "manual"),
            "source_uri": payload.get("source_uri", f"file://{fallback_stem}"),
            "title": payload.get("title", fallback_stem),
            "tags": payload.get("tags", []),
            "updated_at": payload.get("updated_at", now_utc_iso()),
            "sections": sections,
        }
    raise ValueError(f"Unsupported JSON knowledge document: {fallback_stem}")


def _load_json(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [_coerce_json_doc(item, f"{path.stem}-{idx}") for idx, item in enumerate(payload, start=1)]
    return [_coerce_json_doc(payload, path.stem)]


def load_documents(kb_dir: Path) -> list[dict]:
    documents: list[dict] = []
    for path in sorted(kb_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".md":
            documents.append(_load_markdown(path))
        elif path.suffix.lower() in {".html", ".htm"}:
            documents.append(_load_html(path))
        elif path.suffix.lower() == ".json":
            documents.extend(_load_json(path))
    return documents
