from __future__ import annotations

from itertools import cycle

from .citations import source_note
from .humanizer import humanize_markdown
from ..planner.keyword_planner import build_keyword_plan, keyword_hits


def _shorten(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: max(limit - 1, 0)].rstrip() + "…"


def _chunk_excerpt(chunk: dict, limit: int = 120) -> str:
    text = chunk.get("text", "").replace("\n", " ").strip()
    return _shorten(text, limit)


def _value_proposition(request: dict) -> str:
    keywords = request.get("seo", {}).get("primary_keywords", [])
    if len(keywords) >= 2:
        return f"把 {keywords[0]}、{keywords[1]} 和审核门槛收成可复核的内容流程"
    if keywords:
        return f"把 {keywords[0]} 和知识库证据收成可复核的文章流程"
    return "把知识库、关键词和审核规则收成可复核的文章流程"


def _title(request: dict) -> str:
    product_name = request.get("product", {}).get("name", "产品")
    primary = request.get("seo", {}).get("primary_keywords", [])
    if len(primary) >= 2:
        first = primary[0]
        title = f"{product_name} × {first}：如何把{primary[1]}做成可信内容流程"
        return _shorten(title, 58)
    if primary:
        only = primary[0]
        return _shorten(f"{product_name}：围绕{only}搭建知识库驱动的可信文章系统", 58)
    return f"{product_name}：知识库驱动内容生产 Phase 1"


def _summary(request: dict, chunks: list[dict]) -> str:
    product_name = request.get("product", {}).get("name", "产品")
    hotspot = request.get("hotspot", {}).get("summary", "")
    value = _value_proposition(request)
    opening = _shorten(f"{product_name} 的核心价值，是 {value}。", 100)
    if hotspot:
        return _shorten(f"{opening} {hotspot}", 120)
    first = _chunk_excerpt(chunks[0], 80) if chunks else "先把知识来源固定下来，再谈自动化分发。"
    return _shorten(f"{opening} {first}", 120)


def _section_content(heading: str, chunk_group: list[dict]) -> tuple[str, list[dict]]:
    claims = []
    bullets = []
    for idx, chunk in enumerate(chunk_group, start=1):
        snippet = _chunk_excerpt(chunk, 140)
        bullets.append(f"- 证据 {idx}：{snippet}")
        claims.append(
            {
                "text": snippet,
                "source_chunk_ids": [chunk["chunk_id"]],
            }
        )
    content_lines = [
        f"### {heading} 的直接证据",
        "",
        f"关于“{heading}”，知识库里至少已经明确写到这些信息：",
        "",
        *bullets,
        "",
        "### 对运营侧意味着什么",
        "",
        "写作时先把证据拎出来，再去展开观点，文章准确率会稳很多。",
        "",
        source_note([chunk["chunk_id"] for chunk in chunk_group]),
    ]
    return "\n".join(content_lines), claims


def _qa_section(request: dict, chunks: list[dict]) -> tuple[dict, list[dict]]:
    product_name = request.get("product", {}).get("name", "产品")
    keywords = request.get("seo", {}).get("primary_keywords", [])
    claims = []
    lines = []
    prompts = [
        f"{product_name} 最适合解决什么问题？",
        f"为什么这次内容要同时覆盖 {keywords[0] if keywords else '主关键词'}？",
        "为什么一定要先审核再发布？",
    ]
    for index, prompt in enumerate(prompts, start=1):
        chunk = chunks[(index - 1) % len(chunks)]
        answer = _chunk_excerpt(chunk, 120)
        lines.extend(
            [
                f"### Q{index}：{prompt}",
                "",
                f"A：{answer}",
                "",
                source_note([chunk["chunk_id"]]),
                "",
            ]
        )
        claims.append(
            {
                "claim_id": f"qa-{index}",
                "text": answer,
                "source_chunk_ids": [chunk["chunk_id"]],
            }
        )
    return {
        "heading": "关键知识点 Q&A",
        "content": "\n".join(lines).strip(),
        "source_chunk_ids": [claim["source_chunk_ids"][0] for claim in claims],
    }, claims


def _comparison_section(request: dict, chunks: list[dict]) -> dict:
    product_name = request.get("product", {}).get("name", "产品")
    lines = [
        "| 维度 | 传统素材拼接 | 知识库驱动生成 |",
        "| --- | --- | --- |",
        f"| 事实来源 | 依赖人工回忆 | 命中 {len(chunks)} 个知识片段后再写 |",
        "| 关键词覆盖 | 标题和正文常常不同步 | 生成前先锁定主关键词、次关键词与禁用词 |",
        f"| 平台改写 | 每个平台重写一遍 | 一次生成 {len(request.get('platforms', []))} 个平台 payload |",
        "| 发布动作 | 审稿和发布容易混在一起 | 先过审核，再输出发布包或草稿同步信息 |",
    ]
    return {
        "heading": "对比表格",
        "content": "\n".join(
            [
                "### 旧流程和新流程到底差在哪里",
                "",
                "\n".join(lines),
                "",
                f"{product_name} 这类主题更适合先把证据链整理清楚，再做平台差异化表达。",
            ]
        ),
        "source_chunk_ids": [chunk["chunk_id"] for chunk in chunks[:2]],
    }


