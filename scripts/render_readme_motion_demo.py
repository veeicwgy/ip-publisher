#!/usr/bin/env python3
"""Render a premium README motion demo as animated GIF + contact sheet.

This creates an Apple-keynote-inspired short animation for the README hero:
request -> audit -> publish package.
"""

from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "readme" / "demo-preview"
FRAMES_DIR = OUT_DIR / "frames"
GIF_PATH = OUT_DIR / "request-audit-publish-demo.gif"
SHEET_PATH = OUT_DIR / "request-audit-publish-demo-sheet.png"

WIDTH = 1280
HEIGHT = 720
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


def chip(x: float, y: float, label: str, width: float, fill: str, text_fill: str, opacity: float = 1.0) -> str:
    return (
        rect(x, y, width, 30, 15, fill, fill_opacity=opacity)
        + text(x + 18, y + 20, label, "chip", fill=text_fill, opacity=opacity)
    )


def metric_row(x: float, y: float, label: str, value: float, reveal: float) -> str:
    bar_w = 176
    fill_w = bar_w * reveal
    return (
        text(x, y, label, "metricLabel")
        + text(x + 196, y, f"{value:.2f}", "metricValue")
        + rect(x, y + 12, bar_w, 8, 4, "#0B1220", fill_opacity=0.10)
        + rect(x, y + 12, fill_w, 8, 4, "#16A34A", fill_opacity=0.95)
    )


def platform_chip(x: float, y: float, label: str, reveal: float) -> str:
    width = 22 + len(label) * 9
    return (
        rect(x, y, width, 28, 14, "#FFFFFF", stroke="#BFDBFE", stroke_width=1.2,
             fill_opacity=0.14 * reveal + 0.02, stroke_opacity=0.65 * reveal)
        + text(x + 14, y + 19, label, "platformChip", fill="#F8FAFC", opacity=0.35 + 0.65 * reveal)
    )


