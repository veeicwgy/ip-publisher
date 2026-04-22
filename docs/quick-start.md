# Quick Start

## 目标

最短链路已经改成：

```text
git clone -> bash scripts/setup.sh -> python3 scripts/quickstart.py -> 生成 7 平台发布包 + 审核报告
```

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/veeicwgy/ip-publisher.git
cd ip-publisher
```

### 2. 执行安装脚本

```bash
bash scripts/setup.sh
```

安装脚本会完成：

- 安装 Python 依赖
- 拉取 `wewrite`、`Humanizer-zh`、`Wechatsync` 等上游仓库到 `~/.ip-publisher/deps/`
- 安装 `skills/`
- 初始化 `~/.ip-publisher/profile.yaml`

### 3. 跑 quickstart

```bash
python3 scripts/quickstart.py
```

现在 quickstart 会问的不是“主题 / 核心观点 / 目标平台”，而是：

```text
产品或工具名
需要运营的主关键词
热点线索 / 选题描述
大纲描述
主要读者
内容类型（general / technical）
```

默认直接输出 7 平台 bundle：

- `wechat_official`
- `xiaohongshu`
- `zhihu`
- `juejin`
- `csdn`
- `toutiao`
- `weibo`

## 产物

执行完成后，`outputs/<task_id>/` 下会出现：

| 文件 | 作用 |
| --- | --- |
| `request.json` | 本次任务输入 |
| `draft.json` | 主稿、结构信号、平台版本 |
| `audit_report.json` | 审核结论 |
| `publish_package.json` | 发布包定义 |
| `article.md` | 适合人工审阅 |
| `platforms/*.md` | 平台级 payload，可直接交给 Wechatsync 或人工复制 |

## 推荐首条动作

| 动作 | 目的 |
| --- | --- |
| 直接跑 `python3 scripts/quickstart.py` | 最快看见知识库驱动生成 + 审核 + 7 平台发布包 |
| 跑 `python3 -m ip_publisher.cli.run_phase1 --request data/tasks/demo-request.json` | 看结构化接口如何接系统 |
| 看 `docs/platform-support.md` | 确认 canonical 平台矩阵 |
| 看 `docs/publish-package.md` | 理解发布包到底交付什么 |

## 故障排查

| 问题 | 原因 | 处理方式 |
| --- | --- | --- |
| quickstart 运行后还在问“目标平台” | 旧脚本未更新 | 拉最新代码后重新执行 |
| 文章没有进入直发 | `audit_report.status` 不是 `pass` | 先修 blocker，再重新生成 |
| 想直接发到平台 | 当前默认走 Wechatsync 草稿同步 | 先确保浏览器已登录，再看 `publish_package.json` 里的 `cli_example` |
| 技术文章没有代码示例 | `content_type` 不是 `technical` | 生成时切到 `technical` |
