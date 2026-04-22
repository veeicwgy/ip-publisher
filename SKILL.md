---
name: ip-publisher-suite
description: 全流程内容自动发布 Skill。从知识库驱动写文章、去 AI 味，到适配多平台格式，再通过 Wechatsync MCP 连接浏览器扩展，一键把草稿同步到知乎、掘金、CSDN、微信公众号等平台。Use for: 用户说"帮我写文章发布到多个平台"、"自动发布内容"时。
---

# IP Publisher 全流程发布 Skill

## 整体流程

```
1. 写文章（知识库驱动生成）
      ↓
2. 去 AI 味（humanizer）
      ↓
3. 多平台格式适配（7 平台 payload）
      ↓
4. 提醒用户连接 Wechatsync 浏览器扩展
      ↓
5. 服务器通过本地 WebSocket 连接 MCP，发起同步
      ↓
6. 各平台草稿写入成功，给出草稿链接
```

---

## Phase 0：收集用户素材（必须先做）

**在生成任何内容之前，必须先检查用户是否提供了以下 4 项信息，缺少任意一项都要主动提问，不能直接使用示例知识库。**

| 必填项 | 说明 | 缺失时的处理方式 |
|--------|------|----------------|
| **主题 / 产品名** | 文章要写什么 | 必须向用户提问，无法自动补全 |
| **内容素材** | 产品文档、官网说明、已有文章等 | 缺失时调用 `skills/hotspot-fetcher/` 抓取当日热点作为素材补充，或直接用热点驱动 |
| **主关键词** | 想被哪些词搜索到 | 缺失时根据主题和热点自动推断 2-3 个，向用户确认 |
| **热点线索** | 想蹭的热点或选题方向 | 缺失时调用 `skills/hotspot-fetcher/` 自动抓取，筛选与主题相关的热点供用户选择 |

### 收集流程

1. 用户发来请求后，先检查上面 4 项是否齐全
2. **一次性把所有缺失项合并提问**，不要分多轮逐一询问
3. 收到用户回复后，按下面规则补全缺失项，再进入 Phase 1

### 各项缺失时的自动补全规则

**素材缺失：**
- 如果用户提供了文档/文字素材 → 写入 `outputs/<YYYYMMDD>-<topic>/kb_raw/<产品名>.md`
- 如果用户没有素材 → 调用 `skills/hotspot-fetcher/` 抓取热点，结合主题生成大纲，`kb_scope.doc_ids` 留空

**热点缺失：**
- 调用 `skills/hotspot-fetcher/` 抓取当日热点
- 从结果中筛选 3-5 条与主题相关的，以列表形式让用户选择，或直接使用最相关的一条

**关键词缺失：**
- 根据主题名称 + 热点线索自动推断 2-3 个主关键词
- 在对话中告知用户推断结果，用户可直接确认或修改

**目标读者（可选，未提供时自动推断）：**
- 根据主题和内容类型自动推断，写入 request.json

### 构建 request.json

收齐所有信息后，在 `outputs/<YYYYMMDD>-<topic>/tasks/request.json` 中构建任务请求，再进入 Phase 1。

> ⚠️ 绝对不要直接使用 `data/kb_raw/mineru-*` 示例文件，那是项目自带的演示数据，与用户无关。

---

## Phase 1：生成文章

### 环境准备

项目路径：`/home/limeiying/FFFFFFFFFiles/ip-publisher`

首次使用需创建 Python 虚拟环境并安装依赖：

```bash
cd /home/limeiying/FFFFFFFFFiles/ip-publisher
python3 -m venv .venv
.venv/bin/pip install pyyaml requests
```

### 目录结构规则

```
outputs/
  <YYYYMMDD>-<topic>/              ← 每次任务一个带时间戳的独立目录
    kb_raw/                        ← 本次任务的知识库文档（不上传 GitHub）
      <产品名>.md
    tasks/
      request.json                 ← 本次任务的 request（不上传 GitHub）
    platforms/                     ← 各平台文章（由 run_phase1 自动生成）
      zhihu.md
      juejin.md
      csdn.md
      ...
    article.md
    audit_report.json
    publish_package.json

data/
  kb_raw/                          ← 只放示例文档（mineru 等，随仓库提交）
  tasks/                           ← 只放示例 request（随仓库提交）
```

