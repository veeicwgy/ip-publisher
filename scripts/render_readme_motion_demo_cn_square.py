#!/usr/bin/env python3
"""Render a square Chinese README motion demo as animated GIF + contact sheet."""

from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "readme" / "demo-preview"
FRAMES_DIR = OUT_DIR / "frames-cn-square"
GIF_PATH = OUT_DIR / "request-audit-publish-demo-cn-square.gif"
SHEET_PATH = OUT_DIR / "request-audit-publish-demo-cn-square-sheet.png"

WIDTH = 1080
HEIGHT = 1080
FRAMES = 84
FPS = 20


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def ease_out_cubic(t: float) -> float:
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    t = clamp(t)
    if t < 0.5:
        return 4 * t * t * t
    return 1 - ((-2 * t + 2) ** 3) / 2


def progress(frame: int, start: int, end: int, ease=ease_out_cubic) -> float:
    if frame <= start:
        return 0.0
    if frame >= end:
        return 1.0
    return ease((frame - start) / (end - start))


def scene_alpha(frame: int, fade_in_start: int, fade_in_end: int, fade_out_start: int | None = None,
                fade_out_end: int | None = None) -> float:
    value = progress(frame, fade_in_start, fade_in_end, ease_in_out_cubic)
    if fade_out_start is not None and fade_out_end is not None:
        value *= 1.0 - progress(frame, fade_out_start, fade_out_end, ease_in_out_cubic)
    return clamp(value)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def fmt(value: float) -> str:
    if isinstance(value, int):
        return str(value)
    if abs(value - round(value)) < 1e-6:
        return str(int(round(value)))
    return f"{value:.2f}"


def rect(x: float, y: float, w: float, h: float, rx: float, fill: str, stroke: str | None = None,
         stroke_width: float = 1.5, fill_opacity: float | None = None, stroke_opacity: float | None = None) -> str:
    attrs = [
        f'x="{fmt(x)}"',
        f'y="{fmt(y)}"',
        f'width="{fmt(w)}"',
        f'height="{fmt(h)}"',
        f'rx="{fmt(rx)}"',
        f'fill="{fill}"',
    ]
    if stroke:
        attrs.append(f'stroke="{stroke}"')
        attrs.append(f'stroke-width="{fmt(stroke_width)}"')
    if fill_opacity is not None:
        attrs.append(f'fill-opacity="{fill_opacity:.3f}"')
    if stroke_opacity is not None:
        attrs.append(f'stroke-opacity="{stroke_opacity:.3f}"')
    return f"<rect {' '.join(attrs)}/>"


def text(x: float, y: float, content: str, klass: str, fill: str | None = None, opacity: float | None = None) -> str:
    attrs = [f'x="{fmt(x)}"', f'y="{fmt(y)}"', f'class="{klass}"']
    if fill:
        attrs.append(f'fill="{fill}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:.3f}"')
    return f"<text {' '.join(attrs)}>{escape(content)}</text>"


def metric_row(x: float, y: float, label: str, value: float, reveal: float, opacity: float = 1.0) -> str:
    bar_w = 142
    fill_w = bar_w * reveal
    return (
        text(x, y, label, "metricLabel", opacity=opacity)
        + text(x + 162, y, f"{value:.2f}", "metricValue", opacity=opacity)
        + rect(x, y + 11, bar_w, 8, 4, "#0B1220", fill_opacity=0.10 * opacity)
        + rect(x, y + 11, fill_w, 8, 4, "#16A34A", fill_opacity=0.95 * opacity)
    )


def platform_chip(x: float, y: float, label: str, reveal: float) -> str:
    width = 34 + len(label) * 16
    return (
        rect(x, y, width, 30, 15, "#FFFFFF", stroke="#BFDBFE", stroke_width=1.2,
             fill_opacity=0.14 * reveal + 0.02, stroke_opacity=0.65 * reveal)
        + text(x + 14, y + 20, label, "platformChip", fill="#F8FAFC", opacity=0.35 + 0.65 * reveal)
    )


def stage_chip(x: float, y: float, label: str, active: float) -> str:
    fill_opacity = 0.05 + 0.16 * active
    stroke_opacity = 0.12 + 0.40 * active
    text_opacity = 0.38 + 0.52 * active
    width = 38 + len(label) * 17
    return (
        rect(x, y, width, 32, 16, "#FFFFFF", stroke="#BFDBFE", stroke_width=1.2,
             fill_opacity=fill_opacity, stroke_opacity=stroke_opacity)
        + text(x + 14, y + 21, label, "stageChip", fill="#F8FAFC", opacity=text_opacity)
    )


