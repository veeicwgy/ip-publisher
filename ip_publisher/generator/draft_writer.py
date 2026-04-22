from __future__ import annotations

from itertools import cycle

from .citations import source_note
from ..planner.keyword_planner import build_keyword_plan, keyword_hits


def _shorten(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: max(limit - 1, 0)].rstrip() + "…"


def _chunk_excerpt(chunk: dict, limit: int = 120) -> str:
    text = chunk.get("text", "").replace("\n", " ").strip()
    return _shorten(text, limit)


def _title(request: dict) -> str:
    product_name = request.get("product", {}).get("name", "产品")
    primary = request.get("seo", {}).get("primary_keywords", [])
    if len(primary) >= 2:
        first = primary[0]
        if first.lower().startswith(product_name.lower()):
            return f"{first}：如何稳住{primary[1]}"
        return f"{product_name}：如何用{first}稳住{primary[1]}"
    if primary:
        only = primary[0]
        if only.lower().startswith(product_name.lower()):
            return f"{only}：可信内容流程怎么搭"
        return f"{product_name}：围绕{only}搭建可信内容流程"
    return f"{product_name}：知识库驱动内容生产 Phase 1"


def _summary(request: dict, chunks: list[dict]) -> str:
    hotspot = request.get("hotspot", {}).get("summary", "")
    first = _chunk_excerpt(chunks[0], 80) if chunks else "先把知识来源固定下来，再谈自动化分发。"
    return " ".join(part for part in [hotspot, first] if part).strip()


def _section_content(heading: str, chunk_group: list[dict]) -> tuple[str, list[dict]]:
    bullets = []
    claims = []
    for idx, chunk in enumerate(chunk_group, start=1):
        snippet = _chunk_excerpt(chunk, 140)
        bullets.append(f"{idx}. {snippet}")
        claims.append(
            {
                "text": snippet,
                "source_chunk_ids": [chunk["chunk_id"]],
            }
        )
    content_lines = [
        f"围绕“{heading}”，可以先从知识库里确认以下要点：",
        *bullets,
        source_note([chunk["chunk_id"] for chunk in chunk_group]),
    ]
    return "\n".join(content_lines), claims


def build_base_draft(request: dict, outline: list[dict], chunks: list[dict]) -> dict:
    title = _title(request)
    summary = _summary(request, chunks)
    primary_keywords = request.get("seo", {}).get("primary_keywords", [])
    sections = []
    claims = []
    chunk_cycle = cycle(chunks or [{"chunk_id": "manual::seed::1", "text": summary, "heading": "摘要"}])
    for index, item in enumerate(outline, start=1):
        chunk_group = [next(chunk_cycle)]
        if len(chunks) > 1 and index % 2 == 1:
            chunk_group.append(next(chunk_cycle))
        content, section_claims = _section_content(item["heading"], chunk_group)
        source_ids = [claim["source_chunk_ids"][0] for claim in section_claims]
        sections.append(
            {
                "heading": item["heading"],
                "content": content,
                "source_chunk_ids": source_ids,
            }
        )
        for claim_index, claim in enumerate(section_claims, start=1):
            claims.append(
                {
                    "claim_id": f"claim-{index}-{claim_index}",
                    "text": claim["text"],
                    "source_chunk_ids": claim["source_chunk_ids"],
                }
            )
    body_parts = [f"# {title}", "", summary]
    if primary_keywords:
        body_parts.extend(["", f"关键词锚点：{', '.join(primary_keywords)}"])
    for section in sections:
        body_parts.extend(["", f"## {section['heading']}", "", section["content"]])
    body_markdown = "\n".join(body_parts).strip() + "\n"
    keyword_plan = build_keyword_plan(request)
    coverage_source = "\n".join([title, summary, body_markdown])
    return {
        "task_id": request["task_id"],
        "title": title,
        "summary": summary,
        "body_markdown": body_markdown,
        "sections": sections,
        "claims": claims,
        "keyword_coverage": {
            "primary_hit": keyword_hits(coverage_source, keyword_plan["primary_keywords"]),
            "missing_primary": [
                keyword for keyword in keyword_plan["primary_keywords"] if keyword not in keyword_hits(coverage_source, keyword_plan["primary_keywords"])
            ],
            "secondary_hit": keyword_hits(coverage_source, keyword_plan["secondary_keywords"]),
        },
    }