> ⚠️ `outputs/` 已加入 `.gitignore`，不会上传 GitHub。
> `data/kb_raw/` 和 `data/tasks/` 只放示例，参考格式用，不放真实用户内容。

> ⚠️ **关键**：`run_phase1` 的输出逻辑是 `output_root / task_id / platforms/`。
> 因此 `--output-root` 必须指向 **任务目录的父级**，`task_id` 必须与目录名一致，
> 即：`--output-root outputs`，`task_id` 设为 `<YYYYMMDD>-<topic>`，
> 最终 platforms 会落在 `outputs/<YYYYMMDD>-<topic>/platforms/`。

### 准备 request.json（参考示例格式）

参考 `data/tasks/demo-request.json` 的结构，在 `outputs/<YYYYMMDD>-<topic>/tasks/request.json` 新建：

```json
{
  "task_id": "<YYYYMMDD>-<topic>",
  "product": { "name": "产品名" },
  "kb_scope": { "doc_ids": ["<产品名>"], "tags": ["knowledge-base"] },
  "seo": {
    "primary_keywords": ["主关键词"],
    "secondary_keywords": ["次关键词"],
    "forbidden_terms": ["禁用词"]
  },
  "hotspot": {
    "title": "热点选题标题",
    "summary": "热点说明",
    "source": "manual"
  },
  "outline": {
    "brief": "大纲说明",
    "must_include_sections": ["核心结论", "产品价值", "使用场景", "上手入口"]
  },
  "platforms": ["wechat_official","xiaohongshu","zhihu","juejin","csdn","toutiao","weibo"],
  "audience": "目标读者",
  "tone": "轻松、实用、有共鸣感",
  "content_type": "general",
  "language": "zh-CN"
}
```

知识库文档放在 `outputs/<YYYYMMDD>-<topic>/kb_raw/<产品名>.md`，支持 `.md` 和 `.json` 格式。

### 执行生成

```bash
# 设置时间戳和主题（根据实际情况替换）
TASK_ID="$(date +%Y%m%d)-<topic>"   # 例如 20260422-nanadraw

export PYTHONPATH=/home/limeiying/FFFFFFFFFiles/ip-publisher
cd /home/limeiying/FFFFFFFFFiles/ip-publisher

# 注意：--output-root 必须指向 outputs/（父级目录）
# 程序会自动在 outputs/<task_id>/ 下生成所有文件，包括 platforms/
.venv/bin/python3 -m ip_publisher.cli.run_phase1 \
  --request outputs/${TASK_ID}/tasks/request.json \
  --kb-dir outputs/${TASK_ID}/kb_raw \
  --output-root outputs
```

生成结果在 `outputs/<YYYYMMDD>-<topic>/`：

| 文件 | 内容 |
|------|------|
| `article.md` | 主稿 Markdown |
| `audit_report.json` | 审核报告，需 `status == pass` 才可发布 |
| `publish_package.json` | 各平台标题、正文、标签、封面说明 |
| `platforms/*.md` | 各平台独立文件，直接用于发布 |

---

## Phase 2：去 AI 味（Humanizer）

生成的文章会经过内置轻量 humanizer，自动完成：

- 删除"首先、其次、总的来说、值得注意的是"等 AI 套话
- 打散过于整齐的并列句式
- 保留事实和数据不变，只做表达自然化

如果需要更深度的去 AI 味，可调用 `skills/humanizer/` 中的规则对 `article.md` 做二次处理。

---

## Phase 3：多平台格式适配

生成完成后，`platforms/` 下会有 7 个平台独立文件，格式已自动适配：

