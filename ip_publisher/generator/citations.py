from __future__ import annotations


def source_note(source_chunk_ids: list[str]) -> str:
    if not source_chunk_ids:
        return "来源片段：无"
    return f"来源片段：{', '.join(source_chunk_ids)}"
