# Quick Start

## 目标

在本地完成安装后，实现以下最短链路：

```text
git clone -> bash scripts/setup.sh -> 对 Claude 说“帮我写一篇小红书文章”
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

安装脚本会完成以下动作：

- 安装 Python 基础依赖
- 拉取上游开源仓库到 `~/.ip-publisher/deps/`
- 把 `skills/` 下的 Skill 安装到 Claude Code 与 OpenClaw 目录
- 初始化 `~/.ip-publisher/profile.yaml`

### 3. 启动首个任务

```text
帮我写一篇小红书文章
```

## 推荐首条指令

| 指令 | 目的 |
| --- | --- |
| 设置我的 IP 人设 | 初始化用户画像 |
| 给我看看今天适合我的热点 | 检查热点链路是否正常 |
| 帮我写一篇公众号文章 | 检查平台生成是否正常 |
| 去掉这篇文章的 AI 味 | 检查 Humanizer 是否接入 |
| 一键发布到知乎和公众号 | 检查发布链路 |

## 故障排查

| 问题 | 原因 | 处理方式 |
| --- | --- | --- |
| 找不到 Skill | 安装目录未复制成功 | 重新执行 `bash scripts/setup.sh` |
| 没有 `profile.yaml` | 初始化未完成 | 复制 `config/ip-profile-template.yaml` 到 `~/.ip-publisher/profile.yaml` |
| 热点抓取失败 | 上游依赖未拉取或网络异常 | 检查 `~/.ip-publisher/deps/wewrite` |
| 发布失败 | 平台未授权 | 先在对应平台完成授权 |
