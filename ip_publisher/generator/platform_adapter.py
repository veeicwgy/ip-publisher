from __future__ import annotations

from pathlib import Path

import yaml


RULES_PATH = Path(__file__).resolve().parents[1] / "config" / "platform_rules.yaml"


def _load_rules() -> dict:
    return yaml.safe_load(RULES_PATH.read_text(encoding="utf-8"))["platforms"]


def _shorten(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: max(limit - 1, 0)].rstrip() + "…"


def _body_length(text: str) -> int:
    return len(text.strip())


def _summary(text: str, limit: int) -> str:
    return _shorten(text.replace("\n", " ").strip(), limit)


def _build_tags(request: dict, recommended_count: int) -> list[str]:
    product_name = request.get("product", {}).get("name", "")
    keywords = request.get("seo", {}).get("primary_keywords", []) + request.get("seo", {}).get("secondary_keywords", [])
    tags = []
    for item in [product_name, *keywords]:
        cleaned = item.replace(" ", "").strip()
        if cleaned and cleaned not in tags:
            tags.append(cleaned)
    if recommended_count <= 0:
        return []
    return tags[:recommended_count]


def build_platform_variants(request: dict, draft: dict) -> dict:
    rules = _load_rules()
    variants: dict[str, dict] = {}
    publisher = (request.get("publish") or {}).get("publisher", "none")
    hotspot_title = (request.get("hotspot") or {}).get("title", "")
    for platform in request.get("platforms", []):
        rule = rules[platform]
        title = draft["title"]
        body = draft["body_markdown"]
        summary = _summary(draft.get("summary", ""), rule.get("summary_max_length", 120))
        tags = _build_tags(request, rule["recommended_tags_count"])
        if platform == "xiaohongshu":
            title = _shorten(title, rule["title_max_length"])
            body = "\n".join(
                [
                    f"# {title}",
                    "",
                    summary,
                    "",
                    "先把知识库、关键词和审核门槛对齐，再去放大流量，内容会稳很多。",
                    "",
                    " ".join(f"#{tag}" for tag in tags),
                ]
            ).strip()
        elif platform == "weibo":
            title = _shorten(title, rule["title_max_length"])
            body = _shorten(f"{summary} {' '.join(f'#{tag}' for tag in tags[:2])}".strip(), rule["body_max_length"])
        elif platform == "zhihu":
            title = title if title.endswith("？") else _shorten(f"{title}，该怎么落地？", rule["title_max_length"])
        elif platform in {"juejin", "csdn"}:
            title = _shorten(f"{title} | 实战版", rule["title_max_length"])
        elif platform == "toutiao":
            title = _shorten(f"{title}：给运营团队的一套落地方法", rule["title_max_length"])
        body = body[: rule["body_max_length"]]
        direct_rule = rule.get("direct_publish", {})
        adapter = rule.get("wechatsync_adapter", platform)
        direct_publish = {
            "supported": publisher == "wechatsync" and direct_rule.get("supported", False),
            "via": direct_rule.get("via", "manual_copy"),
            "draft_only": direct_rule.get("draft_only", False),
            "adapter": adapter,
            "notes": direct_rule.get("notes", "默认只输出可复制 payload。"),
            "cli_example": f"wechatsync sync outputs/{request['task_id']}/platforms/{platform}.md -p {adapter}"
            if publisher == "wechatsync" and direct_rule.get("supported", False)
            else "",
        }
        variants[platform] = {
            "title": title,
            "summary": summary,
            "body_markdown": body,
            "format": rule.get("default_output_format", "markdown"),
            "tags": tags,
            "cover_brief": f"{rule['display_name']} 封面以 {request.get('product', {}).get('name', '产品')} + {hotspot_title or '可信内容流程'} 为核心信息，按 {rule['cover_ratio']} 输出。",
            "direct_publish": direct_publish,
            "checks": {
                "title_length": len(title),
                "title_max_length": rule["title_max_length"],
                "summary_length": len(summary),
                "summary_max_length": rule.get("summary_max_length", 120),
                "body_length": _body_length(body),
                "body_max_length": rule["body_max_length"],
                "tags_count": len(tags),
                "within_limit": (
                    len(title) <= rule["title_max_length"]
                    and len(summary) <= rule.get("summary_max_length", 120)
                    and _body_length(body) <= rule["body_max_length"]
                ),
                "cover_ratio": rule["cover_ratio"],
                "recommended_tags_count": rule["recommended_tags_count"],
                "format": rule.get("default_output_format", "markdown"),
            },
        }
    return variants
