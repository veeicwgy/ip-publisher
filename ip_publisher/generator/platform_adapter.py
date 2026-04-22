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


def build_platform_variants(request: dict, draft: dict) -> dict:
    rules = _load_rules()
    keywords = request.get("seo", {}).get("primary_keywords", [])
    tags = [keyword.replace(" ", "") for keyword in keywords][:8]
    variants: dict[str, dict] = {}
    for platform in request.get("platforms", []):
        rule = rules[platform]
        title = draft["title"]
        body = draft["body_markdown"]
        if platform == "xiaohongshu":
            title = _shorten(title, rule["title_max_length"])
            body = "\n".join(
                [
                    f"# {title}",
                    "",
                    draft["summary"],
                    "",
                    "如果你也在搭知识库驱动的内容流程，可以先从“生成 + 审核”开始跑。",
                    "",
                    " ".join(f"#{tag}" for tag in tags),
                ]
            ).strip()
        elif platform == "zhihu":
            title = title if title.endswith("？") else _shorten(f"{title}，该怎么落地？", rule["title_max_length"])
        body = body[: rule["body_max_length"]]
        variants[platform] = {
            "title": title,
            "body_markdown": body,
            "checks": {
                "title_length": len(title),
                "title_max_length": rule["title_max_length"],
                "body_length": _body_length(body),
                "body_max_length": rule["body_max_length"],
                "within_limit": len(title) <= rule["title_max_length"] and _body_length(body) <= rule["body_max_length"],
                "cover_ratio": rule["cover_ratio"],
                "recommended_tags_count": rule["recommended_tags_count"],
            },
        }
    return variants