def render_frame(frame: int) -> str:
    req_p = progress(frame, 0, 12, ease_in_out_cubic)
    evidence_a = scene_alpha(frame, 12, 20, 24, 28)
    draft_a = scene_alpha(frame, 30, 38, 42, 46)
    audit_a = scene_alpha(frame, 48, 56)
    pub_p = progress(frame, 60, 72, ease_in_out_cubic)
    hold_p = progress(frame, 70, 82, ease_in_out_cubic)

    request_active = max(req_p, 0.25 if frame >= 12 else 0.0)
    evidence_active = max(evidence_a, 0.25 if frame >= 20 else 0.0)
    draft_active = max(draft_a, 0.25 if frame >= 38 else 0.0)
    audit_active = max(audit_a, 0.25 if frame >= 56 else 0.0)
    publish_active = max(pub_p, 0.25 if frame >= 72 else 0.0)

    req_x = lerp(24, 54, req_p)
    req_y = lerp(448, 424, req_p)
    req_op = req_p

    center_x = 388
    center_y = lerp(390, 366, max(evidence_a, draft_a, audit_a, 0.0))
    center_op = max(evidence_a, draft_a, audit_a)

    pub_x = lerp(756, 724, pub_p)
    pub_y = lerp(448, 424, pub_p)
    pub_op = pub_p

    line1_p = progress(frame, 14, 22, ease_in_out_cubic)
    line2_p = progress(frame, 60, 68, ease_in_out_cubic)
    metrics_p = progress(frame, 50, 60, ease_out_cubic)
    package_p = progress(frame, 62, 74, ease_out_cubic)

    glow_shift = math.sin(frame / 10) * 8
    float_y = math.sin(frame / 12) * 2.5

    request_card = []
    request_card.append(rect(req_x, req_y + float_y, 248, 248, 30, "#FFFFFF", stroke="#BFDBFE", stroke_width=1.5,
                             fill_opacity=0.97, stroke_opacity=0.55))
    request_card.append(rect(req_x + 22, req_y + 22 + float_y, 78, 30, 15, "#DBEAFE", fill_opacity=0.98))
    request_card.append(text(req_x + 40, req_y + 42 + float_y, "请求", "chip", fill="#1D4ED8", opacity=req_op))
    request_card.append(text(req_x + 22, req_y + 90 + float_y, "MinerU 演示", "cardTitle", fill="#0F172A", opacity=req_op))
    request_card.append(text(req_x + 22, req_y + 124 + float_y, "知识库：overview + faq", "cardCopy", fill="#334155", opacity=req_op))
    request_card.append(text(req_x + 22, req_y + 152 + float_y, "SEO：MinerU 知识库", "cardCopy", fill="#334155", opacity=req_op))
    request_card.append(text(req_x + 22, req_y + 180 + float_y, "热点：可信且可审计内容", "cardCopy", fill="#334155", opacity=req_op))
    request_card.append(text(req_x + 22, req_y + 218 + float_y, "大纲：结论 / 价值 / 审核 / 边界", "cardSmall", fill="#64748B", opacity=req_op))

    center_card = []
    center_card.append(rect(center_x, center_y - float_y, 304, 360, 30, "#FFFFFF", stroke="#D1FAE5", stroke_width=1.5,
                            fill_opacity=0.98, stroke_opacity=0.65))

    center_card.append(rect(center_x + 26, center_y + 24 - float_y, 96, 32, 16, "#DBEAFE", fill_opacity=evidence_a))
    center_card.append(text(center_x + 50, center_y + 45 - float_y, "知识片段", "chip", fill="#1D4ED8", opacity=evidence_a))
    center_card.append(text(center_x + 26, center_y + 96 - float_y, "知识库取证", "cardTitle", fill="#0F172A", opacity=evidence_a))
    center_card.append(text(center_x + 26, center_y + 132 - float_y, "mineru-overview::sec-1::1", "cardCopy", fill="#334155", opacity=evidence_a))
    center_card.append(text(center_x + 26, center_y + 160 - float_y, "mineru-overview::sec-2::1", "cardCopy", fill="#334155", opacity=evidence_a))
    center_card.append(text(center_x + 26, center_y + 188 - float_y, "mineru-faq::faq-2::1", "cardCopy", fill="#334155", opacity=evidence_a))
    center_card.append(text(center_x + 26, center_y + 228 - float_y, "只保留可回溯的知识块，再进入写作。", "cardSmall", fill="#64748B", opacity=evidence_a))
    center_card.append(text(center_x + 26, center_y + 258 - float_y, "每个关键结论都要能回到原始知识库。", "cardSmall", fill="#64748B", opacity=evidence_a))

    center_card.append(rect(center_x + 26, center_y + 24 - float_y, 96, 32, 16, "#FDE68A", fill_opacity=draft_a))
    center_card.append(text(center_x + 50, center_y + 45 - float_y, "主稿结构", "chip", fill="#B45309", opacity=draft_a))
    center_card.append(text(center_x + 26, center_y + 96 - float_y, "文章预览", "cardTitle", fill="#0F172A", opacity=draft_a))
    center_card.append(rect(center_x + 26, center_y + 118 - float_y, 252, 132, 18, "#F8FAFC", stroke="#E2E8F0", stroke_width=1.2,
                            fill_opacity=0.98 * draft_a, stroke_opacity=0.85 * draft_a))
    center_card.append(text(center_x + 42, center_y + 146 - float_y, "MinerU 知识库：如何稳住自动生成文章", "cardSmall", fill="#0F172A", opacity=draft_a))
    center_card.append(text(center_x + 42, center_y + 174 - float_y, "开头 100 字出现产品名与核心价值。", "cardSmall", fill="#475569", opacity=draft_a))
    center_card.append(text(center_x + 42, center_y + 198 - float_y, "Q&A 拆知识点，对比表格放复杂信息。", "cardSmall", fill="#475569", opacity=draft_a))
    center_card.append(text(center_x + 42, center_y + 222 - float_y, "H1 / H2 / H3 分层明确，利于 AI 提取。", "cardSmall", fill="#475569", opacity=draft_a))
    center_card.append(rect(center_x + 26, center_y + 270 - float_y, 56, 26, 13, "#E0F2FE", fill_opacity=draft_a))
    center_card.append(text(center_x + 42, center_y + 288 - float_y, "Q&A", "platformChip", fill="#0369A1", opacity=draft_a))
    center_card.append(rect(center_x + 90, center_y + 270 - float_y, 92, 26, 13, "#DCFCE7", fill_opacity=draft_a))
    center_card.append(text(center_x + 106, center_y + 288 - float_y, "对比表格", "platformChip", fill="#15803D", opacity=draft_a))
    center_card.append(rect(center_x + 190, center_y + 270 - float_y, 74, 26, 13, "#E9D5FF", fill_opacity=draft_a))
    center_card.append(text(center_x + 206, center_y + 288 - float_y, "实体标注", "platformChip", fill="#7C3AED", opacity=draft_a))
    center_card.append(rect(center_x + 26, center_y + 308 - float_y, 120, 34, 12, "#0F172A", fill_opacity=0.92 * draft_a))
    center_card.append(text(center_x + 42, center_y + 331 - float_y, "示例代码 / 数据块", "cardSmall", fill="#F8FAFC", opacity=draft_a))

    center_card.append(rect(center_x + 26, center_y + 24 - float_y, 74, 32, 16, "#16A34A", fill_opacity=audit_a))
    center_card.append(text(center_x + 49, center_y + 45 - float_y, "通过", "chip", fill="#F8FAFC", opacity=audit_a))
    center_card.append(text(center_x + 26, center_y + 96 - float_y, "审核闸门", "cardTitle", fill="#0F172A", opacity=audit_a))
    center_card.append(text(center_x + 26, center_y + 132 - float_y, "事实对齐、关键词、结构", "cardCopy", fill="#334155", opacity=audit_a))
    center_card.append(text(center_x + 26, center_y + 158 - float_y, "和平台规则全部检查。", "cardCopy", fill="#334155", opacity=audit_a))
    center_card.append(metric_row(center_x + 26, center_y + 214 - float_y, "事实对齐", 1.00, metrics_p * audit_a, audit_a))
    center_card.append(metric_row(center_x + 26, center_y + 248 - float_y, "关键词", 1.00, metrics_p * audit_a, audit_a))
    center_card.append(metric_row(center_x + 26, center_y + 282 - float_y, "结构", 1.00, metrics_p * audit_a, audit_a))
    center_card.append(metric_row(center_x + 26, center_y + 316 - float_y, "平台", 1.00, metrics_p * audit_a, audit_a))

    publish_card = []
    publish_card.append(rect(pub_x, pub_y + float_y, 292, 248, 30, "#FFFFFF", stroke="#BFDBFE", stroke_width=1.5,
                             fill_opacity=0.97 if pub_op > 0.02 else 0.12, stroke_opacity=0.62 * pub_op))
    publish_card.append(rect(pub_x + 22, pub_y + 22 + float_y, 98, 30, 15, "#DBEAFE", fill_opacity=pub_op))
    publish_card.append(text(pub_x + 42, pub_y + 42 + float_y, "发布包", "chip", fill="#1D4ED8", opacity=pub_op))
    publish_card.append(text(pub_x + 22, pub_y + 90 + float_y, "准备交付", "cardTitle", fill="#0F172A", opacity=pub_op))
    publish_card.append(text(pub_x + 22, pub_y + 126 + float_y, "article.md", "cardCopy", fill="#334155", opacity=package_p))
    publish_card.append(text(pub_x + 22, pub_y + 154 + float_y, "audit_report.json", "cardCopy", fill="#334155", opacity=package_p))
    publish_card.append(text(pub_x + 22, pub_y + 182 + float_y, "publish_package.json", "cardCopy", fill="#334155", opacity=package_p))
    publish_card.append(text(pub_x + 22, pub_y + 218 + float_y, "7 个平台版本已准备就绪", "cardSmall", fill="#64748B", opacity=package_p))

    platform_labels = ["公众号", "小红书", "知乎", "掘金", "CSDN", "头条", "微博"]
    platform_nodes = []
    x_cursor = pub_x + 18
    for idx, label in enumerate(platform_labels):
        reveal = progress(frame, 64 + idx * 2, 72 + idx * 2, ease_out_cubic)
        y_base = 706 if idx < 4 else 744
        if idx == 4:
            x_cursor = pub_x + 18
        platform_nodes.append(platform_chip(x_cursor, y_base, label, reveal))
        x_cursor += 18 + len(label) * 16

    line_y = 548
    line1_x2 = lerp(req_x + 248, center_x, line1_p)
    line2_x2 = lerp(center_x + 304, pub_x, line2_p)

    stage_labels = ["请求输入", "知识库取证", "主稿结构", "审核结果", "发布包"]
    stage_values = [request_active, evidence_active, draft_active, audit_active, publish_active]
    stage_nodes = []
    x_cursor = 72
    for label, active in zip(stage_labels, stage_values):
        stage_nodes.append(stage_chip(x_cursor, 350, label, active))
        x_cursor += 48 + len(label) * 17

    svg = f"""<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="62" y1="44" x2="1018" y2="1028" gradientUnits="userSpaceOnUse">
      <stop stop-color="#040B16"/>
      <stop offset="0.5" stop-color="#0F172A"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <radialGradient id="glowA" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({846 + glow_shift:.1f} 124) rotate(90) scale(190 240)">
      <stop stop-color="#2563EB" stop-opacity="0.62"/>
      <stop offset="1" stop-color="#2563EB" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({164 - glow_shift:.1f} 862) rotate(90) scale(180 220)">
      <stop stop-color="#7C3AED" stop-opacity="0.50"/>
      <stop offset="1" stop-color="#7C3AED" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="22" stdDeviation="22" flood-color="#000000" flood-opacity="0.24"/>
    </filter>
    <style>
      .sans {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Display","SFNS","Helvetica Neue",Arial,sans-serif; }}
      .chip {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 0.08em; }}
      .stageChip {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 13px; font-weight: 700; }}
      .kicker {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 12px; font-weight: 800; letter-spacing: 0.18em; }}
      .title {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Display","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 60px; font-weight: 800; }}
      .subtitle {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 19px; font-weight: 500; }}
      .cardTitle {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Display","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 24px; font-weight: 800; }}
      .cardCopy {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 15px; font-weight: 600; }}
      .cardSmall {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 13px; font-weight: 600; }}
      .metricLabel {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 14px; font-weight: 700; fill: #0F172A; }}
      .metricValue {{ font-family: "SF Pro Display","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 14px; font-weight: 800; fill: #0F172A; text-anchor: end; }}
      .platformChip {{ font-family: "PingFang SC","Hiragino Sans GB","SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 12px; font-weight: 700; }}
    </style>
  </defs>

  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>
  <circle cx="{fmt(846 + glow_shift)}" cy="124" r="212" fill="url(#glowA)"/>
  <circle cx="{fmt(164 - glow_shift)}" cy="862" r="180" fill="url(#glowB)"/>

  <text x="72" y="92" class="kicker" fill="#60A5FA">README 动效预览</text>
  <text x="72" y="162" class="title" fill="#FFFFFF">从请求，到</text>
  <text x="72" y="228" class="title" fill="#FFFFFF">发布包。</text>
  <text x="72" y="284" class="subtitle" fill="#CBD5E1">知识库输入、取证成稿、审核通过，再进入发布包。</text>
  <text x="72" y="316" class="subtitle" fill="#CBD5E1">让运营拿到可复查、可分发、可继续协作的内容结果。</text>

  {rect(738, 74, 240, 30, 15, "#0B1220", fill_opacity=0.26)}
  {text(764, 94, "请求 -> 取证 -> 成稿 -> 审核 -> 发布", "chip", fill="#F8FAFC", opacity=0.92)}
  {''.join(stage_nodes)}

  <path d="M{fmt(req_x + 248)} {line_y} C {fmt(req_x + 286)} {line_y}, {fmt(center_x - 32)} {line_y}, {fmt(line1_x2)} {line_y}" stroke="#60A5FA" stroke-opacity="{0.18 + 0.72 * line1_p:.3f}" stroke-width="4" stroke-linecap="round"/>
  <path d="M{center_x + 304} {line_y} C {center_x + 338} {line_y}, {fmt(pub_x - 24)} {line_y}, {fmt(line2_x2)} {line_y}" stroke="#60A5FA" stroke-opacity="{0.18 + 0.72 * line2_p:.3f}" stroke-width="4" stroke-linecap="round"/>

  <g filter="url(#shadow)" opacity="{req_op:.3f}">
    {''.join(request_card)}
  </g>

  <g filter="url(#shadow)" opacity="{center_op:.3f}">
    {''.join(center_card)}
  </g>

  <g filter="url(#shadow)" opacity="{pub_op:.3f}">
    {''.join(publish_card)}
    {''.join(platform_nodes)}
  </g>

  {rect(72, 946, 936, 54, 27, "#FFFFFF", stroke="#BFDBFE", stroke_width=1.2, fill_opacity=0.04 + 0.06 * hold_p, stroke_opacity=0.16 + 0.22 * hold_p)}
  {text(104, 980, "先取证，再成稿，再审核，最后进入发布包。", "cardCopy", fill="#E2E8F0", opacity=0.26 + 0.64 * hold_p)}
</svg>
"""
    return svg


