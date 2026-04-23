# IP Publisher

<p align="right"><a href="./README.md">简体中文</a> | <strong>English</strong></p>

<p align="center"><img src="assets/logo.webp" alt="IP Publisher Logo" width="520"></p>

<p align="center">
  <a href="https://github.com/veeicwgy/ip-publisher/stargazers"><img src="https://img.shields.io/github/stars/veeicwgy/ip-publisher?style=flat-square" alt="GitHub stars"></a>
  <a href="https://github.com/veeicwgy/ip-publisher/releases"><img src="https://img.shields.io/github/v/release/veeicwgy/ip-publisher?style=flat-square" alt="GitHub release"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/veeicwgy/ip-publisher?style=flat-square" alt="MIT License"></a>
  <a href="https://clawhub.ai/veeicwgy/ip-publisher"><img src="https://img.shields.io/badge/Install-ClawHub-111827?style=flat-square" alt="Install from ClawHub"></a>
</p>

> Turn product documentation, knowledge-base facts, SEO keywords, trend hooks, and an outline into **audited articles + 7-platform publish packs** before any publishing step.

<p align="center">
  <a href="https://clawhub.ai/veeicwgy/ip-publisher"><strong>👉 Install from ClawHub</strong></a> ·
  <a href="./data/tasks/demo-request.json">Demo Request</a> ·
  <a href="./data/kb_raw/mineru-overview.md">Demo KB</a> ·
  <a href="./docs/platform-support.md">Platform Matrix</a> ·
  <a href="./docs/publish-package.md">Publish Package Contract</a>
</p>

## 30-second overview

| You provide | The workflow does | You get back |
| --- | --- | --- |
| Product/tool KB docs, primary keywords, trend hooks, outline brief, audience | Generates from the KB, audits grounding/keyword fit/structure/platform rules, then adapts the same core piece into 7 platform payloads | `article.md`, `audit_report.json`, `publish_package.json`, and `platforms/*.md` |

<table>
  <tr>
    <td width="50%" align="center"><img src="./assets/readme/inputs-overview.svg" alt="Inputs overview" width="100%"></td>
    <td width="50%" align="center"><img src="./assets/readme/outputs-overview.svg" alt="Outputs overview" width="100%"></td>
  </tr>
  <tr>
    <td align="center"><strong>Inputs</strong><br>KB docs, keywords, trend hooks, and outline brief</td>
    <td align="center"><strong>Outputs</strong><br>Draft, publish package, and platform files</td>
  </tr>
  <tr>
    <td width="50%" align="center"><img src="./assets/readme/audit-report-overview.svg" alt="Audit report overview" width="100%"></td>
    <td width="50%" align="center"><img src="./assets/readme/platforms-overview.svg" alt="7 platform payload overview" width="100%"></td>
  </tr>
  <tr>
    <td align="center"><strong>Audit report</strong><br>Grounding, keyword fit, structure, and platform gates</td>
    <td align="center"><strong>7 platform payloads</strong><br>One source topic adapted into the canonical bundle</td>
  </tr>
</table>

```text
outputs/<task_id>/
  article.md
  audit_report.json
  publish_package.json
  platforms/
    wechat_official.md
    xiaohongshu.md
    zhihu.md
    juejin.md
    csdn.md
    toutiao.md
    weibo.md
```

## Why this is not just another AI rewriter

- It starts from a **knowledge base**, not an empty prompt.
- It runs an **audit gate** before packaging content for distribution.
- It defaults to a **canonical 7-platform bundle**, not an inconsistent 3-platform vs. 29-platform story.
- It is **draft-sync first** through [Wechatsync](https://github.com/wechatsync/Wechatsync), not a username/password autopublisher.
- For technical content it explicitly optimizes for `Q&A`, comparison tables, clear heading hierarchy, entity labels, and reproducible code examples.

## Who this is for

- Product, SEO, and knowledge-base content teams
- Operators who need one source topic adapted into WeChat, Xiaohongshu, Zhihu, Juejin, CSDN, Toutiao, and Weibo
- Teams that want accuracy and auditability before adding publishing automation

## What it does now

IP Publisher now centers on one production path:

1. Retrieve facts from a product/tool knowledge base
2. Combine them with SEO keywords, trend hooks, and an outline brief
3. Generate an AI-friendly article structure
4. Audit grounding, keyword coverage, structure quality, fact density, and platform limits
5. Export 7 platform payloads plus a publish package and Wechatsync draft-sync metadata

The default canonical bundle is:

- `wechat_official`
- `xiaohongshu`
- `zhihu`
- `juejin`
- `csdn`
- `toutiao`
- `weibo`

## Quick start

```bash
git clone https://github.com/veeicwgy/ip-publisher.git
cd ip-publisher
bash scripts/setup.sh
python3 scripts/quickstart.py
```

The new quickstart asks for:

- product/tool name
- primary keywords
- trend/topic hook
- outline brief
- target audience
- content type (`general` or `technical`)

It no longer asks “which platform?” as the main question. One topic now defaults to the 7-platform bundle.

Useful demo inputs:

- [Demo KB overview](./data/kb_raw/mineru-overview.md)
- [Demo KB FAQ](./data/kb_raw/mineru-faq.json)
- [Demo request](./data/tasks/demo-request.json)

## Outputs

After a run you will get:

- `request.json`
- `draft.json`
- `audit_report.json`
- `publish_package.json`
- `article.md`
- `platforms/*.md`

## Direct publishing stance

This repo does not do username/password login automation.

The recommended publishing bridge is [Wechatsync](https://github.com/wechatsync/Wechatsync):

- browser-login based
- draft-first
- same web APIs as the platform editors
- only after `audit_report.status == pass`

## Humanizer

The repo now includes a lightweight built-in humanizer step inspired by [Humanizer-zh](https://github.com/op7418/Humanizer-zh). It focuses on reducing template-like AI phrasing while preserving facts.

## Docs

- [Platform matrix](./docs/platform-support.md)
- [Publish package contract](./docs/publish-package.md)
- [Phase 1 scaffold](./docs/phase1-scaffold.md)

## License

MIT
