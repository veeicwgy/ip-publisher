# IP Publisher

<p align="center"><img src="assets/logo.webp" alt="IP Publisher Logo" width="520"></p>

> 面向个人 IP 运营者的开源内容自动化工作流  
> 从「热点发现」到「多平台发布」，一条命令跑通。

[GitHub 仓库](https://github.com/veeicwgy/ip-publisher) | [3 分钟跑通](#3-分钟跑通推荐) | [稳定版本 v0.1.0](https://github.com/veeicwgy/ip-publisher/releases/tag/v0.1.0)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 这个项目解决什么问题

个人创作者做内容，最耗时间的不是“写字”，而是：

- 选题慢：每天不知道写什么
- 多平台改写重复劳动：小红书、知乎、公众号风格不同
- AI 味重：读起来像模板
- 发布链路碎片化：封面、正文、分发各一套工具

**IP Publisher** 把这些步骤串成一个可执行工作流：  
`热点 -> 人设对齐 -> 平台改写 -> 去 AI 味 -> 封面生成 -> 多平台发布`

---

## 3 分钟跑通（推荐）

### 1) 前置依赖

| 依赖项 | 最低要求 | 用途 |
| --- | --- | --- |
| Git | 可执行 `git --version` | 克隆仓库与拉取依赖 |
| Python 3 | 可执行 `python3 --version` | 运行安装与辅助脚本 |
| pip | 可执行 `pip --version` 或 `pip3 --version` | 安装脚本依赖 |
| Bash | macOS / Linux 自带，Windows 建议使用 WSL | 执行 `scripts/setup.sh` |
| Claude Code / OpenClaw | 已正确安装 | 加载仓库 Skills 并触发主流程 |

### 2) 网络要求

首次安装会拉取依赖仓库并复制 Skills，请确保当前网络可以访问 GitHub，且终端没有被错误代理或公司网络策略拦截。

### 3) 克隆仓库

```bash
git clone https://github.com/veeicwgy/ip-publisher.git
cd ip-publisher
```

### 4) 安装依赖并初始化配置

```bash
bash scripts/setup.sh
```

### 5) 触发首条指令

对 Claude Code 或 OpenClaw 说：

```text
帮我写一篇小红书文章
```

### 成功跑通后你会看到什么

| 验收点 | 成功标准 |
| --- | --- |
| 人设文件 | 本地生成 `~/.ip-publisher/profile.yaml` |
| 依赖目录 | 本地生成 `~/.ip-publisher/deps/`，并能看到拉取下来的依赖仓库 |
| Skills 安装 | 至少一个目录出现 `ip-publisher` 相关技能：`~/.claude/skills/`、`~/.config/claude/skills/` 或 `~/.openclaw/skills/` |
| 首次触发 | 输入首条指令后，Agent 能开始读取人设并进入内容生成流程 |

如果以上四项都满足，说明安装已基本成功。

---

## 5 个常见问题与快速修复

| 问题 | 常见表现 | 快速修复 |
| --- | --- | --- |
| 权限问题 | 提示 `Permission denied` 或脚本无法执行 | 不要直接双击脚本，请在仓库根目录运行 `bash scripts/setup.sh` |
| GitHub 拉取失败 | 依赖仓库克隆超时、连接被拒绝 | 检查代理设置、网络连通性，必要时切换网络后重试 |
| Python / pip 缺失 | 安装阶段提示找不到 `python3` 或 `pip` | 先安装 Python 3 与 pip，再重新运行 setup 脚本 |
| Skill 未加载 | 安装完成后 Claude Code / OpenClaw 无法识别相关 Skill | 确认 `~/.claude/skills/`、`~/.config/claude/skills/` 或 `~/.openclaw/skills/` 下已生成对应目录，并重启客户端 |
| 平台授权失败 | 触发发布或登录能力时报授权错误 | 先完成所需平台登录/授权，再重试对应发布动作 |

---

## 当前稳定版本

当前建议从 **v0.1.0** 开始体验。这个版本重点确保三件事：

| 版本能力 | 说明 |
| --- | --- |
| Quick Start 可跑通 | README 与安装脚本围绕首次成功率进行了整理 |
| 开源入口一致 | 官网、仓库与 Skill 的导向统一收敛到 GitHub 开源仓库 |
| 运维 Skill 可复用 | 仓库附带官网开源导向改版 Skill，可直接复用维护官网 |

查看版本说明：<https://github.com/veeicwgy/ip-publisher/releases/tag/v0.1.0>

---

## 它会自动完成什么

| 步骤 | 动作 | 结果 |
| --- | --- | --- |
| 1 | 加载或创建 IP 人设 | 明确职业、风格、受众、禁忌话题 |
| 2 | 抓取实时热点 | 返回与你领域相关的话题候选 |
| 3 | 生成内容策略 | 输出标题方向、核心观点、情绪目标 |
| 4 | 适配目标平台 | 生成小红书、知乎、公众号等平台文案 |
| 5 | 去 AI 味处理 | 减少模板感，注入个人表达风格 |
| 6 | 生成封面 | 输出平台匹配的封面方案 |
| 7 | 多平台发布 | 推送到目标平台并生成状态报告 |

---

## 支持哪些平台

| 平台 | 适合内容 | 是否支持封面 |
| --- | --- | --- |
| 小红书 | 情绪化表达、图文种草 | 是 |
| 知乎 | 观点分析、长文回答 | 是 |
| 微信公众号 | 叙事型长文、品牌沉淀 | 是 |
| CSDN | 技术教程、复盘文章 | 是 |
| 微博 | 热点短评、互动表达 | 否 |
| 今日头条 | 热点扩写、大众议题 | 是 |
| 掘金 | 技术实操、工程总结 | 是 |

---

## 5 个常用触发词

```text
帮我写一篇关于 AI 趋势的小红书文章
基于今天的热点写一篇公众号推文
设置我的 IP 人设
给我看看今天适合我的热点
一键发布到知乎和公众号
```

---

## 为什么这个仓库更适合个人 IP

它不是单点写作工具，而是一条围绕个人 IP 运营设计的完整链路。核心思路不是“生成一篇文章”，而是先对齐你是谁、适合写什么、平台应该怎么改，再把最后一步的分发也串起来。

---

## 集成的开源项目

| 项目 | 作用 |
| --- | --- |
| [wewrite](https://github.com/oaker-io/wewrite) | 热点抓取与信息聚合 |
| [Wechatsync](https://github.com/wechatsync/Wechatsync) | 多平台同步与发布 |
| [baoyu-skills](https://github.com/jimliu/baoyu-skills) | 封面生成能力参考 |
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 中文去 AI 味处理 |

---

## 当前状态与后续计划

| 方向 | 当前状态 | 后续计划 |
| --- | --- | --- |
| 平台适配 | 已覆盖主流中文内容平台 | 补充更多平台适配器 |
| 去 AI 味 | 已有规则化处理流程 | 增加效果评估与反馈回路 |
| 封面生成 | 已接入封面生成步骤 | 增加更多模板与批量生成能力 |
| 发布报告 | 已输出基础状态报告 | 增加失败重试与日志归档 |

---

## 仓库附带的运维 Skill

除了内容生产主流程，这个仓库现在也附带一个用于维护官网开源导向的 Skill：

| Skill | 用途 | 位置 |
| --- | --- | --- |
| `github-open-source-site-rework` | 当官网需要从收费、升级或价格导向改为 GitHub 开源仓库导向时，统一处理 CTA、试用提示、残留文案、回归测试与交付清单。 | `skills/github-open-source-site-rework/SKILL.md` |

如果你在维护官网或产品落地页，希望所有引导都与本仓库的开源定位保持一致，可以直接复用这个 Skill。

---

## License

本项目采用 [MIT License](LICENSE)。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=veeicwgy/ip-publisher&type=Date)](https://star-history.com/#veeicwgy/ip-publisher&Date)