| 平台 | 文件 | 格式 | 字数限制 |
|------|------|------|---------|
| 微信公众号 | `wechat_official.md` | html | 20000 |
| 小红书 | `xiaohongshu.md` | markdown | 1000 |
| 知乎 | `zhihu.md` | markdown | 5000 |
| 掘金 | `juejin.md` | markdown | 10000 |
| CSDN | `csdn.md` | markdown | 10000 |
| 头条号 | `toutiao.md` | html | 5000 |
| 微博 | `weibo.md` | text | 140 |

---

## Phase 4：提醒用户连接 Wechatsync

**不允许在用户未看到文章内容的情况下直接发布。**
**在执行发布前，必须先确认用户的 Chrome 扩展已连接。**

向用户发送如下提示：

> 📌 **发布前需要你做一步操作：**
>
> 1. 在 Chrome 中安装 **文章同步助手 (Wechatsync)** 扩展
>    → 官网安装：https://www.wechatsync.com/#install
>    → 或 Chrome 商店：https://chromewebstore.google.com/detail/hchobocdmclopcbnibdnoafilagadion
>
> 2. 在浏览器工具栏**点击**扩展图标 → **点击**“文章同步助手” → 选择「设置」→ 找到「**CLI/MCP 连接**」或「**同步桥接**」→ **启用开关**
>
> 3. 页面上会显示一串 Token，**把它发给我**
>
> 4. 在 Chrome 中登录你想要发布的平台账号（知乎、掘金、CSDN 等）
>
> 完成后告诉我，我就可以开始发布了。

---

## Phase 5：服务器连接 MCP 并发布

### 安装 wechatsync CLI

```bash
npm install -g @wechatsync/cli
```

### 工作原理

```
服务器（AI 助手）
     │
     │  export WECHATSYNC_TOKEN="用户的token"
     │  wechatsync sync article.md -p juejin
     │
     ▼
localhost:9527 (WebSocket)
     │
     │  ← Chrome 扩展主动连接过来 →
     │
     ▼
Chrome Extension（在用户电脑上运行）
     │
     │  使用浏览器中已登录的 Cookie
     │
     ▼
各平台 API（知乎 / 掘金 / CSDN / ...）
```

> ⚠️ 关键：wechatsync CLI 会在本机启动一个 WebSocket 服务（端口 9527）。
> Chrome 扩展启用「MCP 连接 / 同步桥接」后，会主动连接到这个端口。
> 只要用户的浏览器和服务器在同一个网络环境（或通过 OpenClaw 转发），连接即可建立。

### 验证连接

在执行发布前，先用以下命令确认连接状态和已登录平台：

```bash
export WECHATSYNC_TOKEN="用户提供的token"
wechatsync platforms --auth
```

预期输出示例：
```
✔ Chrome Extension 已连接 (通过 PRIMARY 转发)

支持的平台 (29):
  zhihu   知乎  ✓ 已登录
  juejin  掘金  ✓ 已登录
  csdn    CSDN  ✓ 已登录
  weixin  微信公众号  ✗ 未登录（登录态过期需刷新）
  ...
```

只向**已登录**的平台发布。

### 执行同步（逐平台）

```bash
# 掘金
wechatsync sync outputs/<task_id>/platforms/juejin.md -p juejin

# 知乎
wechatsync sync outputs/<task_id>/platforms/zhihu.md -p zhihu

# CSDN
wechatsync sync outputs/<task_id>/platforms/csdn.md -p csdn

# 微信公众号（需已登录）
wechatsync sync outputs/<task_id>/platforms/wechat_official.md -p weixin

# 小红书（需已登录）
wechatsync sync outputs/<task_id>/platforms/xiaohongshu.md -p xiaohongshu

# 头条（需已登录）
wechatsync sync outputs/<task_id>/platforms/toutiao.md -p toutiao

# 微博（文件无 # 标题，需加 --title）
wechatsync sync outputs/<task_id>/platforms/weibo.md \
  --title "文章标题" -p weibo
```

> ⚠️ 微博等纯文本平台的 .md 文件可能没有 `# 标题`，必须加 `--title` 参数，否则报错。

---

## Phase 6：发布结果汇报

每个平台同步完成后，汇总结果给用户：

