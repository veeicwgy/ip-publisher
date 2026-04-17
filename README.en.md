# IP Publisher

<p align="right"><a href="./README.md">简体中文</a> | <strong>English</strong></p>

<p align="center"><img src="assets/logo.webp" alt="IP Publisher Logo" width="520"></p>

> An end-to-end AI content workflow for personal brand operators.
> From trend discovery to publish-ready content packs, one command runs the whole pipeline.

<p align="center">
  <a href="https://ippublisher-lwukxvsq.manus.space">Website</a> ·
  <a href="https://github.com/veeicwgy/ip-publisher">GitHub Repository</a> ·
  <a href="./README.md">中文说明</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/veeicwgy/ip-publisher?style=social)](https://github.com/veeicwgy/ip-publisher/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/veeicwgy/ip-publisher?style=social)](https://github.com/veeicwgy/ip-publisher/network/members)

> If this project is useful to you, please consider giving it a **Star**. That helps prioritize API-based auto publishing, more cover templates, and a broader content workflow.

---

## What problem does this project solve?

For individual creators, the slowest part is often not writing itself. It is choosing topics, rewriting for different platforms, reducing the “AI-generated” feel, and preparing covers plus final publishing assets across multiple tools.

**IP Publisher** turns those steps into one executable workflow: `trends -> persona alignment -> platform rewriting -> humanization -> cover generation -> publish-ready output`.

---

## Content Output Example

The image below is a sample of the kind of content output this repository is designed to produce. You only need to provide one intent, and the workflow continues with trend filtering, persona alignment, article generation, humanization, and cover preparation before giving you a publish-ready result.

<p align="center"><img src="assets/one-click-demo.png" alt="IP Publisher content output example" width="980"></p>

---

## Get it running in 3 minutes

### 1) Clone the repository

```bash
git clone https://github.com/veeicwgy/ip-publisher.git
cd ip-publisher
```

### 2) Install dependencies and initialize config

```bash
bash scripts/setup.sh
```

### 3) Trigger the main workflow

Say this to Claude Code or OpenClaw:

```text
Write a Xiaohongshu post for me
```

If you want to see the product presentation first, you can also visit the [IP Publisher website](https://ippublisher-lwukxvsq.manus.space).

---

## What it automates

| Step | Action | Output |
| --- | --- | --- |
| 1 | Load or create your IP persona | Defines profession, tone, audience, and topic boundaries |
| 2 | Fetch live trends | Pulls public topics from Weibo, Zhihu, and 36Kr |
| 3 | Generate a content strategy | Produces title directions, core angles, and emotion targets |
| 4 | Adapt to target platforms | Creates tailored copy for Xiaohongshu, Zhihu, and WeChat |
| 5 | Humanize the writing | Reduces template feel and adds a more personal voice |
| 6 | Generate covers | Uses real AI image generation for cover output |
| 7 | Export publish-ready packs | Delivers copy and status notes ready for manual publishing |

---

## Supported platforms

| Platform | Best for | Cover support |
| --- | --- | --- |
| Xiaohongshu | Emotional storytelling and lifestyle posts | Yes |
| Zhihu | Opinion pieces and long-form answers | Yes |
| WeChat Official Accounts | Narrative long-form articles and brand content | Yes |
| CSDN | Technical tutorials and engineering writeups | Yes |
| Weibo | Short trend commentary and engagement posts | No |
| Toutiao | Trend expansion and broader public topics | Yes |
| Juejin | Technical practice and developer content | Yes |

---

## Five common prompts

```text
Write a Xiaohongshu post about AI trends
Create a WeChat article based on today's hot topics
Set up my personal brand persona
Show me the best trends for my persona today
Generate publish-ready versions for both Zhihu and WeChat
```

---

## Why this repository fits personal brands better

This is not a single-purpose writing helper. It is a complete workflow designed for personal brand operations. The goal is not just to generate one article, but to first align who you are, what you should write, and how each platform should be adapted, then carry that through cover generation and publishing preparation.

---

## Core capabilities and dependencies

| Capability / Dependency | Purpose |
| --- | --- |
| Agent-based search and web extraction | Pulls trending topics directly from Weibo, Zhihu, and 36Kr without extra Python packages |
| Wechatsync | Plugin dependency for multi-platform syncing and publishing; current version still requires user-side cooperation |
| miaoda_image_generate | Real AI cover generation |
| Humanizer-zh | Chinese humanization step to reduce AI tone |

---

## Current status and roadmap

| Area | Current status | Next step |
| --- | --- | --- |
| Trend fetching | Already switched to direct web search and extraction | Add more vertical sources |
| Humanization | Rule-based refinement flow is in place | Add evaluation and feedback loops |
| Cover generation | Upgraded to real image generation | Add more templates and batch generation |
| Publishing delivery | Standardized article and cover outputs for manual publishing | Connect platform APIs for automated publishing later |

---

## License

This project is released under the [MIT License](LICENSE).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=veeicwgy/ip-publisher&type=Date)](https://star-history.com/#veeicwgy/ip-publisher&Date)