def _authority_section(request: dict, claims: list[dict], chunks: list[dict]) -> dict:
    product_name = request.get("product", {}).get("name", "产品")
    keyword_plan = build_keyword_plan(request)
    doc_count = len({chunk["doc_id"] for chunk in chunks})
    platform_count = len(request.get("platforms", []))
    lines = [
        "### 权威信号",
        "",
        f"- 知识来源覆盖：本次写作命中 {doc_count} 篇知识文档、{len(chunks)} 个片段。",
        f"- 可引用声明：正文内保留 {len(claims)} 条带 chunk_id 的可追溯断言。",
        f"- 审核门槛：关键词命中、结构检查、grounding 和平台规则同时通过才允许发布。",
        f"- 平台范围：同一主题默认生成 {platform_count} 个平台 payload，避免重复提问目标平台。",
        "",
        "### 实体标注",
        "",
        f"- 产品：{product_name}",
        f"- 主关键词：{', '.join(keyword_plan['primary_keywords']) or '未设置'}",
        f"- 次关键词：{', '.join(keyword_plan['secondary_keywords']) or '未设置'}",
        f"- 热点线索：{(request.get('hotspot') or {}).get('title', '未设置')}",
        f"- 目标读者：{request.get('audience', '未设置')}",
    ]
    return {
        "heading": "权威信号与实体标注",
        "content": "\n".join(lines),
        "source_chunk_ids": [chunk["chunk_id"] for chunk in chunks[:2]],
    }


def _code_section(request: dict) -> dict:
    code_block = "\n".join(
        [
            "```bash",
            "python3 -m ip_publisher.cli.run_phase1 \\",
            "  --request data/tasks/demo-request.json \\",
            "  --kb-dir data/kb_raw \\",
            "  --index-db data/kb_index/demo.db \\",
            "  --output-root outputs/demo-run",
            "```",
        ]
    )
    lines = [
        "### 可复现执行方式",
        "",
        "下面这条命令就是这个工作流的最小复现路径：",
        "",
        code_block,
        "",
        "如果你要发技术内容，正文里最好直接给出这种能跑通的命令，而不是只写抽象流程。",
    ]
    return {
        "heading": "可复现代码示例",
        "content": "\n".join(lines),
        "source_chunk_ids": [],
    }


def _publish_section(request: dict) -> dict:
    publisher = (request.get("publish") or {}).get("publisher", "none")
    lines = [
        "### 审核通过后再进入发布",
        "",
        "- gate 1：标题、简介、正文命中主关键词。",
        "- gate 2：关键声明保留来源 chunk_id。",
        "- gate 3：AI 友好结构、Q&A、表格、实体标注齐全。",
        f"- gate 4：如果走 {publisher}，默认只进草稿，不直接正式发布。",
    ]
    return {
        "heading": "发布前检查",
        "content": "\n".join(lines),
        "source_chunk_ids": [],
    }


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
    qa_section, qa_claims = _qa_section(request, chunks or [{"chunk_id": "manual::seed::1", "text": summary}])
    sections.append(qa_section)
    claims.extend(qa_claims)
    sections.append(_comparison_section(request, chunks))
    sections.append(_authority_section(request, claims, chunks))
    if request.get("content_type") == "technical" or (request.get("structure") or {}).get("code_example_required"):
        sections.append(_code_section(request))
    sections.append(_publish_section(request))

    opening = _shorten(summary, 100)
    body_parts = [f"# {title}", "", opening, "", "## 文章摘要", "", draft_summary_line(summary)]
    if primary_keywords:
        body_parts.extend(["", f"关键词锚点：{', '.join(primary_keywords)}"])
    for section in sections:
        body_parts.extend(["", f"## {section['heading']}", "", section["content"]])
    body_markdown = humanize_markdown("\n".join(body_parts))
    keyword_plan = build_keyword_plan(request)
    hotspot = request.get("hotspot", {})
    hotspot_hit = False
    if hotspot:
        hotspot_terms = [hotspot.get("title", ""), hotspot.get("summary", "")]
        hotspot_hit = any(term and term in "\n".join([title, summary, body_markdown]) for term in hotspot_terms)
    coverage_source = "\n".join([title, summary, body_markdown])
    summary_hits = keyword_hits(summary, keyword_plan["primary_keywords"])
    structure_signals = {
        "opening_mentions_product": request.get("product", {}).get("name", "") in opening,
        "opening_mentions_value": "核心价值" in summary or "可复核" in summary or "可审核" in summary,
        "opening_within_100_chars": len(opening) <= 100,
        "qa_section_present": "## 关键知识点 Q&A" in body_markdown,
        "comparison_table_present": "| 维度 | 传统素材拼接 | 知识库驱动生成 |" in body_markdown,
        "entity_labels_present": "### 实体标注" in body_markdown,
        "authority_signal_count": 4,
        "code_example_present": "```bash" in body_markdown,
        "ai_friendly_score": sum(
            [
                "# " in body_markdown,
                "## " in body_markdown,
                "### " in body_markdown,
                "## 关键知识点 Q&A" in body_markdown,
                "| 维度 | 传统素材拼接 | 知识库驱动生成 |" in body_markdown,
                len(opening) <= 100,
            ]
        )
        / 6,
        "hotspot_hit": hotspot_hit,
    }
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
        "structure_signals": structure_signals,
    }


def draft_summary_line(summary: str) -> str:
    return summary
