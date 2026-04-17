---
name: ip publisher xiaohongshu wechat zhihu publish pack
description: 帮你把一个话题改写成小红书、公众号、知乎三个版本，一键生成发布包。Use for: ip publisher, xiaohongshu publisher, wechat publisher, zhihu publisher, publish pack, content workflow, multi-platform rewrite. 默认不自动登录、不托管凭证、不伪造已发布成功。
---

# IP Publisher

## Use this skill when the user wants one topic rewritten into Xiaohongshu, WeChat, and Zhihu versions

当用户想把**一个话题**快速改写成 **小红书 / Xiaohongshu**、**微信公众号 / WeChat Official Account**、**知乎 / Zhihu** 三个平台版本，并顺手整理成可审阅、可复制、可协作的**发布包**时，使用本 Skill。它的核心结果不是“替用户偷偷代发”，而是把三平台内容、标签、封面建议与发布说明收拢成一份真实可交付的结果。

## What users can search for

这个 Skill 现在优先覆盖下面这些更直接的搜索意图：**ip publisher**、**xiaohongshu publisher**、**wechat publisher**、**zhihu publisher**、**publish pack**、**content workflow**、**multi-platform rewrite**。如果用户说的是“帮我把一个主题拆成小红书、公众号、知乎三个版本”“给我一份发布包”“把母稿改写成三平台版本”，都应该命中这个 Skill。

## Trigger when

- 用户说“帮我把这个主题写成小红书、公众号、知乎三个版本”
- 用户说“给我一键生成发布包”
- 用户说“把这篇母稿拆成三平台版本”
- 用户说“我想做 xiaohongshu publisher / wechat publisher / zhihu publisher”
- 用户说“帮我准备可人工发布的内容包”
- 用户说“基于这个话题先出三个平台版本，再给我发布建议”

## What users get after install

安装后，用户默认得到的是一条**更短、更直观**的结果链路：输入一个话题，补一句核心角度，然后产出小红书版、公众号版、知乎版，以及对应的标题、正文、标签、封面 brief 与发布说明。仓库里还提供 `scripts/quickstart.py` 和 `scripts/generate-publish-pack.py`，前者通过交互问答直接生成结果，后者适合脚本化批量整理 Markdown / JSON 双格式发布包。

## Platform coverage

当前重点支持以下平台与表达风格：

| 平台 | 默认结果形态 | 重点改写方向 |
| --- | --- | --- |
| Xiaohongshu / 小红书 | 短句、emoji、互动感更强 | 更快进入主题，方便直接发笔记 |
| WeChat Official Account / 微信公众号 | 叙事型长文 | 信息更完整，适合观点展开 |
| Zhihu / 知乎 | 先说结论再论证 | 更强调逻辑结构和分析感 |

## Safety and operational boundaries

- 默认**不自动保存**用户画像到本地文件；仅在用户明确同意“保存到本机配置”时，才写入 `~/.ip-publisher/profile.yaml`。
- 默认**不收集、不代填、不托管**任何平台账号、Cookie、Token 或密码。
- 默认**不直接联网登录平台后台**；发布动作仅在用户明确授权且本地环境已具备所需插件时尝试。
- 若缺少发布条件，本 Skill 改为输出手动发布包，不伪造“已发布成功”。
- 所有外部动作都应在结果中说明来源、依赖项与限制，不隐瞒前置条件。

## External dependencies and declared interfaces

| 模块 | 用途 | 依赖/接口说明 | 默认行为 |
| --- | --- | --- | --- |
| `ip-profile` | 加载或整理人设信息 | 可选读取 `~/.ip-publisher/profile.yaml` | 未获同意时仅使用当前会话信息 |
| `hotspot-fetcher` | 抓取热点 | 使用公开网页抓取/搜索能力；来源以 Skill 内声明为准 | 输出热点候选，不做隐式登录 |
| `article-generator` | 生成平台文案 | 本地 Skill 编排 | 输出草稿 |
| `humanizer` | 降低 AI 味 | 本地 Skill 编排 | 输出润色版草稿 |
| `cover-generator` | 生成封面方案或提示词 | 调用图像生成能力时，应在结果中说明 | 默认输出封面 brief 或可执行提示词 |
| `multi-publisher` | 发布准备或发布执行 | 依赖用户本地已安装并登录的发布插件/工具 | 默认输出发布包与预检结果，非默认自动发布 |

## Step by step workflow

### Step 1 - 确认是否已有话题与平台

1. 如果用户已经给出明确主题，直接进入平台改写。
2. 如果用户未给出话题，再补做热点抓取与选题建议。
3. 如果用户未指定平台，默认优先提供 Xiaohongshu、WeChat Official Account、Zhihu 三个平台版本。

### Step 2 - 确认人设与核心角度

1. 优先检查用户是否已在当前会话提供职业、领域、风格、受众、价值观和禁忌话题。
2. 若本地存在 `~/.ip-publisher/profile.yaml`，先询问用户是否直接复用。
3. 若用户未授权本地保存，则仅在当前任务中临时使用该人设信息。
4. 只有在用户明确说“保存人设配置”时，才把结构化结果写入本地 YAML。

### Step 3 - 生成三平台版本

1. 调用 `article-generator` 先输出一个母稿或核心观点骨架。
2. 针对 Xiaohongshu 生成更短、更口语、更适合互动的版本。
3. 针对 WeChat Official Account 生成更完整、更叙事的版本。
4. 针对 Zhihu 生成更强调结论、结构和论证的版本。

### Step 4 - 去 AI 味处理

1. 调用 `humanizer` 对三平台正文进行润色。
2. 重点减少模板化衔接词、过度工整句式和缺乏个人语气的问题。
3. 保留事实准确性，不为了“像人写的”而添加未经证实的信息。

### Step 5 - 封面方案生成

1. 调用 `cover-generator` 生成封面 brief、提示词或封面图。
2. 平台尺寸规则由 `cover-generator` 自身声明负责。
3. 如果当前环境不能直接生成图片，则至少输出可复用的封面文案和构图要求。

### Step 6 - 生成发布包

1. 默认先生成“发布包”，包括标题、正文、封面、标签、平台填写建议和注意事项。
2. 若需要结构化文件，可调用 `scripts/quickstart.py` 或 `scripts/generate-publish-pack.py` 输出 Markdown / JSON。
3. 若用户明确要求执行发布，则先检查 `multi-publisher` 所声明的前置条件是否满足。
4. 输出真实状态报告，只能写“已准备”“待用户确认”“手动发布完成”或“插件执行结果”，不得虚构平台回执。

## Operational rules

- 如果用户只要求某一个子步骤，只执行该步骤及必要前置步骤。
- 如果未指定平台，默认给出 Xiaohongshu、WeChat Official Account、Zhihu 三个平台版本。
- 如果未指定话题，优先进入热点抓取。
- 如果用户要求“没有 AI 感”，必须执行 `humanizer`。
- 如果用户要求直接发布，必须先检查是否具备用户授权、已登录状态和插件条件。

## Output format

每一步完成后，输出当前状态与预览内容。最终输出完整结果时，至少包含以下信息：

- 已使用的人设摘要（注明是临时会话还是本地配置）
- 选中的热点或话题，以及选择原因
- 内容策略摘要
- 小红书、公众号、知乎三个版本的标题与正文预览
- 去 AI 味处理说明
- 封面方案摘要
- 发布包状态，或真实发布结果与失败原因
