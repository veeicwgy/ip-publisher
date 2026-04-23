---
name: ip-publisher-suite
description: 知识库驱动的多平台内容生成与发布包准备。基于用户提供的知识来源、关键词和大纲，生成主稿、7 平台适配版本和发布说明包，默认在审核通过后交付对话内结果，用户可随时执行发布。
---

# IP Publisher Suite — 根路由

> 本文件是项目根路由入口。Skill 逻辑、边界定义和参考文件均在 `skills/ip-publisher/` 目录下。

## 快速导航

| 文件 | 说明 |
|---|---|
| [`skills/ip-publisher/SKILL.md`](./skills/ip-publisher/SKILL.md) | **主 Skill 定义**：能力边界、触发条件、核心流程、发布模式 |
| [`skills/ip-publisher/references/input-checklist.md`](./skills/ip-publisher/references/input-checklist.md) | 输入项清单与提问规则 |
| [`skills/ip-publisher/references/output-contract.md`](./skills/ip-publisher/references/output-contract.md) | 输出契约与禁止声明 |
| [`skills/ip-publisher/references/package-boundary.md`](./skills/ip-publisher/references/package-boundary.md) | Skill 包资产边界 |
| [`skills/ip-publisher/references/platform-specs.md`](./skills/ip-publisher/references/platform-specs.md) | 7 平台格式规格 |
| [`docs/wechatsync-runbook.md`](./docs/wechatsync-runbook.md) | 仓库模式完整操作手册（CLI、Token、发布命令） |

## 一句话说明

- **ClawHub 安装者**：读 `skills/ip-publisher/SKILL.md`，对话内交付发布包，不执行发布。
- **仓库使用者**：读 `docs/wechatsync-runbook.md`，本地 CLI + Wechatsync 执行发布。
