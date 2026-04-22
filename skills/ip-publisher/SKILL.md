---
name: ip-publisher
description: Knowledge base article generation + publish pack for WeChat, Xiaohongshu, Zhihu, Juejin, CSDN, Toutiao, and Weibo. 基于知识库、SEO 关键词、热点和大纲生成可审核内容，并附 Wechatsync 草稿同步说明。
---

# IP Publisher

## Use this skill when the user wants KB-driven article generation with a multi-platform publish pack

当用户想基于**知识库 + 关键词 + 热点 + 大纲**做 **knowledge base article generation**，并整理成一份**可审阅、可复制、可继续人工发布的 publish pack** 时，使用本 Skill。默认平台 bundle 是 7 个：微信公众号、小红书、知乎、掘金、CSDN、头条号、微博。

## What this published package includes

当前已发布的 skill 包默认聚焦于四件事：确认知识来源与关键词、生成 AI 友好结构主稿、整理 7 平台差异化 payload、输出一份可人工发布或进入 Wechatsync 草稿同步的发布包说明。

## Trigger when

- 用户说“基于知识库和关键词生成文章”
- 用户说“同一主题直接出多个平台版本”
- 用户说“给我一份可审阅的发布包”
- 用户说“帮我准备 7 平台发布包”
- 用户说“先不要直发，只要审核通过后的 payload”

## Default workflow

### Step 1 - 确认知识来源与目标

先确认用户已经给出产品/工具、知识来源、主关键词、热点线索和大纲描述。如果信息不足，再补问最少必要信息。

### Step 2 - 生成主稿与 7 平台 payload

围绕同一个主题，先生成 AI 友好结构主稿，再拆成 7 平台 payload。保持平台风格差异，但不编造事实，不虚构个人经历。

### Step 3 - 整理发布包

把 7 平台的标题、简介、正文、标签建议、封面方向、审核结论与发布说明整理成一份可审阅结果，便于用户复制、修改、协作和手动发布。

## Network and local-file boundaries

- 默认**不读取**任何本地路径，包括 `~/.ip-publisher/profile.yaml`。
- 默认**不写入**任何本地文件。
- 默认**不主动抓取**网页或实时热点。
- 只有在用户明确要求“看最新热点”时，才进入检索，并在结果里标明来源。
- 只有在用户明确要求“导出到本地仓库脚本”时，才说明 companion repo 模式的额外资源；该动作不属于当前已安装 skill 的默认能力。

## Publishing boundary

- 默认只输出**可人工发布的发布包**或 **Wechatsync 草稿同步信息**，不直接进入平台后台。
- 默认不代管账号、Cookie、Token 或密码。
- 默认不声称“已发布成功”。
- 如果用户明确要求发布执行，也要先说明：这超出当前已发布 skill 的默认边界，需要另行确认外部工具、登录状态与人工接管方式。

## Output requirements

最终结果至少包含以下内容：

- 知识来源与关键词摘要
- 主稿标题、摘要与审核状态
- 7 平台版本标题、简介与正文
- 每个平台的标签建议
- 封面 brief
- 发布说明、Wechatsync 草稿同步信息与人工检查项

## Operating rules

- 如果用户只要某一个平台，只输出对应版本。
- 如果用户没有给知识来源，先补问，不默认联网。
- 如果用户要求“更像人写的”，就在改写时加强口语感、节奏变化与个人语气，但不得降低事实准确性。
- 如果用户要求使用仓库脚本或本地文件，先明确那是 **companion repo mode**，不是当前 skill 包的默认组成部分。
