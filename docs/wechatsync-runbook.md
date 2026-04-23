# Wechatsync Runbook

> **适用场景：仓库使用者（Repo Mode）**
>
> 本文档仅适用于克隆了 `ip-publisher` 仓库、在本地运行 CLI 脚本、并希望通过 Wechatsync 将草稿同步到各平台的用户。
>
> 如果你是通过 ClawHub 安装的 Skill 用户，默认工作流在生成发布包后停止，不涉及本文档的任何操作。

---

## 前置条件

在执行任何发布操作前，必须满足以下所有条件：

1. **内容已生成**：`article.md` 和 `platforms/*.md` 均已生成。
2. **审核已通过**：`audit_report.json` 中 `status == pass`。未通过审核时，**禁止进入发布流程**。
3. **用户已确认内容**：用户已阅读并确认文章内容无误。
4. **Wechatsync 扩展已连接**：用户 Chrome 中的扩展已启用并提供了 Token。

---

## Phase 1：本地环境准备（仅首次）

```bash
cd /path/to/ip-publisher   # 替换为你的实际路径
python3 -m venv .venv
.venv/bin/pip install pyyaml requests
```

## Phase 2：生成内容

```bash
TASK_ID="$(date +%Y%m%d)-<topic>"   # 例：20260422-nanadraw

export PYTHONPATH=$(pwd)

.venv/bin/python3 -m ip_publisher.cli.run_phase1 \
  --request outputs/${TASK_ID}/tasks/request.json \
  --kb-dir   outputs/${TASK_ID}/kb_raw \
  --output-root outputs
```

生成结果说明：

| 文件 | 内容 |
|---|---|
| `article.md` | 主稿 Markdown |
| `audit_report.json` | 审核报告，`status == pass` 才可继续 |
| `publish_package.json` | 各平台标题、正文、标签、封面说明 |
| `platforms/*.md` | 7 个平台独立文件 |

> ⚠️ 目录结构要求：`--output-root` 指向 `outputs/`（父级），`task_id` 与 `request.json` 中的 `task_id` 字段保持一致。最终文件落在 `outputs/<task_id>/platforms/`。

---

## Phase 3：引导用户连接 Wechatsync

在执行发布前，向用户发送以下操作指引：

> 📌 **发布前需要你做一步操作：**
>
> 1. 在 Chrome 中安装 **文章同步助手 (Wechatsync)** 扩展
>    → 官网：https://www.wechatsync.com/#install
>    → Chrome 商店：https://chromewebstore.google.com/detail/hchobocdmclopcbnibdnoafilagadion
>
> 2. 点击扩展图标 → 设置 → 找到「CLI/MCP 连接」或「同步桥接」→ **启用开关**
>
> 3. 页面会显示一串 Token，**把它发给我**
>
> 4. 在 Chrome 中登录你想发布的平台账号（知乎、掘金、CSDN 等）
>
> 完成后告诉我，我就可以开始发布了。

---

## Phase 4：安装 CLI 并验证连接

```bash
npm install -g @wechatsync/cli

export WECHATSYNC_TOKEN="<用户提供的 token>"
wechatsync platforms --auth
```

预期输出：

```
✔ Chrome Extension 已连接

支持的平台:
  zhihu   知乎  ✓ 已登录
  juejin  掘金  ✓ 已登录
  csdn    CSDN  ✓ 已登录
  weixin  微信公众号  ✗ 未登录
```

**只向「已登录」的平台同步。**

---

## Phase 5：执行同步

```bash
TASK_ID="<本次任务 ID>"
export WECHATSYNC_TOKEN="<token>"

# 逐平台同步
wechatsync sync outputs/${TASK_ID}/platforms/juejin.md          -p juejin
wechatsync sync outputs/${TASK_ID}/platforms/zhihu.md           -p zhihu
wechatsync sync outputs/${TASK_ID}/platforms/csdn.md            -p csdn
wechatsync sync outputs/${TASK_ID}/platforms/wechat_official.md -p weixin
wechatsync sync outputs/${TASK_ID}/platforms/xiaohongshu.md     -p xiaohongshu
wechatsync sync outputs/${TASK_ID}/platforms/toutiao.md         -p toutiao

# 微博无 # 标题，需加 --title
wechatsync sync outputs/${TASK_ID}/platforms/weibo.md \
  --title "文章标题" -p weibo
```

---

## Phase 6：汇报结果

向用户汇总同步结果，格式参考：

```
✅ 同步成功（3 个平台）：
  掘金  → https://juejin.cn/editor/drafts/xxxxxx
  知乎  → https://zhuanlan.zhihu.com/p/xxxxxx/edit
  CSDN  → https://editor.csdn.net/md?articleId=xxxxxx

❌ 未同步：
  微信公众号 → 登录态已过期，请在浏览器重新登录后告知我
  小红书     → 未登录
```

所有结果均为**草稿**，用户人工确认后再点击发布。

---

## 排错指南

| 错误 | 原因 | 解决方式 |
|---|---|---|
| `Chrome Extension 未连接` | 扩展未启用同步桥接，或连接超时断开 | 在扩展设置页将「同步桥接 / MCP 连接」关掉再重新打开 |
| `登录态超时` | 平台 Cookie 过期 | 在 Chrome 中重新登录该平台 |
| `无法从文件提取标题` | .md 文件无 `# 标题` | 命令中加 `--title "标题"` |
| `No knowledge-base chunks matched` | kb_raw 中无匹配文档 | 检查 `kb_raw/` 文件存在，并确认 `--kb-dir` 参数正确 |
| `ModuleNotFoundError: ip_publisher` | PYTHONPATH 未设置 | 在项目根目录执行 `export PYTHONPATH=$(pwd)` |

---

## 一键脚本示例

```bash
# 设置参数
TASK_DATE=$(date +%Y%m%d)
TASK_TOPIC="your-topic"           # ← 替换
TASK_DIR="outputs/${TASK_DATE}-${TASK_TOPIC}"
WECHATSYNC_TOKEN="your-token"     # ← 用户提供

cd /path/to/ip-publisher           # ← 替换为实际路径
export PYTHONPATH=$(pwd)

# 1. 创建任务目录（素材和 request.json 需手动填入）
mkdir -p ${TASK_DIR}/kb_raw ${TASK_DIR}/tasks ${TASK_DIR}/platforms

# 2. 生成内容（确保 request.json 和 kb_raw/ 已准备好）
.venv/bin/python3 -m ip_publisher.cli.run_phase1 \
  --request ${TASK_DIR}/tasks/request.json \
  --kb-dir  ${TASK_DIR}/kb_raw \
  --output-root outputs

# 3. 检查审核结果（status 必须为 pass）
cat ${TASK_DIR}/audit_report.json | python3 -c "import sys,json; r=json.load(sys.stdin); print('PASS' if r.get('status')=='pass' else 'FAIL:', r.get('reason',''))"

# 4. ⚠️ 用户确认内容后再继续

# 5. 设置 Token 并验证连接
export WECHATSYNC_TOKEN="${WECHATSYNC_TOKEN}"
wechatsync platforms --auth

# 6. 同步到已登录平台
for platform in juejin zhihu csdn; do
  wechatsync sync ${TASK_DIR}/platforms/${platform}.md -p ${platform}
done
wechatsync sync ${TASK_DIR}/platforms/weibo.md --title "${TASK_TOPIC}" -p weibo
```
