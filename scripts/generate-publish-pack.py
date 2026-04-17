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
    parser = argparse.ArgumentParser(
        description="Rewrite one topic into multi-platform publish packs with platform-specific markdown/json output"
    )
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
        "personality": [x for x in data.get("personality", []) if x],
        "writing_style": data.get("writing_style", "") or "真实、清楚、少一点套话",
        "target_audience": data.get("target_audience", "") or "关注该主题的读者",
        "core_values": [x for x in data.get("core_values", []) if x],
        "tone_examples": [x for x in data.get("tone_examples", []) if x],
        "preferred_platforms": [x for x in data.get("preferred_platforms", []) if x],
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


def split_sentences(text: str):
    cleaned = re.sub(r"#+\s*", "", text)
    cleaned = re.sub(r"\n+", "\n", cleaned).strip()
    parts = re.split(r"(?<=[。！？!?])|\n", cleaned)
    return [part.strip(" -•\t") for part in parts if part.strip(" -•\t")]


def shorten(text: str, limit: int):
    return text if len(text) <= limit else text[: max(limit - 1, 0)].rstrip() + "…"


def fallback_points(topic: str, angle: str, profile):
    return [
        f"先别急着追求所有平台同时自动化，先把「{topic}」讲清楚。",
        f"我更在意的角度是：{angle or f'为什么 {topic} 值得现在写'}。",
        f"站在 {profile['profession']} 的视角，内容稳定输出比一次性爆发更重要。",
        f"如果读者是 {profile['target_audience']}，就要把结论和行动建议直接给出来。",
    ]


def collect_points(body: str, topic: str, angle: str, profile):
    points = split_sentences(body)
    if len(points) < 4:
        points.extend(fallback_points(topic, angle, profile))
    deduped = []
    for point in points:
        normalized = point.strip()
        if normalized and normalized not in deduped:
            deduped.append(normalized)
    return deduped[:8]


def xhs_title(topic: str, angle: str):
    return shorten(f"{topic}：我为什么先把流程跑顺，再谈自动化", 20) if topic else shorten(angle or "我为什么先把流程跑顺，再谈自动化", 20)


def build_xiaohongshu(topic: str, angle: str, points, profile, base_tags):
    lines = [
        f"# {xhs_title(topic, angle)}",
        "",
        f"🌟 最近我一直在想「{topic}」这件事。" if topic else "🌟 最近我一直在复盘内容生产这件事。",
        f"😵 真正让我卡住的，不是不会写，而是 {shorten(points[0], 46)}",
        f"🧭 我现在更稳的做法，是先定角度：{shorten(angle or points[1], 46)}",
        f"✍️ 站在 {profile['profession']} 的视角，我会先讲清楚问题，再给 {profile['target_audience']} 一个能直接带走的判断。",
        f"✅ 这样拆完以后，小红书会更口语，公众号能写深，知乎也更容易讲逻辑。",
        "如果你也在做内容，你现在最卡的是选题、改写，还是发布？评论区告诉我。",
        "",
    ]
    tags = base_tags or ["内容工作流", "小红书运营", "发布包"]
    lines.append(" ".join(f"#{tag}" for tag in tags[:8]))
    return "\n".join(lines).strip() + "\n"


def build_wechat(topic: str, angle: str, points, profile):
    sections = [
        f"# {topic or '为什么我先把内容流程跑顺，再谈自动化'}",
        "",
        f"最近我反复在想一件事：{topic or '内容自动化'} 之所以让很多人焦虑，不是因为工具不够多，而是因为每次动笔前都要重新决定角度、结构和平台。",
        "",
        f"我现在更认可的判断是：{angle or points[1]}",
        "",
        f"先从我的工作方式说起。作为 {profile['profession']}，我越来越少追求“一步到位”，而是先把母稿写清楚，再把改写和发布整理成可复用的后半段流程。这样做最直接的好处，是我不会再为了同一个话题来回重写三遍。",
        "",
        f"具体到这次的话题，我会先确认三个问题。第一，这件事真正值得写的部分是什么；第二，读者 {profile['target_audience']} 最想带走哪一个判断；第三，我能不能用更像自己的语气把它讲明白。只要这三件事先确定，后面无论要写公众号、小红书还是知乎，差别都只是表达方式，而不是推倒重来。",
        "",
        f"拿这次的内容来说，我最想强调的不是“工具有多全”，而是 {shorten(points[0], 120)}。如果只追求看起来什么都能做，最后往往会把每一步都做成口号；反过来，先把流程跑顺，再让工具去承担重复劳动，整条链路会更稳，也更容易协作。",
        "",
        f"这也是我为什么会保留发布包这个中间结果。它让标题、正文、标签和封面建议都能先被审阅，再决定是否真的发出去。对于个人 IP 或小团队来说，这反而比直接代发更安全，因为你知道每个平台最终出现的到底是什么。",
        "",
        f"如果你也在处理 {topic or '多平台内容'}，不妨先试着把话题、角度和读者对象固定下来，再去做平台适配。很多时候，真正提高效率的不是更快地产出第一稿，而是减少后面无休止的返工。",
        "",
        "## 这篇内容可继续拆成什么",
        "",
        "1. 小红书版：保留结论和情绪，把句子压短，增加评论区互动。",
        "2. 知乎版：补上论证链路，把结论拆成 3 个更完整的小标题。",
        "3. 发布包：统一整理标题、正文、标签和封面建议，方便人工终审。",
    ]
    return "\n".join(sections).strip() + "\n"


