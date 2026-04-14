# IP Publisher

<p align="center"><img src="assets/logo.webp" alt="IP Publisher Logo" width="520"></p>

> 面向个人 IP 运营者的全流程 AI 内容自动化工具  
> 从「热点发现」到「多平台发布」，一条命令完成。

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

## 3 分钟跑通（MVP）

### 1) 克隆仓库

```bash
git clone https://github.com/veeicwgy/ip-publisher.git
cd ip-publisher
```

### 2) 安装依赖并初始化配置

```bash
bash scripts/setup.sh
```

### 3) 直接触发主流程

对 Claude Code 或 OpenClaw 说：

```text
帮我写一篇小红书文章
```

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

## License

本项目采用 [MIT License](LICENSE)。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=veeicwgy/ip-publisher&type=Date)](https://star-history.com/#veeicwgy/ip-publisher&Date)
