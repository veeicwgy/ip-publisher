---
name: ip publisher xiaohongshu wechat zhihu content publisher
description: IP Publisher is a Xiaohongshu, WeChat Official Account, and Zhihu content workflow skill for personal IP creators who need one workflow from hotspot selection to drafting, AI style removal, cover brief creation, and publish-pack preparation. Use for: xiaohongshu publisher, wechat publisher, zhihu publisher, ip publisher, personal IP content workflow, AI content workflow, hotspot selection, platform-native article generation, and safe multi-platform publish-pack preparation. 默认不自动登录、不代管凭证、不在未经同意时持久化本地配置。
---

# IP Publisher

## Use this skill as a Xiaohongshu WeChat Zhihu content publisher workflow

当用户想把“找热点、定角度、写内容、去 AI 味、出封面、做发布准备”串成一条完整流程时，使用本 Skill。它尤其适合 **xiaohongshu publisher**、**wechat publisher**、**zhihu publisher**、**personal IP**、**AI content workflow**、**content automation** 与 **multi-platform publishing preparation** 场景。

## Platform coverage: Xiaohongshu, WeChat Official Account, Zhihu and more

该 Skill 重点支持以下平台及其对应写法：**Xiaohongshu / 小红书**、**WeChat Official Account / 微信公众号**、**Zhihu / 知乎**、CSDN、Weibo、Toutiao、Juejin。它会根据目标平台输出适合的平台原生版本，而不是把一份通稿强行改写。

## Trigger when

- 用户说“帮我做 personal IP 内容工作流”
- 用户说“做一个 AI content workflow”
- 用户说“给我写一篇小红书笔记”
- 用户说“帮我写一篇微信公众号文章”
- 用户说“帮我生成一篇知乎回答或知乎文章”
- 用户说“基于热点写内容并准备发布”
- 用户说“帮我去 AI 味，再生成封面和发布包”
- 用户说“准备发布内容到 XX 平台”
- 用户说“生成发布包”
- 用户说“把这篇内容拆成多个平台版本”

## What users get after install

安装后，用户得到的是一条可执行的 **IP Publisher workflow**：热点抓取、选题判断、内容策略、平台草稿、AI style removal、封面 brief，以及最终的发布准备包。对于 **Xiaohongshu / 小红书**、**WeChat Official Account / 微信公众号**、**Zhihu / 知乎**，它会直接产出更接近平台原生格式的标题、正文、标签与发布建议。默认产出是**可人工审阅、可复制粘贴、可继续交给人工后台发布**的内容包；仓库内还提供 `scripts/generate-publish-pack.py`，可把草稿整理成 Markdown / JSON 双格式发布包。只有在用户明确要求、并且本地发布插件或账号环境已由用户自行配置完成时，才进入发布执行环节。

## Searchable use cases

| Search intent | What this skill can do |
| --- | --- |
| `ip publisher` | 用品牌词直接进入个人 IP 内容工作流主流程 |
| `personal ip` | 为个人品牌、知识型创作者、行业 IP 提供内容生产工作流 |
| `ai content workflow` | 将热点、选题、写作、润色、封面与发布准备串联起来 |
| `xiaohongshu` | 生成小红书笔记结构、标题、正文、标签与封面方向 |
| `xiaohongshu publisher` | 为小红书准备可直接发布的笔记草稿、标签与封面 brief |
| `wechat official account` | 生成微信公众号文章结构、标题与导语结尾 |
| `wechat publisher` | 为微信公众号准备文章草稿、摘要、导语、结尾与发布说明 |
| `zhihu` | 生成知乎回答、知乎文章的逻辑展开与观点表达 |
| `zhihu publisher` | 为知乎回答或文章准备更适合发布的观点结构与正文草稿 |

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
| `multi-publisher` | 发布准备或发布执行 | 依赖用户本地已安装并登录的发布插件/工具（当前以 Wechatsync 手动链路为主） | 默认输出发布包与预检结果，非默认自动发布 |

## Step by step personal IP content workflow

### Step 1 - 人设加载或临时设定

1. 优先检查用户是否已在当前会话提供职业、领域、风格、受众、价值观和禁忌话题。
2. 若本地存在 `~/.ip-publisher/profile.yaml`，先询问用户是否直接复用。
3. 若用户未授权本地保存，则仅在当前任务中临时使用该人设信息。
4. 只有在用户明确说“保存人设配置”时，才把结构化结果写入本地 YAML。

### Step 2 - 热点抓取与筛选

1. 调用 `hotspot-fetcher` 抓取与当前领域相关的公开热点。
2. 热点来源按 `hotspot-fetcher` 已声明的数据源执行，不引用未声明的私有接口。
3. 返回 Top 5 候选，并写明每个热点与人设的结合角度。

### Step 3 - 话题选择与内容策略

1. 如果用户没有指定主题，则展示候选热点供用户选择。
2. 如果用户明确要求自动选择，则选择匹配度最高的话题，并在结果中说明选择依据。
3. 输出内容策略，包括标题方向、核心观点、目标情绪和风险边界。

### Step 4 - Platform writing for Xiaohongshu, WeChat Official Account, Zhihu and others

根据目标平台调用 `article-generator` 生成草稿，并遵循对应平台的篇幅、结构和语气要求。若用户一次指定多个平台，则为每个平台分别生成版本，不混淆格式。对于 Xiaohongshu、WeChat Official Account、Zhihu，应优先输出更贴近平台原生阅读习惯的表达方式。

### Step 5 - 去 AI 味处理

1. 调用 `humanizer` 对草稿进行润色。
2. 重点减少模板化衔接词、过度工整句式和缺乏个人语气的问题。
3. 保留事实准确性，不为了“像人写的”而添加未经证实的信息。

### Step 6 - 封面方案生成

1. 调用 `cover-generator` 生成封面 brief、提示词或封面图。
2. 平台尺寸规则由 `cover-generator` 自身声明负责。
3. 如果当前环境不能直接生成图片，则至少输出可复用的封面文案和构图要求。

### Step 7 - 发布准备或发布执行

1. 默认先生成“发布包”，包括标题、正文、封面、标签、平台填写建议和注意事项；如需结构化文件，可调用 `scripts/generate-publish-pack.py` 输出 Markdown / JSON。
2. 若用户明确要求执行发布，则先检查 `multi-publisher` 所声明的前置条件是否满足。
3. 当前默认发布链路依赖用户本地已安装并已登录的 Wechatsync 等工具；若条件不满足，则退回手动复制粘贴发布方案。
4. 输出真实状态报告，只能写“已准备”“待用户确认”“手动发布完成”或“插件执行结果”，不得虚构平台回执。

## Operational rules

- 如果用户只要求某一个子步骤，只执行该步骤及必要前置步骤。
- 如果未指定平台，先询问一次目标平台；若用户要求自动化，可按其历史偏好给出推荐，但仍需在结果中说明。
- 如果未指定话题，优先进入热点抓取。
- 如果用户要求“没有 AI 感”，必须执行 `humanizer`。
- 如果用户要求直接发布，必须先检查是否具备用户授权、已登录状态和插件条件。

## Output format

每一步完成后，输出当前状态与预览内容。最终输出完整结果时，至少包含以下信息：

- 已使用的人设摘要（注明是临时会话还是本地配置）
- 选中的热点或话题，以及选择原因
- 内容策略摘要
- 各平台标题与正文预览
- 去 AI 味处理说明
- 封面方案摘要
- 发布准备状态，或真实发布结果与失败原因
