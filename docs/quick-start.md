# Quick Start

## 目标

在本地完成安装后，实现以下最短链路：

```text
git clone -> bash scripts/setup.sh -> python3 scripts/quickstart.py -> 生成三平台发布包
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

### 3. 运行交互式 quickstart

```bash
python3 scripts/quickstart.py
```

脚本会直接问你几个问题，例如：

```text
你想改写的主题是什么？
你最想强调的核心观点是什么？
你希望主要写给谁看？
目标平台是什么？
```

答完以后，你会在 `outputs/` 下看到：

| 文件 | 作用 |
| --- | --- |
| `*.md` | 直接审阅、复制、协作 |
| `*.json` | 继续接入你自己的流程或脚本 |

## 推荐首条动作

| 动作 | 目的 |
| --- | --- |
| 直接跑 `python3 scripts/quickstart.py` | 最快看到三平台结果 |
| 复用 `~/.ip-publisher/profile.yaml` | 让改写更像你自己的语气 |
| 用 `scripts/generate-publish-pack.py` | 适合脚本化生成发布包 |
| 把结果交给编辑或运营复核 | 发挥“发布包先于代发”的优势 |

## 故障排查

| 问题 | 原因 | 处理方式 |
| --- | --- | --- |
| 找不到 Skill | 安装目录未复制成功 | 重新执行 `bash scripts/setup.sh` |
| 没有 `profile.yaml` | 初始化未完成 | 复制 `config/ip-profile-template.yaml` 到 `~/.ip-publisher/profile.yaml` |
| quickstart 无法生成文件 | Python 依赖未装好 | 重新执行 `bash scripts/setup.sh` |
| 发布包不符合预期 | 主题或角度太空泛 | 在 quickstart 中补充更具体的核心观点 |
| 没有自动发布 | 当前默认就是发布包模式 | 先人工审阅，再决定是否接你自己的发布链路 |
