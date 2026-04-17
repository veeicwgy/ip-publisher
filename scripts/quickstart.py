#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = Path.home() / ".ip-publisher" / "profile.yaml"
GENERATOR = REPO_ROOT / "scripts" / "generate-publish-pack.py"
DEFAULT_PLATFORMS = ["xiaohongshu", "wechat_official", "zhihu"]


def parse_args():
    parser = argparse.ArgumentParser(description="Interactive quickstart for IP Publisher")
    parser.add_argument("--topic", default="")
    parser.add_argument("--angle", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--name", default="")
    parser.add_argument("--profession", default="")
    parser.add_argument("--audience", default="")
    parser.add_argument("--style", default="")
    parser.add_argument("--platforms", nargs="+", default=[])
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE))
    parser.add_argument("--yes", action="store_true", help="Use defaults for confirmations in non-interactive mode")
    return parser.parse_args()


def ask(text: str, default: str = ""):
    suffix = f" [{default}]" if default else ""
    value = input(f"{text}{suffix}: ").strip()
    return value or default


def choose_profile(args):
    profile_path = Path(args.profile)
    if profile_path.exists() and not args.yes:
        reuse = ask("检测到本地 profile.yaml，是否直接复用？(y/n)", "y").lower()
        if reuse.startswith("y"):
            return str(profile_path), None
    if args.name or args.profession or args.audience or args.style:
        data = {
            "ip_profile": {
                "name": args.name or "未命名 IP",
                "profession": args.profession or "内容创作者",
                "writing_style": args.style or "真实、清楚、少一点套话",
                "target_audience": args.audience or "关注这个话题的人",
                "core_values": [item.strip() for item in args.tags.split(",") if item.strip()],
                "tone_examples": [args.angle or "先把问题说清楚，再给出自己的判断。"],
                "preferred_platforms": args.platforms or DEFAULT_PLATFORMS,
            }
        }
    elif args.yes:
        data = {
            "ip_profile": {
                "name": "未命名 IP",
                "profession": "内容创作者",
                "writing_style": "真实、清楚、少一点套话",
                "target_audience": "关注这个话题的人",
                "core_values": [item.strip() for item in args.tags.split(",") if item.strip()],
                "tone_examples": [args.angle or "先把问题说清楚，再给出自己的判断。"],
                "preferred_platforms": args.platforms or DEFAULT_PLATFORMS,
            }
        }
    else:
        print("\n没有强制要求先配完整人设，我只问你 4 个最关键的问题。\n")
        data = {
            "ip_profile": {
                "name": ask("你想让发布包里显示的名字", "未命名 IP"),
                "profession": ask("你的职业/领域", "内容创作者"),
                "writing_style": ask("希望整体语气更像什么", "真实、清楚、少一点套话"),
                "target_audience": ask("你希望主要写给谁看", "关注这个话题的人"),
                "core_values": [item.strip() for item in ask("补充 2-3 个关键词标签，用逗号分隔", args.tags).split(",") if item.strip()],
                "tone_examples": [args.angle or "先把问题说清楚，再给出自己的判断。"],
                "preferred_platforms": args.platforms or DEFAULT_PLATFORMS,
            }
        }
    temp_dir = Path(tempfile.mkdtemp(prefix="ip-publisher-profile-"))
    temp_profile = temp_dir / "profile.yaml"
    temp_profile.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return str(temp_profile), temp_dir


def gather_inputs(args):
    topic = args.topic or ask("你想改写的主题是什么", "为什么我先把内容流程跑顺，再谈自动化")
    angle = args.angle or ask("你最想强调的核心观点", f"先把「{topic}」讲清楚，再谈自动化")
    body = args.body or ask("输入 1-2 句背景或素材（可直接回车使用默认母稿）", "")
    tags = args.tags or ask("补充标签，逗号分隔", "内容工作流,发布包,多平台改写")
    platforms = args.platforms or ask("目标平台，空格分隔", "xiaohongshu wechat_official zhihu").split()
    return topic, angle, body, tags, platforms


def run_generator(topic, angle, body, tags, platforms, profile_path, output_dir):
    command = [
        sys.executable,
        str(GENERATOR),
        "--platform",
        *platforms,
        "--topic",
        topic,
        "--angle",
        angle,
        "--tags",
        tags,
        "--profile",
        profile_path,
        "--output-dir",
        output_dir,
    ]
    if body.strip():
        command.extend(["--body", body])
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return [line.split(": ", 1)[1].strip() for line in result.stdout.splitlines() if ": " in line]


def print_preview(paths):
    if not paths:
        return
    json_path = next((Path(item) for item in paths if item.endswith(".json")), None)
    md_path = next((Path(item) for item in paths if item.endswith(".md")), None)
    print("\n已生成发布包：")
    for item in paths:
        print(f"- {item}")
    if json_path and json_path.exists():
        data = json.loads(json_path.read_text(encoding="utf-8"))
        print("\n平台预览：")
        for pack in data.get("packs", []):
            print(f"\n[{pack['display_name']}] {pack['title']}")
            preview = pack["body"].strip().splitlines()[:5]
            for line in preview:
                print(line)
    if md_path and md_path.exists():
        print(f"\n你也可以直接打开 Markdown 发布包继续人工审阅：{md_path}")


def main():
    args = parse_args()
    print("IP Publisher Quickstart")
    print("这会把一个主题改写成小红书、公众号、知乎三个版本，并直接生成发布包。\n")
    topic, angle, body, tags, platforms = gather_inputs(args)
    profile_path, temp_dir = choose_profile(args)
    try:
        paths = run_generator(topic, angle, body, tags, platforms, profile_path, args.output_dir)
        print_preview(paths)
    finally:
        if temp_dir and temp_dir.exists():
            for item in temp_dir.glob("*"):
                item.unlink()
            temp_dir.rmdir()


if __name__ == "__main__":
    main()