def render_svg_frames() -> list[Path]:
    if shutil.which("rsvg-convert") is None or shutil.which("magick") is None:
        raise SystemExit("This script requires both rsvg-convert and magick in PATH.")

    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    png_paths: list[Path] = []
    for frame in range(FRAMES):
        svg_path = FRAMES_DIR / f"frame-{frame:03d}.svg"
        png_path = FRAMES_DIR / f"frame-{frame:03d}.png"
        svg_path.write_text(render_frame(frame), encoding="utf-8")
        subprocess.run(
            ["rsvg-convert", "-w", str(WIDTH), "-h", str(HEIGHT), str(svg_path), "-o", str(png_path)],
            check=True,
        )
        png_paths.append(png_path)
    return png_paths


def build_gif(png_paths: Iterable[Path]) -> None:
    delay = max(1, round(100 / FPS))
    subprocess.run(
        [
            "magick",
            *[str(path) for path in png_paths],
            "-delay",
            str(delay),
            "-loop",
            "0",
            "-layers",
            "Optimize",
            str(GIF_PATH),
        ],
        check=True,
    )


def build_sheet(frame_indices: list[int]) -> None:
    frame_paths = [FRAMES_DIR / f"frame-{index:03d}.png" for index in frame_indices]
    row1 = OUT_DIR / "row1-cn.png"
    row2 = OUT_DIR / "row2-cn.png"
    subprocess.run(
        [
            "magick",
            str(frame_paths[0]),
            "-bordercolor", "#F8FAFC", "-border", "24x24",
            str(frame_paths[1]),
            "-bordercolor", "#F8FAFC", "-border", "24x24",
            "+append",
            str(row1),
        ],
        check=True,
    )
    subprocess.run(
        [
            "magick",
            str(frame_paths[2]),
            "-bordercolor", "#F8FAFC", "-border", "24x24",
            str(frame_paths[3]),
            "-bordercolor", "#F8FAFC", "-border", "24x24",
            "+append",
            str(row2),
        ],
        check=True,
    )
    subprocess.run(["magick", str(row1), str(row2), "-append", str(SHEET_PATH)], check=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_paths = render_svg_frames()
    build_gif(png_paths)
    build_sheet([0, 24, 48, 76])
    print(f"GIF: {GIF_PATH}")
    print(f"Sheet: {SHEET_PATH}")


if __name__ == "__main__":
    main()
