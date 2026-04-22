#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DEFAULT_PROFILE = Path.home() / ".ip-publisher" / "profile.yaml"
DEFAULT_KB_DIR = REPO_ROOT / "data" / "kb_raw"
DEFAULT_INDEX_DIR = REPO_ROOT / "data" / "kb_index"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "outputs"
DEFAULT_PLATFORMS = [
    "wechat_official",
    "xiaohongshu",
    "zhihu",
    "juejin",
    "csdn",
    "toutiao",
    "weibo",
]
DEFAULT_STRUCTURE = {
    "qa_required": True,
    "comparison_table_required": True,
    "ai_friendly_required": True,
    "authority_signal_required": True,
    "entity_labels_required": True,
    "opening_value_required": True,
    "code_example_required": False,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Interactive quickstart for KB-driven multi-platform publishing")
    parser.add_argument("--product-name", default="")
    parser.add_argument("--primary-keywords", default="")
    parser.add_argument("--secondary-keywords", default="")
    parser.add_argument("--forbidden-terms", default="")
    parser.add_argument("--hotspot", default="")
    parser.add_argument("--hotspot-summary", default="")
    parser.add_argument("--outline-brief", default="")
    parser.add_argument("--must-include-sections", default="")
    parser.add_argument("--audience", default="")
    parser.add_argument("--tone", default="")
    parser.add_argument("--content-type", choices=["general", "technical"], default="")
    parser.add_argument("--platforms", nargs="+", default=[])
    parser.add_argument("--kb-dir", default=str(DEFAULT_KB_DIR))
    parser.add_argument("--index-db", default="")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE))
    parser.add_argument("--publisher", choices=["none", "wechatsync"], default="wechatsync")
    parser.add_argument("--publish-mode", choices=["publish_pack", "direct_publish_ready"], default="direct_publish_ready")
    parser.add_argument("--yes", action="store_true")
    return parser.parse_args()


