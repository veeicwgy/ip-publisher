---
name: ip-publisher-suite
description: IP Publisher 仓库总入口。Use for: 理解“小红书、公众号、知乎三平台改写 + 发布包整理”相关 skills、companion repo 资源与安装边界。
---

# IP Publisher Skill Suite

## Use when

- 需要理解整个仓库由哪些 skills、reference 文件与 companion repo 资源组成
- 需要把一个话题改写成小红书、公众号、知乎三个版本，并整理成发布包
- 需要区分“已发布 skill 默认能力”和“仓库额外脚本/配置”的边界

## Included skills

| Skill | 默认职责 | 默认边界 |
| --- | --- | --- |
| `ip-publisher` | 生成 Xiaohongshu / WeChat / Zhihu 三个平台版本并整理发布包 | 默认只输出对话内结果 |
| `ip-profile` | 整理结构化人设 YAML | 默认不自动保存本地文件 |
| `multi-publisher` | 整理多平台可复制发布内容与预发布检查 | 默认不自动发布 |

## Companion repo resources

仓库根目录下还可能存在 `scripts/`、`config/`、`examples/` 等资源，但这些内容应被视为 **companion repo resources**，而不是每个已发布 skill 自动自带的安装资产。只有在用户明确处于仓库模式、并且主动要求使用这些资源时，才讨论它们的调用方式。

## Default rule

解释能力时，优先使用“当前已发布 skill 默认能做什么”这条口径。不要把 companion repo 里的脚本、本地路径或外部发布工具，写成所有安装场景下都自动成立的默认能力。