def build_zhihu(topic: str, angle: str, points, profile):
    title = topic if topic and topic.endswith(("?", "？")) else f"{topic or '内容流程'}，为什么要先跑顺再谈自动化？"
    body = [
        f"# {title}",
        "",
        "先说结论：如果你的目标是持续输出，而不是只做一次爆款，那么先把“选题—改写—发布准备”这条链路跑顺，比一开始追求全自动更重要。",
        "",
        f"## 1. 为什么这个问题总让人反复返工",
        "",
        f"因为很多人真正缺的不是写作工具，而是稳定的表达结构。{shorten(points[0], 140)}。当每个平台都从零开始写，返工成本会被迅速放大。",
        "",
        "## 2. 我现在更推荐的做法是什么",
        "",
        f"我的做法是先固定母稿，再按平台拆版本。小红书负责情绪和钩子，公众号负责叙事和完整信息，知乎负责结论与论证。这样处理以后，同一个主题可以服务不同平台，但核心观点不会散掉。",
        "",
        "## 3. 为什么发布包反而是更稳的终点",
        "",
        f"因为发布包把标题、正文、标签、封面建议和注意事项都整理成了一个可审阅结果。对于 {profile['target_audience']} 来说，这意味着既能提高效率，也能保留最后的人为判断，不会因为“看起来自动化”而把错误直接同步到所有平台。",
        "",
        "## 4. 适合谁先这样做",
        "",
        f"如果你是 {profile['profession']}、独立创作者，或者需要团队协作复核内容的人，这套方法会比较合适。它不要求你一开始就接入所有发布接口，但能先把最常见的重写、整理和终审成本降下来。",
    ]
    return "\n".join(body).strip() + "\n"


def build_generic(platform_name: str, topic: str, angle: str, points, profile):
    lines = [
        f"# {topic or platform_name + ' 发布包草稿'}",
        "",
        f"适配平台：{platform_name}",
        f"核心角度：{angle or points[1]}",
        "",
    ]
    for idx, point in enumerate(points[:4], start=1):
        lines.append(f"{idx}. {point}")
    lines.extend([
        "",
        f"站在 {profile['profession']} 的视角，建议先审阅再发布。",
    ])
    return "\n".join(lines).strip() + "\n"


def adapt_content(platform_id: str, platform_name: str, args, profile, points):
    topic = args.topic or args.title or "这个话题"
    angle = args.angle
    if platform_id == "xiaohongshu":
        return xhs_title(topic, angle), build_xiaohongshu(topic, angle, points, profile, build_tags(args, profile, 8))
    if platform_id == "wechat_official":
        title = args.title or f"{topic}：为什么我先把内容流程跑顺，再谈自动化"
        return title, build_wechat(topic, angle, points, profile)
    if platform_id == "zhihu":
        title = args.title or (topic if topic.endswith(("?", "？")) else f"{topic}，为什么要先跑顺再谈自动化？")
        return title, build_zhihu(topic, angle, points, profile)
    title = args.title or f"{platform_name} 发布包草稿"
    return title, build_generic(platform_name, topic, angle, points, profile)


def trim_text(text: str, limit: int):
    cleaned = text.strip()
    truncated = False
    if limit and len(cleaned) > limit:
        cleaned = cleaned[: max(limit - 24, 0)].rstrip() + "\n\n[内容因平台长度限制被截断]"
        truncated = True
    return cleaned, truncated


def make_pack(platform, profile, args, points):
    display_name = platform["display_name"]["zh"]
    title, adapted_body = adapt_content(platform["platform_id"], display_name, args, profile, points)
    tags = build_tags(args, profile, platform.get("recommended_tags_count", 0))
    content, truncated = trim_text(adapted_body, platform.get("max_length", 0))
    checks = {
        "body_length": len(content),
        "max_length": platform.get("max_length", 0),
        "body_within_limit": len(content) <= platform.get("max_length", 0),
        "tags_count": len(tags),
        "recommended_tags_count": platform.get("recommended_tags_count", 0),
        "supports_cover": platform.get("supports_cover", False),
        "rewrite_mode": "template_adapted",
    }
    cover_idea = args.cover_idea or f"{title} / {display_name} / 比例 {platform.get('cover_ratio', 'none')}"
    notes = [
        f"格式优先级：{', '.join(platform.get('article_format', []))}",
        f"封面比例：{platform.get('cover_ratio', 'none')}",
        f"适配器标识：{platform.get('wechatsync_adapter', 'n/a')}",
        "当前脚本会按平台模板重写同一话题，并默认交付发布包，不直接代用户登录后台。",
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
    points = collect_points(body, args.topic or args.title, args.angle, profile)
    packs = [make_pack(platform_map[item], profile, args, points) for item in requested]
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
        "source_points": points,
        "packs": packs,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(to_markdown(packs, profile, args), encoding="utf-8")
    print(f"JSON: {json_path}")
    print(f"Markdown: {md_path}")


if __name__ == "__main__":
    main()