def ask(text: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{text}{suffix}: ").strip()
    return value or default


def resolve_input(cli_value: str, prompt: str, default: str, assume_yes: bool) -> str:
    if cli_value:
        return cli_value
    if assume_yes:
        return default
    return ask(prompt, default)


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def load_profile_defaults(path: Path) -> dict:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return payload.get("ip_profile", {})


def build_request(args: argparse.Namespace, profile_defaults: dict) -> dict:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    kb_dir = args.kb_dir or str(DEFAULT_KB_DIR)
    product_name = resolve_input(args.product_name, "产品或工具名", "MinerU", args.yes)
    primary_keywords = split_csv(
        resolve_input(
            args.primary_keywords,
            "需要运营的主关键词（逗号分隔）",
            f"{product_name} 知识库,自动生成文章",
            args.yes,
        )
    )
    secondary_keywords = split_csv(
        resolve_input(
            args.secondary_keywords,
            "补充次关键词（逗号分隔）",
            "内容审核,多平台发布,可信内容,AI 友好结构",
            args.yes,
        )
    )
    forbidden_terms = split_csv(
        resolve_input(args.forbidden_terms, "禁用词（逗号分隔，可直接回车）", "保证收录,全自动无人工", args.yes)
    )
    hotspot = resolve_input(args.hotspot, "热点线索 / 选题描述", "AI 内容运营开始回归可信和可审计", args.yes)
    hotspot_summary = resolve_input(
        args.hotspot_summary,
        "热点补充说明",
        "越来越多团队开始从追求一键生成，转向先做知识库驱动与审核闭环。",
        args.yes,
    )
    outline_brief = resolve_input(
        args.outline_brief,
        "大纲描述",
        f"围绕 {product_name} 在知识库驱动内容生产中的价值，解释为什么先做生成和审核，再接发布。",
        args.yes,
    )
    audience = resolve_input(
        args.audience,
        "主要读者",
        profile_defaults.get("target_audience", "内容运营和产品营销团队"),
        args.yes,
    )
    tone = args.tone or profile_defaults.get("writing_style", "专业、克制、可执行")
    if not tone and not args.yes:
        tone = ask("整体语气", "专业、克制、可执行")
    content_type = resolve_input(args.content_type, "内容类型（general / technical）", "general", args.yes)
    must_include_sections = split_csv(
        resolve_input(
            args.must_include_sections,
            "必须包含的小节（逗号分隔）",
            "核心结论,知识库价值,审核引擎,发布边界",
            args.yes,
        )
    )
    platforms = args.platforms or DEFAULT_PLATFORMS
    structure = dict(DEFAULT_STRUCTURE)
    structure["code_example_required"] = content_type == "technical"
    return {
        "task_id": f"quickstart-{timestamp}",
        "product": {
            "name": product_name,
        },
        "kb_scope": {
            "tags": ["knowledge-base"],
        },
        "seo": {
            "primary_keywords": primary_keywords,
            "secondary_keywords": secondary_keywords,
            "forbidden_terms": forbidden_terms,
        },
        "hotspot": {
            "title": hotspot,
            "summary": hotspot_summary,
            "source": "manual",
        },
        "outline": {
            "brief": outline_brief,
            "must_include_sections": must_include_sections,
        },
        "platforms": platforms,
        "audience": audience,
        "tone": tone,
        "content_type": content_type,
        "structure": structure,
        "publish": {
            "mode": args.publish_mode,
            "publisher": args.publisher,
        },
        "language": "zh-CN",
        "_runtime": {
            "kb_dir": kb_dir,
        },
    }


def run_workflow(request: dict, output_root: Path, index_db: Path) -> dict:
    from ip_publisher.workflows.phase1_generate_and_audit import run_phase1

    runtime = request.pop("_runtime")
    with tempfile.TemporaryDirectory(prefix="ip-publisher-request-") as temp_dir:
        request_path = Path(temp_dir) / "request.json"
        request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
        return run_phase1(
            request_path=request_path,
            kb_dir=Path(runtime["kb_dir"]),
            index_db=index_db,
            output_root=output_root,
        )


def print_preview(result: dict) -> None:
    artifacts = result["artifacts"]
    audit_report = result["audit_report"]
    draft = result["draft"]
    print("\n已生成知识库驱动发布包：")
    for key, value in artifacts.items():
        print(f"- {key}: {value}")
    print("\n审核摘要：")
    print(f"- 状态: {audit_report['status']}")
    print(f"- Overall Score: {audit_report['scores']['overall']:.2f}")
    print(f"- 可引用声明数: {audit_report.get('metrics', {}).get('citable_claims', 0)}")
    print(f"- 事实密度: {audit_report.get('metrics', {}).get('fact_density', 0):.2f}")
    print("\n平台预览：")
    for platform, variant in draft.get("platform_variants", {}).items():
        direct_publish = variant.get("direct_publish", {})
        mode = direct_publish.get("via", "manual_copy")
        print(f"\n[{platform}] {variant['title']}")
        print(f"格式: {variant['format']} | 标签: {', '.join(variant.get('tags', [])) or '无'} | 发布方式: {mode}")
        if direct_publish.get("cli_example"):
            print(f"Wechatsync: {direct_publish['cli_example']}")


def main() -> None:
    args = parse_args()
    print("IP Publisher Quickstart")
    print("这条路径会基于 知识库 + 关键词 + 热点 + 大纲，默认输出 7 平台发布包和 Wechatsync 草稿同步信息。\n")
    profile_defaults = load_profile_defaults(Path(args.profile))
    request = build_request(args, profile_defaults)
    index_db = Path(args.index_db) if args.index_db else DEFAULT_INDEX_DIR / f"{request['task_id']}.db"
    result = run_workflow(
        request=request,
        output_root=Path(args.output_root),
        index_db=index_db,
    )
    print_preview(result)


if __name__ == "__main__":
    main()