```
✅ 同步成功（3 个平台）：

  掘金   → https://juejin.cn/editor/drafts/xxxxxx
  知乎   → https://zhuanlan.zhihu.com/p/xxxxxx/edit
  CSDN   → https://editor.csdn.net/md?articleId=xxxxxx

❌ 未同步（原因）：
  微信公众号 → 登录态已过期，请在浏览器重新登录后告知我
  小红书     → 未登录
```

所有同步结果均为**草稿**，用户人工确认内容后再点击发布。

---

## 常见问题排查

| 问题 | 原因 | 解决方式 |
|------|------|---------|
| `Chrome Extension 未连接` | 扩展未启用 MCP/同步桥接，或连接已超时断开 | 打开 Wechatsync 扩展选项页 → 把「同步桥接 / MCP 连接」开关**关掉再重新打开一次**，等待重新连接后再试 |
| `登录态超时` | 平台 Cookie 过期 | 在 Chrome 中重新打开该平台网页并登录 |
| `无法从文件提取标题` | .md 文件无 `# 标题` | 命令中加 `--title "标题"` |
| `No knowledge-base chunks matched` | kb_raw 中没有匹配文档 | 检查 `data/kb_raw/` 文件是否存在，并加 `--kb-dir` 参数 |
| `ModuleNotFoundError: ip_publisher` | 未设置 PYTHONPATH | 加 `export PYTHONPATH=/path/to/ip-publisher` |

---

## 完整一键命令示例

```bash
# ==== 准备阶段 ====

# 0. 设置当前任务参数（每次替换）
TASK_DATE=$(date +%Y%m%d)
TASK_TOPIC="nanadraw"              # 替换为实际主题
TASK_DIR="outputs/${TASK_DATE}-${TASK_TOPIC}"

cd /home/limeiying/FFFFFFFFFiles/ip-publisher
export PYTHONPATH=$(pwd)

# 1. 创建本次任务目录
mkdir -p ${TASK_DIR}/kb_raw ${TASK_DIR}/tasks ${TASK_DIR}/platforms

# 2. 把用户提供的素材写入知识库（内容由 Phase 0 收集后填入）
# 示例： cat > ${TASK_DIR}/kb_raw/<产品名>.md << 'EOF'
# 用户素材内容...
# EOF

# 3. 构建 request.json（参考 data/tasks/demo-request.json 格式）
# 内容由 Phase 0 收齐 4 项信息后自动写入
# ${TASK_DIR}/tasks/request.json

# ==== 生成阶段 ====

# 4. 运行 Phase 1 生成文章
# 注意：--output-root 指向 outputs/，程序会自动在其下创建 <task_id>/platforms/
# task_id 必须与 TASK_DIR 的目录名一致（即 request.json 里的 task_id 字段）
.venv/bin/python3 -m ip_publisher.cli.run_phase1 \
  --request ${TASK_DIR}/tasks/request.json \
  --kb-dir ${TASK_DIR}/kb_raw \
  --output-root outputs

# 生成结果落在：
# outputs/${TASK_DATE}-${TASK_TOPIC}/article.md
# outputs/${TASK_DATE}-${TASK_TOPIC}/platforms/zhihu.md
# outputs/${TASK_DATE}-${TASK_TOPIC}/platforms/juejin.md  ... 等

# ==== 用户确认阶段 ====

# 5. 展示文章给用户确认（必须做，不能跳过）
# 用户确认内容后再进入发布

# ==== 发布阶段 ====

# 6. 设置 Token（用户提供）
export WECHATSYNC_TOKEN="用户的token"

# 7. 验证连接和已登录平台
wechatsync platforms --auth

# 8. 逐平台同步（只向已登录的平台发布）
for platform in juejin zhihu csdn; do
  wechatsync sync ${TASK_DIR}/platforms/${platform}.md -p ${platform}
done

# 微博文件无 # 标题，需单独处理
wechatsync sync ${TASK_DIR}/platforms/weibo.md \
  --title "文章标题" -p weibo
```
