# IP Publisher

<p align="right"><a href="./README.md">简体中文</a> | <strong>English</strong></p>

<p align="center"><img src="assets/logo.webp" alt="IP Publisher Logo" width="520"></p>

> A KB-driven content workflow for teams that need **generation + audit + 7-platform publish packs** before any publishing step.

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
