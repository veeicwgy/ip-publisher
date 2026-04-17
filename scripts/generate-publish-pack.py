#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
PLATFORMS_FILE = REPO_ROOT / "config" / "platforms.yaml"
DEFAULT_PROFILE = Path.home() / ".ip-publisher" / "profile.yaml"


def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.strip().lower())
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "publish-pack"


def parse_args():
    parser = argparse.ArgumentParser(description="Generate multi-platform publish packs from config/platforms.yaml")
    parser.add_argument("--platform", nargs="+", required=True, help="Platform IDs or 'all'")
    parser.add_argument("--title", default="", help="Base title for the content")
    parser.add_argument("--topic", default="", help="Topic if title is not provided")
    parser.add_argument("--angle", default="", help="Core angle or argument")
    parser.add_argument("--body", default="", help="Body text passed inline")
    parser.add_argument("--body-file", default="", help="Path to a markdown/text file as source body")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--cover-idea", default="", help="Optional cover idea")
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE), help="Optional profile yaml path")
    parser.add_argument("--output-dir", default="outputs", help="Directory for generated packs")
    return parser.parse_args()


def load_platform_map():
    raw = load_yaml(PLATFORMS_FILE).get("platforms", [])
    return {item["platform_id"]: item for item in raw}


def load_profile(path: Path):
    data = load_yaml(path).get("ip_profile", {})
    return {
        "name": data.get("name", "") or "未命名 IP",
        "profession": data.get("profession", "") or "内容创作者",
        "writing_style": data.get("writing_style", "") or "真实、清楚、少一点套话",
        "target_audience": data.get("target_audience", "") or "关注该主题的读者",
        "core_values": [x for x in data.get("core_values", []) if x],
        "tone_examples": [x for x in data.get("tone_examples", []) if x],
    }


def read_body(args, profile):
    if args.body_file:
        return Path(args.body_file).read_text(encoding="utf-8").strip()
    if args.body.strip():
        return args.body.strip()
    topic = args.topic or args.title or "这个话题"
    angle = args.angle or f"为什么 {topic} 值得现在写"
    tone = profile["tone_examples"][0] if profile["tone_examples"] else "先把问题说清楚，再给出自己的判断。"
    return "\n\n".join([
        f"最近我在持续观察「{topic}」。",
        f"如果只把它当成热点，很容易写成泛泛而谈的总结；我更关心的是：{angle}。",
        f"我会先从 {profile['profession']} 的视角拆解问题，再补上对 {profile['target_audience']} 真正有帮助的行动建议。",
        "我通常会保留三个层次：先说发生了什么，再说为什么值得关注，最后说我会怎么做。",
        tone,
    ])


def build_tags(args, profile, limit):
    seeds = [item.strip() for item in args.tags.split(",") if item.strip()]
    seeds.extend(profile["core_values"])
    ordered = []
    for item in seeds:
        if item not in ordered:
            ordered.append(item)
    if limit <= 0:
        return []
    return ordered[:limit]


def trim_text(text: str, limit: int):
    cleaned = text.strip()
    truncated = False
    if limit and len(cleaned) > limit:
        cleaned = cleaned[: max(limit - 24, 0)].rstrip() + "\n\n[内容因平台长度限制被截断]"
        truncated = True
    return cleaned, truncated


def format_title(base_title: str, platform_name: str):
    if base_title:
        return base_title
    return f"{platform_name} 发布包草稿"


def make_pack(platform, profile, args, body):
    display_name = platform["display_name"]["zh"]
    title = format_title(args.title or args.topic, display_name)
    tags = build_tags(args, profile, platform.get("recommended_tags_count", 0))
    content, truncated = trim_text(body, platform.get("max_length", 0))
    checks = {
        "body_length": len(content),
        "max_length": platform.get("max_length", 0),
        "body_within_limit": len(content) <= platform.get("max_length", 0),
        "tags_count": len(tags),
        "recommended_tags_count": platform.get("recommended_tags_count", 0),
        "supports_cover": platform.get("supports_cover", False),
    }
    cover_idea = args.cover_idea or f"{title} / {display_name} / 比例 {platform.get('cover_ratio', 'none')}"
    notes = [
        f"格式优先级：{', '.join(platform.get('article_format', []))}",
        f"封面比例：{platform.get('cover_ratio', 'none')}",
        f"适配器标识：{platform.get('wechatsync_adapter', 'n/a')}",
        "当前仓库默认交付发布包，不直接代用户登录后台。",
    ]
    if truncated:
        notes.append("正文已按平台限制截断，请人工继续精修。")
    return {
        "platform_id": platform["platform_id"],
        "display_name": display_name,
        "title": title,
        "body": content,
        "tags": tags,
        "cover_idea": cover_idea,
        "checks": checks,
        "notes": notes,
    }


def to_markdown(packs, profile, args):
    lines = [
        "# Publish Pack",
        "",
        f"- 生成时间：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"- 主题：{args.topic or args.title or '未提供'}",
        f"- 角度：{args.angle or '未提供'}",
        f"- 人设：{profile['name']} / {profile['profession']}",
        "",
        "| 平台 | 标题 | 正文长度 | 标签数 | 封面 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for pack in packs:
        lines.append(
            f"| {pack['display_name']} | {pack['title']} | {pack['checks']['body_length']}/{pack['checks']['max_length']} | {pack['checks']['tags_count']} | {'是' if pack['checks']['supports_cover'] else '否'} |"
        )
    for pack in packs:
        lines.extend([
            "",
            f"## {pack['display_name']}",
            "",
            f"**标题**：{pack['title']}",
            "",
            "**正文**：",
            "",
            pack["body"],
            "",
            f"**标签**：{', '.join(pack['tags']) if pack['tags'] else '无'}",
            "",
            f"**封面建议**：{pack['cover_idea'] if pack['checks']['supports_cover'] else '该平台无需封面'}",
            "",
            "**发布备注**：",
            "",
        ])
        lines.extend([f"- {note}" for note in pack["notes"]])
    return "\n".join(lines).strip() + "\n"


def main():
    args = parse_args()
    platform_map = load_platform_map()
    requested = list(platform_map) if args.platform == ["all"] else args.platform
    unknown = [item for item in requested if item not in platform_map]
    if unknown:
        raise SystemExit(f"Unknown platform(s): {', '.join(unknown)}")
    profile = load_profile(Path(args.profile))
    body = read_body(args, profile)
    packs = [make_pack(platform_map[item], profile, args, body) for item in requested]
    output_dir = (REPO_ROOT / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = f"{stamp}-{slugify(args.title or args.topic or 'publish-pack')}"
    json_path = output_dir / f"{base_name}.json"
    md_path = output_dir / f"{base_name}.md"
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "profile": profile,
        "topic": args.topic,
        "angle": args.angle,
        "packs": packs,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(to_markdown(packs, profile, args), encoding="utf-8")
    print(f"JSON: {json_path}")
    print(f"Markdown: {md_path}")


if __name__ == "__main__":
    main()