def render_frame(frame: int) -> str:
    req_p = progress(frame, 0, 18, ease_in_out_cubic)
    aud_p = progress(frame, 16, 38, ease_in_out_cubic)
    pub_p = progress(frame, 34, 58, ease_in_out_cubic)
    hold_p = progress(frame, 56, 76, ease_in_out_cubic)

    req_x = lerp(-280, 84, req_p)
    req_y = 228
    req_op = req_p

    aud_y = lerp(820, 168, aud_p)
    aud_op = aud_p

    pub_x = lerp(1380, 860, pub_p)
    pub_op = pub_p

    line1_p = progress(frame, 18, 32, ease_in_out_cubic)
    line2_p = progress(frame, 38, 52, ease_in_out_cubic)

    pass_p = progress(frame, 24, 38, ease_out_cubic)
    metrics_p = progress(frame, 28, 46, ease_out_cubic)
    package_p = progress(frame, 48, 66, ease_out_cubic)

    glow_shift = math.sin(frame / 10) * 18
    float_y = math.sin(frame / 12) * 6

    request_card = []
    request_card.append(rect(req_x, req_y + float_y, 320, 264, 28, "#FFFFFF", stroke="#BFDBFE", stroke_width=1.5,
                             fill_opacity=0.97, stroke_opacity=0.55))
    request_card.append(rect(req_x + 26, req_y + 26 + float_y, 98, 32, 16, "#DBEAFE", fill_opacity=0.98))
    request_card.append(text(req_x + 48, req_y + 47 + float_y, "REQUEST", "chip", fill="#1D4ED8", opacity=req_op))
    request_card.append(text(req_x + 26, req_y + 94 + float_y, "MinerU demo", "cardTitle", fill="#0F172A", opacity=req_op))
    request_card.append(text(req_x + 26, req_y + 128 + float_y, "KB: overview + faq", "cardCopy", fill="#334155", opacity=req_op))
    request_card.append(text(req_x + 26, req_y + 156 + float_y, "SEO: MinerU 知识库", "cardCopy", fill="#334155", opacity=req_op))
    request_card.append(text(req_x + 26, req_y + 184 + float_y, "Trend: trusted and reviewable content", "cardCopy", fill="#334155", opacity=req_op))
    request_card.append(text(req_x + 26, req_y + 224 + float_y, "Outline: request -> audit -> publish", "cardSmall", fill="#64748B", opacity=req_op))

    audit_card = []
    audit_card.append(rect(472, aud_y - float_y, 336, 384, 30, "#FFFFFF", stroke="#D1FAE5", stroke_width=1.5,
                           fill_opacity=0.98, stroke_opacity=0.65))
    audit_card.append(rect(500, aud_y + 28 - float_y, 82, 34, 17, "#16A34A", fill_opacity=pass_p))
    audit_card.append(text(526, aud_y + 50 - float_y, "PASS", "chip", fill="#F8FAFC", opacity=pass_p))
    audit_card.append(text(500, aud_y + 116 - float_y, "Audit gate", "cardTitle", fill="#0F172A", opacity=aud_op))
    audit_card.append(text(500, aud_y + 152 - float_y, "Grounding, keyword fit, structure,", "cardCopy", fill="#334155", opacity=aud_op))
    audit_card.append(text(500, aud_y + 180 - float_y, "and platform rules are all checked.", "cardCopy", fill="#334155", opacity=aud_op))
    audit_card.append(metric_row(500, aud_y + 232 - float_y, "Grounding", 1.00, metrics_p))
    audit_card.append(metric_row(500, aud_y + 272 - float_y, "Keyword fit", 1.00, metrics_p))
    audit_card.append(metric_row(500, aud_y + 312 - float_y, "Outline fit", 1.00, metrics_p))
    audit_card.append(metric_row(500, aud_y + 352 - float_y, "Platform fit", 1.00, metrics_p))

    publish_card = []
    publish_card.append(rect(pub_x, 228 + float_y, 336, 264, 28, "#FFFFFF", stroke="#BFDBFE", stroke_width=1.5,
                             fill_opacity=0.12 if pub_op < 0.02 else 0.97, stroke_opacity=0.62 * pub_op))
    publish_card.append(rect(pub_x + 26, 254 + float_y, 152, 32, 16, "#DBEAFE", fill_opacity=pub_op))
    publish_card.append(text(pub_x + 50, 275 + float_y, "PUBLISH PACKAGE", "chip", fill="#1D4ED8", opacity=pub_op))
    publish_card.append(text(pub_x + 26, 322 + float_y, "Ready for handoff", "cardTitle", fill="#0F172A", opacity=pub_op))
    publish_card.append(text(pub_x + 26, 356 + float_y, "article.md", "cardCopy", fill="#334155", opacity=package_p))
    publish_card.append(text(pub_x + 26, 384 + float_y, "audit_report.json", "cardCopy", fill="#334155", opacity=package_p))
    publish_card.append(text(pub_x + 26, 412 + float_y, "publish_package.json", "cardCopy", fill="#334155", opacity=package_p))
    publish_card.append(text(pub_x + 26, 446 + float_y, "7 payloads ready for channel handoff", "cardSmall", fill="#64748B", opacity=package_p))

    platform_labels = ["WeChat", "XHS", "Zhihu", "Juejin", "CSDN", "Toutiao", "Weibo"]
    platform_nodes = []
    x_cursor = pub_x + 26
    for idx, label in enumerate(platform_labels):
        reveal = progress(frame, 52 + idx * 2, 64 + idx * 2, ease_out_cubic)
        y_base = 474 + float_y if idx < 4 else 508 + float_y
        if idx == 4:
            x_cursor = pub_x + 26
        platform_nodes.append(platform_chip(x_cursor, y_base, label, reveal))
        x_cursor += 24 + len(label) * 9

    line1_x2 = lerp(req_x + 320, 472, line1_p)
    line2_x2 = lerp(808, pub_x, line2_p)

    svg = f"""<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="64" y1="48" x2="1216" y2="680" gradientUnits="userSpaceOnUse">
      <stop stop-color="#040B16"/>
      <stop offset="0.5" stop-color="#0F172A"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <radialGradient id="glowA" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({980 + glow_shift:.1f} 118) rotate(90) scale(180 240)">
      <stop stop-color="#2563EB" stop-opacity="0.62"/>
      <stop offset="1" stop-color="#2563EB" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({220 - glow_shift:.1f} 640) rotate(90) scale(160 240)">
      <stop stop-color="#7C3AED" stop-opacity="0.48"/>
      <stop offset="1" stop-color="#7C3AED" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="22" stdDeviation="22" flood-color="#000000" flood-opacity="0.24"/>
    </filter>
    <style>
      .sans {{ font-family: "SF Pro Display","SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; }}
      .chip {{ font-family: "SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 0.08em; }}
      .kicker {{ font-family: "SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 0.18em; }}
      .title {{ font-family: "SF Pro Display","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 58px; font-weight: 800; }}
      .subtitle {{ font-family: "SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 22px; font-weight: 500; }}
      .cardTitle {{ font-family: "SF Pro Display","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 26px; font-weight: 800; }}
      .cardCopy {{ font-family: "SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 16px; font-weight: 600; }}
      .cardSmall {{ font-family: "SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 14px; font-weight: 600; }}
      .metricLabel {{ font-family: "SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 15px; font-weight: 700; fill: #0F172A; }}
      .metricValue {{ font-family: "SF Pro Display","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 15px; font-weight: 800; fill: #0F172A; text-anchor: end; }}
      .platformChip {{ font-family: "SF Pro Text","SFNS","Helvetica Neue",Arial,sans-serif; font-size: 13px; font-weight: 700; }}
    </style>
  </defs>

  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>
  <circle cx="{fmt(980 + glow_shift)}" cy="118" r="210" fill="url(#glowA)"/>
  <circle cx="{fmt(220 - glow_shift)}" cy="640" r="180" fill="url(#glowB)"/>

  <text x="88" y="92" class="kicker" fill="#60A5FA">IP PUBLISHER FLOW</text>
  <text x="88" y="156" class="title" fill="#FFFFFF">Request to publish.</text>
  <text x="88" y="206" class="subtitle" fill="#CBD5E1">Knowledge enters as a structured request, moves through audit,</text>
  <text x="88" y="238" class="subtitle" fill="#CBD5E1">and exits as a publish package with channel-ready payloads.</text>
  {rect(1022, 70, 170, 28, 14, "#0B1220", fill_opacity=0.26)}
  {text(1052, 89, "request -> audit -> publish", "chip", fill="#F8FAFC", opacity=0.92)}

  <path d="M{fmt(req_x + 320)} 358 C {fmt(req_x + 358)} 358, 428 358, {fmt(line1_x2)} 358" stroke="#60A5FA" stroke-opacity="{0.18 + 0.72 * line1_p:.3f}" stroke-width="4" stroke-linecap="round"/>
  <path d="M808 358 C 844 358, 892 358, {fmt(line2_x2)} 358" stroke="#60A5FA" stroke-opacity="{0.18 + 0.72 * line2_p:.3f}" stroke-width="4" stroke-linecap="round"/>

  <g filter="url(#shadow)" opacity="{req_op:.3f}">
    {''.join(request_card)}
  </g>

  <g filter="url(#shadow)" opacity="{aud_op:.3f}">
    {''.join(audit_card)}
  </g>

  <g filter="url(#shadow)" opacity="{pub_op:.3f}">
    {''.join(publish_card)}
    {''.join(platform_nodes)}
  </g>

  {rect(88, 616, 1104, 54, 27, "#FFFFFF", stroke="#BFDBFE", stroke_width=1.2, fill_opacity=0.05 + 0.08 * hold_p, stroke_opacity=0.18 + 0.28 * hold_p)}
  {text(118, 649, "Structured request in. Audited package out.", "cardCopy", fill="#E2E8F0", opacity=0.32 + 0.68 * hold_p)}
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
    png_args = [str(path) for path in png_paths]
    subprocess.run(
        [
            "magick",
            *png_args,
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
    row1 = OUT_DIR / "row1.png"
    row2 = OUT_DIR / "row2.png"
    subprocess.run(
        [
            "magick",
            str(frame_paths[0]),
            "-bordercolor",
            "#F8FAFC",
            "-border",
            "24x24",
            str(frame_paths[1]),
            "-bordercolor",
            "#F8FAFC",
            "-border",
            "24x24",
            "+append",
            str(row1),
        ],
        check=True,
    )
    subprocess.run(
        [
            "magick",
            str(frame_paths[2]),
            "-bordercolor",
            "#F8FAFC",
            "-border",
            "24x24",
            str(frame_paths[3]),
            "-bordercolor",
            "#F8FAFC",
            "-border",
            "24x24",
            "+append",
            str(row2),
        ],
        check=True,
    )
    subprocess.run(
        ["magick", str(row1), str(row2), "-append", str(SHEET_PATH)],
        check=True,
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_paths = render_svg_frames()
    build_gif(png_paths)
    build_sheet([0, 24, 48, 76])
    print(f"GIF: {GIF_PATH}")
    print(f"Sheet: {SHEET_PATH}")


if __name__ == "__main__":
    main()
