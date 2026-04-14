# IP Publisher

<p align="center"><img src="assets/logo.webp" alt="IP Publisher Logo" width="520"></p>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Star History Chart](https://api.star-history.com/svg?repos=veeicwgy/ip-publisher&type=Date)](https://star-history.com/#veeicwgy/ip-publisher&Date)

> **一句话简介 / One-line Pitch**  
> 全流程个人 IP 内容自动化工具，从热点到发布，一句话搞定。  
> End-to-end AI content automation for personal brands, from trend discovery to multi-platform publishing in one command.

## 项目简介 | Overview

**IP Publisher** 是一个面向个人 IP 运营者的开源 Skill 仓库。它把“人设定义、热点抓取、内容生成、去 AI 味处理、封面生成、多平台发布”串成一个可执行的工作流，让内容生产从零散的提示词操作变成稳定、可复用的自动化链路。

**IP Publisher** is an open-source skill collection for personal brand operators. It turns fragmented prompting into a reusable workflow that discovers trends, generates platform-native copy, removes AI patterns, creates cover assets, and publishes across channels.

## 核心功能模块 | Core Modules

| 模块 | 功能说明 | 来源仓库 | 在本项目中的职责 |
| --- | --- | --- | --- |
| IP Profile | 定义 IP 人设、语气、禁忌话题与常用平台 | `ip-publisher` | 作为全流程输入源，统一内容风格 |
| Hotspot Fetcher | 抓取微博、知乎、头条、36氪、微信热文热点 | [wewrite](https://github.com/oaker-io/wewrite) | 提供热点发现与领域过滤能力 |
| Article Generator | 根据平台规范生成完整文章 | `ip-publisher` | 承接人设与热点，输出平台定制文案 |
| Humanizer | 去掉套话、平衡句式、注入个人语气 | [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 降低 AI 痕迹，增强真人表达感 |
| Cover Generator | 根据标题与平台生成封面图提示与调用参数 | [baoyu-skills](https://github.com/jimliu/baoyu-skills) | 输出平台适配封面生成任务 |
| Multi Publisher | 将文章与封面推送到多个平台 | [Wechatsync](https://github.com/wechatsync/Wechatsync) | 负责草稿或直发模式发布 |

## 快速开始 | Quick Start

### Step 1. 克隆仓库

```bash
git clone https://github.com/veeicwgy/ip-publisher.git
cd ip-publisher
```

### Step 2. 运行安装脚本

```bash
bash scripts/setup.sh
```

### Step 3. 触发 Skill

对 Claude Code 或 OpenClaw 说：

```text
帮我写一篇小红书文章
```

## 支持平台 | Supported Platforms

| 平台 | 内容形态 | 封面支持 | 典型用途 |
| --- | --- | --- | --- |
| 小红书 | 短内容、图文种草 | 是 | 情绪化表达、经验分享、互动种草 |
| 知乎 | 长文回答、观点分析 | 是 | 深度观点、论证型内容 |
| 微信公众号 | 长文图文 | 是 | 个人品牌沉淀、故事化表达 |
| CSDN | 技术长文、教程 | 是 | 技术复盘、教程、工具链分享 |
| 微博 | 短文本 | 否 | 热点跟进、观点短评 |
| 今日头条 | 中长文 | 是 | 大众议题、热点扩写 |
| 掘金 | 技术文章 | 是 | 工程实践、实操总结 |

## Skill 触发示例 | Trigger Examples

| 中文示例 | 说明 |
| --- | --- |
| 帮我写一篇关于 AI 趋势的小红书文章 | 自动加载人设、抓热点、生成内容 |
| 基于今天的热点写一篇公众号推文 | 自动从热点池选题并输出长文 |
| 设置我的 IP 人设 | 启动人设配置向导并保存到本地 |
| 给我看看今天有哪些适合我的热点 | 仅执行热点抓取与筛选 |
| 一键发布到知乎和公众号 | 进入多平台发布流程 |

## 工作流程图 | Workflow

```text
[User Request]
      |
      v
[IP Profile Loader] ----> ~/.ip-publisher/profile.yaml
      |
      v
[Hotspot Fetcher] ----> Top 5 relevant topics
      |
      v
[Strategy Builder] ----> Title directions / core观点 / 情绪目标
      |
      v
[Article Generator] ----> Platform-native draft
      |
      v
[Humanizer] ----> 去 AI 味 + 注入个性语气
      |
      v
[Cover Generator] ----> Platform-fit cover options
      |
      v
[Multi Publisher] ----> Xiaohongshu / Zhihu / WeChat / CSDN / Weibo / Toutiao / Juejin
```

## 集成开源项目致谢 | Acknowledgements

| 项目 | 用途 |
| --- | --- |
| [wewrite](https://github.com/oaker-io/wewrite) | 热点抓取与信息聚合 |
| [Wechatsync](https://github.com/wechatsync/Wechatsync) | 多平台内容同步与发布 |
| [baoyu-skills](https://github.com/jimliu/baoyu-skills) | 封面图 Skill 能力参考 |
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 中文文本去 AI 味处理 |

## 遗留问题与路线图 | Known Gaps and Roadmap

| 方向 | 当前状态 | 后续规划 |
| --- | --- | --- |
| 平台接口稳定性 | 依赖上游适配器版本 | 补充版本锁定与回归测试 |
| 封面生成闭环 | 当前以 Skill 编排为主 | 增加本地模板与批处理脚本 |
| 热点筛选精度 | 依赖领域关键词匹配 | 引入更细的人设标签体系 |
| 去 AI 味质量评估 | 主要依赖规则与 LLM 判断 | 增加自动对比与人工反馈回路 |
| 发布报告 | 已提供基础状态汇总 | 增加失败重试与平台日志归档 |

## License

本项目采用 [MIT License](./LICENSE)。  
This project is released under the [MIT License](./LICENSE).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=veeicwgy/ip-publisher&type=Date)](https://star-history.com/#veeicwgy/ip-publisher&Date)
