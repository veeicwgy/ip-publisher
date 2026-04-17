# IP Publisher

## 一句话描述

帮你把一个话题改写成小红书、公众号、知乎三个版本，一键生成发布包。

## 功能亮点

1. 一个主题直接拆成小红书、公众号、知乎三平台版本。
2. 先有人设与角度，再做平台改写，减少内容跑偏。
3. 支持 Markdown / JSON 双格式发布包，便于人工审阅与团队协作。
4. 可继续串联去 AI 味、封面 brief 和发布预检流程。
5. 默认不伪造自动代发成功，结果更安全也更容易复核。

## 安装方法

1. `git clone https://github.com/veeicwgy/ip-publisher.git && cd ip-publisher`
2. `bash scripts/setup.sh`
3. `python3 scripts/quickstart.py`

## 示例触发词

- 把这个话题改写成小红书、公众号、知乎三个版本
- 为这篇母稿一键生成发布包
- 给我一份可审阅的 Markdown 和 JSON 发布包
- 帮我准备小红书和公众号版本
- 把这篇内容改成更适合知乎发布的版本

## 集成开源项目列表

- `Wechatsync`（仅在用户本地已配置时用于后续发布链路）
- `OpenClaw / Claude Code Skills`
- 仓库内置的 `quickstart.py` 与 `generate-publish-pack.py`

## 截图 / 演示 GIF 说明

建议展示以下 3 组演示内容：

1. 终端里运行 `python3 scripts/quickstart.py` 的问答过程。
2. 同一主题输出小红书版与公众号版的对比结果。
3. Markdown / JSON 发布包文件与人工审阅场景。
