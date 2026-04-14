---
name: ip-publisher-suite
description: IP Publisher 总入口说明。Use for: 安装、理解和调度个人 IP 内容自动化技能集合，包括人设、热点、写作、去 AI 味、封面和多平台发布。
---

# IP Publisher Skill Suite

## Use when

- 需要理解整个仓库由哪些 Skill 组成
- 需要安装 Claude Code 或 OpenClaw 可识别的 Skill 集合
- 需要查看完整工作流与配置文件关系

## Included Skills

| Skill | 职责 | 关键输入 | 关键输出 |
| --- | --- | --- | --- |
| `ip-publisher` | 编排全流程 | 平台、话题、用户目标 | 完整发布报告 |
| `ip-profile` | 管理人设 | 职业、风格、受众 | `~/.ip-publisher/profile.yaml` |
| `hotspot-fetcher` | 抓取热点 | 人设领域、时间窗口 | Top 热点列表 |
| `article-generator` | 生成平台文案 | 人设、热点、平台 | 文章草稿 |
| `humanizer` | 去 AI 味 | 草稿、人设语气 | 人性化文章 |
| `cover-generator` | 生成封面任务 | 标题、平台、风格 | 封面方案 |
| `multi-publisher` | 多平台发布 | 文章、封面、平台列表 | 状态报告 |

## Default Workflow

1. 读取 `~/.ip-publisher/profile.yaml`。
2. 当用户没有明确话题时，先抓取热点并筛选 Top 5。
3. 生成标题方向、核心观点与情绪目标。
4. 根据目标平台输出适配内容。
5. 对草稿执行去 AI 味处理。
6. 生成封面方案。
7. 推送到目标平台并汇总状态。

## Required Local Files

- `~/.ip-publisher/profile.yaml`：用户人设配置
- `config/platforms.yaml`：平台规范配置
- `config/hotspot-sources.yaml`：热点来源配置

## Installation Hint

运行 `bash scripts/setup.sh` 完成依赖拉取、Skill 安装和人设初始化。
