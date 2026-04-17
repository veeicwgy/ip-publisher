---
name: ip-publisher-suite
description: IP Publisher 总入口说明。Use for: 安装、理解和调度个人 IP 内容工作流技能集合，包括人设、热点筛选、平台写作、去 AI 味、封面 brief、多平台发布包生成与官网开源导向改版。
---

# IP Publisher Skill Suite

## Use when

- 需要理解整个仓库由哪些 Skill 组成
- 需要安装 Claude Code 或 OpenClaw 可识别的 Skill 集合
- 需要查看完整工作流、脚本与配置文件关系
- 需要把产品官网从收费导向改为 GitHub 开源仓库导向

## Included Skills

| Skill | 职责 | 关键输入 | 关键输出 |
| --- | --- | --- | --- |
| `ip-publisher` | 编排完整内容工作流 | 平台、话题、用户目标 | 草稿、封面 brief、发布包准备结果 |
| `ip-profile` | 管理人设 | 职业、风格、受众 | `~/.ip-publisher/profile.yaml` |
| `hotspot-fetcher` | 抓取并筛选公开热点 | 人设领域、时间窗口 | Top 热点列表 |
| `article-generator` | 生成平台文案 | 人设、热点、平台 | 文章草稿 |
| `humanizer` | 去 AI 味 | 草稿、人设语气 | 人性化文章 |
| `cover-generator` | 生成封面任务 | 标题、平台、风格 | 封面方案或图片 |
| `multi-publisher` | 生成多平台发布包并做预检 | 文章、封面、平台列表 | 平台差异化发布内容与检查结果 |
| `github-open-source-site-rework` | 维护官网的开源获取导向 | 当前官网页面、试用提示、GitHub 仓库地址 | 改版后的官网文案与校验清单 |

## What is real in this repository

- `scripts/setup.sh` 可以真实完成依赖拉取、Skill 安装和本地人设初始化。
- `scripts/generate-publish-pack.py` 可以真实读取 `config/platforms.yaml` 并生成 Markdown / JSON 发布包。
- `examples/` 提供了可直接查看的输出样例。
- 当前默认交付是**发布准备结果**，不是伪装成“已经自动发到所有平台”的成功状态。

## Default workflow

1. 读取 `~/.ip-publisher/profile.yaml`。
2. 当用户没有明确话题时，先抓取热点并筛选 Top 5。
3. 生成标题方向、核心观点与情绪目标。
4. 根据目标平台输出适配内容。
5. 对草稿执行去 AI 味处理。
6. 生成封面方案。
7. 生成发布包或执行用户已明确授权的发布动作，并汇总真实状态。

## Required local files

- `~/.ip-publisher/profile.yaml`：用户人设配置
- `config/platforms.yaml`：平台规范配置
- `config/hotspot-sources.yaml`：热点来源配置

## Installation hint

运行 `bash scripts/setup.sh` 完成依赖拉取、Skill 安装和人设初始化；若只想验证仓库里的真实脚本，可继续运行 `python3 scripts/generate-publish-pack.py --platform xiaohongshu --title "测试标题" --body "测试正文"`。
