---
name: ip-publisher-suite
description: 知识库驱动的多平台内容生成与发布包准备。基于用户提供的知识来源、关键词和大纲，生成主稿、7 平台适配版本和发布说明包，默认在审核通过后交付对话内结果，不自动执行发布。
---

# IP Publisher Suite

## 能力边界

本 Skill 负责：

1. 根据用户提供的知识来源、关键词和大纲，生成 AI 友好主稿
2. 将主稿适配为 7 个平台的差异化版本（微信公众号、小红书、知乎、掘金、CSDN、头条号、微博）
3. 整理封面 brief、标签建议和平台发布说明
4. 输出一份**可人工审阅、可复制的发布包**，在对话内交付

**默认停在审核通过后的发布包，不自动执行任何发布动作。**

## 触发条件

- 用户说"基于知识库生成文章"
- 用户说"给我一份多平台发布包"
- 用户说"帮我写文章，先审核再发布"
- 用户说"同一主题出 7 个平台版本"

## 核心流程

```
1. 确认知识来源与输入项（见 references/input-checklist.md）
         ↓
2. 基于知识来源生成主稿
         ↓
3. 审核（必须通过才能继续）
         ↓
4. 适配 7 平台版本（见 references/platform-specs.md）
         ↓
5. 输出发布包 ← 默认终点
```

## 前置闸门：审核通过是硬性条件

- 审核未通过 → 不输出发布包，不进入任何发布流程
- 审核通过 → 输出完整发布包，等待用户确认
- 用户确认后 → 进入发布（见下方「发布模式」）

## 输入要求

必须由用户提供，不自动填充：

- **知识来源**：产品文档、官网说明、已有文章等
- **主题 / 产品名**
- **主关键词**

详见 [`references/input-checklist.md`](./references/input-checklist.md)

## 默认行为约束

- **不读取本地文件**，不写入 `outputs/`，不构建 `request.json`
- **不执行 CLI 命令**，不调用仓库脚本
- **不自动抓取热点**代替知识库素材
- **不代管**账号、Cookie、Token 或密码
- **对话内输出结果**，不声称已发布或已保存

## 发布模式

### ClawHub 安装者（默认）

发布包在对话内交付，用户自行复制到各平台。Wechatsync 同步说明作为可选附注提供，不主动执行。

### 仓库使用者（Companion Repo Mode）

如果用户明确要求使用本地仓库脚本和 Wechatsync CLI 执行发布，进入 Companion Repo Mode：

→ 详细操作步骤见 [`docs/wechatsync-runbook.md`](../../docs/wechatsync-runbook.md)

进入此模式前需用户明确确认：已克隆仓库、已配置环境、已安装 Wechatsync 扩展并提供 Token。

## 参考文件

| 文件 | 用途 |
|---|---|
| `references/input-checklist.md` | 输入项清单与提问规则 |
| `references/output-contract.md` | 输出契约与禁止声明 |
| `references/package-boundary.md` | Skill 包资产边界说明 |
| `references/platform-specs.md` | 7 平台格式规格 |
| `docs/wechatsync-runbook.md` | 仓库模式完整操作手册 |
