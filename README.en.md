# IP Publisher — AI Content Workflow for Personal Brands

<p align="right"><a href="./README.md">简体中文</a> | <strong>English</strong></p>

<p align="center"><img src="assets/logo.webp" alt="IP Publisher Logo" width="520"></p>

> A repository for creators who need a repeatable **AI content workflow**.
> Its current value is not "one-click publishing". Its current value is helping you turn one idea into a cleaner **publish pack** with persona context, platform adaptation, and manual-review-ready output.

<p align="center">
  <a href="https://ippublisher-lwukxvsq.manus.space">Website</a> ·
  <a href="https://github.com/veeicwgy/ip-publisher">GitHub Repository</a> ·
  <a href="./README.md">中文说明</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/veeicwgy/ip-publisher?style=social)](https://github.com/veeicwgy/ip-publisher/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/veeicwgy/ip-publisher?style=social)](https://github.com/veeicwgy/ip-publisher/network/members)

> If this project is useful, please give it a **Star**. I would rather spend the next iteration making the workflow more verifiable than adding bigger claims that still cannot be checked.

---

## Why I built this repository

When I work on personal-brand content, the hardest part is rarely typing the draft itself. The real friction is choosing a usable angle, keeping the voice aligned with the persona, rewriting the same idea for different channels, removing the generic AI tone, and packaging everything for the final publishing step.

That is why I narrowed the positioning of **IP Publisher**. This repository is a **creator workflow system** first, and a publishing helper second. If you need a tool that promises to log into every platform and publish automatically, this version is not that. If you need a workflow that helps you prepare cleaner drafts, platform-specific variants, and structured publish packs that you or your team can review and post manually, it is already useful.

---

## What is actually runnable today

| Deliverable | What it does now | File |
| --- | --- | --- |
| Setup script | Pulls dependencies, initializes local persona config, installs skills for Claude / OpenClaw | `scripts/setup.sh` |
| Publish-pack generator | Reads `config/platforms.yaml` and exports Markdown / JSON packs for multiple platforms | `scripts/generate-publish-pack.py` |
| Platform rules | Stores real limits such as content length, cover ratio, and recommended tag count | `config/platforms.yaml` |
| Persona template | Defines the local `profile.yaml` structure | `config/ip-profile-template.yaml` |
| Example outputs | Shows realistic long-form and short-form content examples | `examples/` |

---

## How I use it in practice

My own workflow is simple. I keep a local persona file, run the main skill to narrow the angle, generate a draft, reduce the template feel, and prepare a cover direction. I do **not** ask the tool to fake a successful publish event. At the last step, I use the publish-pack generator to turn the draft into platform-ready title, body, tag, and checklist bundles, then I review and paste them into the actual publishing backends myself.

That change matters. It moves the project away from pseudo-automation and toward a workflow that a solo creator or a small content team can repeat without guessing what the next step should be. The files in `examples/article-output-wechat.md`, `examples/article-output-xiaohongshu.md`, and `examples/article-output-zhihu.md` reflect that operating style.

---

## Output example

The image below reflects the kind of result this repository is trying to produce today: not a fake "published successfully" screen, but a structured content workflow and a reviewable output set.

<p align="center"><img src="assets/one-click-demo.png" alt="IP Publisher content workflow output example" width="980"></p>

---

## Get it running in about 3 minutes

### 1) Clone the repository

```bash
git clone https://github.com/veeicwgy/ip-publisher.git
cd ip-publisher
```

### 2) Install dependencies and initialize persona config

```bash
bash scripts/setup.sh
```

### 3) Generate a real publish pack

```bash
python3 scripts/generate-publish-pack.py \
  --platform xiaohongshu wechat_official zhihu \
  --title "Why I fixed the content workflow before chasing bigger automation" \
  --angle "A personal brand needs a stable content system before it needs bigger automation" \
  --body-file examples/article-output-wechat.md \
  --tags personal-brand,content-workflow,multi-platform
```

This command creates both a Markdown pack and a JSON manifest under `outputs/`, so you can review the copy, compare platform checks, and continue with your own manual publishing flow.

If you want to inspect the product shape first, visit the [IP Publisher website](https://ippublisher-lwukxvsq.manus.space).

---

## Best-fit use cases

| Use case | Why it fits |
| --- | --- |
| Personal branding | Keep persona, positioning, and output structure consistent |
| Social media publishing preparation | Turn one source draft into platform-specific publish packs |
| Content repurposing | Reuse the same idea across short-form and long-form channels |
| Small creator teams | Hand structured output to editors or operators for final review |

---

## Current capability boundaries

| Module | Current state | Notes |
| --- | --- | --- |
| Trend discovery | Available through skill orchestration and public web sourcing | Not yet a standalone repository script |
| Platform adaptation | Available through the main workflow skill | Depends on Claude / OpenClaw execution |
| Humanization | Available through the `humanizer` sub-skill | Still workflow-oriented rather than a separate engine |
| Cover generation | Can output cover briefs and use image generation when the runtime supports it | Environment-dependent |
| Multi-platform publishing | Exports publish packs and preflight checks by default | Does not fake automatic posting |
| Fully automatic posting | Not implemented | Should only be claimed after real API or plugin execution exists |

---

## Supported platforms

| Platform | Best for | Cover ratio | Recommended tags |
| --- | --- | --- | --- |
| Xiaohongshu | Story-led creator posts and recommendation notes | `1:1` | 8 |
| Zhihu | Opinion pieces and long-form answers | `16:9` | 5 |
| WeChat Official Account | Narrative long-form brand articles | `2.35:1` | 0 |
| CSDN | Technical tutorials and engineering writeups | `16:9` | 6 |
| Weibo | Short reactions and trend commentary | `none` | 2 |
| Toutiao | Broad-interest trend expansion | `16:9` | 5 |
| Juejin | Developer education and technical practice | `16:9` | 5 |

---

## More honest prompts

```text
Find a topic that fits my persona, then draft a WeChat article
Turn this source draft into Xiaohongshu and Zhihu versions
Reduce the generic AI tone and give me a cover brief
Generate a multi-platform publish pack for manual review, not direct posting
```

---

## Repository structure

```text
config/      Platform rules, persona template, hotspot sources
examples/    Real sample outputs
scripts/     Setup, dependency install, publish-pack generator
skills/      Main workflow and sub-skill orchestration
assets/      README visuals
```

---

## License

This project is released under the [MIT License](LICENSE).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=veeicwgy/ip-publisher&type=Date)](https://star-history.com/#veeicwgy/ip-publisher&Date)
