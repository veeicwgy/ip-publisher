# IP Publisher

<p align="right"><strong>简体中文</strong> | <a href="./README.en.md">English</a></p>

<p align="center"><img src="assets/logo.webp" alt="IP Publisher Logo" width="520"></p>

> 一个面向个人 IP 运营者的内容生产工作流仓库。
> 它现在最真实的价值，不是“替你一键发完所有平台”，而是把选题、人设、改写、去模板感和**发布包生成**串成一条可复用链路。

<p align="center">
  <a href="https://ippublisher-lwukxvsq.manus.space">官网</a> ·
  <a href="https://github.com/veeicwgy/ip-publisher">GitHub 仓库</a> ·
  <a href="./README.en.md">English README</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/veeicwgy/ip-publisher?style=social)](https://github.com/veeicwgy/ip-publisher/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/veeicwgy/ip-publisher?style=social)](https://github.com/veeicwgy/ip-publisher/network/members)

> 如果这个项目对你有帮助，欢迎点一个 **Star**。我会优先把它继续补成更扎实的创作者工作流，而不是继续堆看起来很满、实际不可验证的承诺。

---

## 我为什么做这个仓库

我自己在做个人 IP 内容时，真正卡住的从来不是“不会写”，而是下面这些重复劳动：今天有什么值得写，哪个角度更像我，公众号和小红书到底要怎么改，写完以后怎样少一点模板感，最后又该怎么整理成可以发布的版本。

所以我把仓库的定位收窄了：**先把内容生产链路理顺，再把发布准备做扎实**。如果你期待的是“登录所有平台后一键代发”，这个版本还不是；如果你需要的是一套能重复使用的内容工作流、可核对的平台规则、和一份可以直接交给自己或运营同事继续发布的内容包，它已经能帮上忙。

---

## 现在仓库里哪些东西是真实可运行的

| 交付物 | 现在能做什么 | 文件位置 |
| --- | --- | --- |
| 安装脚本 | 拉取依赖、初始化人设配置、把 Skill 安装到 Claude / OpenClaw | `scripts/setup.sh` |
| 发布包生成脚本 | 读取 `config/platforms.yaml`，输出多平台 Markdown / JSON 发布包 | `scripts/generate-publish-pack.py` |
| 平台规则配置 | 提供 7 个平台的篇幅、封面比例、标签数量等硬规则 | `config/platforms.yaml` |
| 人设模板 | 提供可落地的本地 `profile.yaml` 结构 | `config/ip-profile-template.yaml` |
| 示例输出 | 提供公众号、小红书、知乎、CSDN 的真实示例文案 | `examples/` |

---

## 我会怎么用它

我通常会先把自己的职业、受众和常写的话题填进 `profile.yaml`，然后用主 Skill 跑一遍“找角度 -> 写草稿 -> 去模板感 -> 生成封面建议”的流程。到了最后一步，我不会让它假装“已经帮我发出去”，而是直接用发布包脚本把标题、正文、标签和平台检查结果整理出来，再手动进各平台后台做最后确认。

这套方法对我最大的帮助，是把“写完一篇再临时改七遍”的混乱状态，改成“先有统一母稿，再按平台拆包”。仓库里的 `examples/article-output-wechat.md`、`examples/article-output-xiaohongshu.md` 和 `examples/article-output-zhihu.md`，就是按这个思路留下来的样例。

---

## 内容输出示例

下面这张图展示的是当前仓库希望交付的结果形态：不是虚构的自动发布成功页，而是一套更接近真实运营流程的内容工作台与结果预览。

<p align="center"><img src="assets/one-click-demo.png" alt="IP Publisher 内容输出示例" width="980"></p>

---

## 3 分钟跑通

### 1) 克隆仓库

```bash
git clone https://github.com/veeicwgy/ip-publisher.git
cd ip-publisher
```

### 2) 初始化依赖与人设文件

```bash
bash scripts/setup.sh
```

### 3) 生成一份真实的发布包

```bash
python3 scripts/generate-publish-pack.py \
  --platform xiaohongshu wechat_official zhihu \
  --title "为什么我先把内容链路跑顺，再谈更大的自动化" \
  --angle "个人 IP 更需要稳定输出，而不是看起来很全的自动化" \
  --body-file examples/article-output-wechat.md \
  --tags 个人IP,内容工作流,多平台改写
```

运行后会在 `outputs/` 下得到一份 Markdown 发布包和一份 JSON 清单，方便你继续人工审阅、复制或接入自己的后续流程。

如果你想先看官网说明，也可以直接访问 [IP Publisher 官网](https://ippublisher-lwukxvsq.manus.space)。

---

## 这个仓库适合什么场景

| 场景 | 更适合你的原因 |
| --- | --- |
| 个人 IP 运营 | 先统一人设、语气和主题边界，再持续输出 |
| 一稿多平台改写 | 用平台规则把同一个主题拆成不同版本 |
| 团队协作前的内容准备 | 先生成结构化发布包，再交给编辑或运营复核 |
| 想降低 AI 模板感 | 把“先有观点，再做润色”这件事变成固定流程 |

---

## 当前能力边界

| 模块 | 当前状态 | 说明 |
| --- | --- | --- |
| 热点发现 | 可通过 Skill 编排公开网页搜索与筛选 | 目前不是独立仓库脚本 |
| 平台改写 | 可通过 Skill 生成不同平台草稿 | 依赖 Claude / OpenClaw 执行 |
| 去模板感处理 | 可通过 `humanizer` 子技能完成 | 当前更偏工作流编排 |
| 封面生成 | 可输出封面 brief，具备图像生成链路 | 依赖运行环境支持 |
| 多平台发布 | 默认生成发布包与预检结果 | 不伪造“已自动发布成功” |
| 真正自动代发 | 还没有 | 未来若接平台 API 再单独说明 |

---

## 支持的平台规则

| 平台 | 适合内容 | 封面比例 | 推荐标签数 |
| --- | --- | --- | --- |
| 小红书 | 情绪表达、经验分享、种草笔记 | `1:1` | 8 |
| 知乎 | 观点分析、问答长文 | `16:9` | 5 |
| 微信公众号 | 叙事型长文、品牌沉淀 | `2.35:1` | 0 |
| CSDN | 技术教程、实操复盘 | `16:9` | 6 |
| 微博 | 热点短评、即时表达 | `none` | 2 |
| 今日头条 | 热点扩写、大众议题 | `16:9` | 5 |
| 掘金 | 技术总结、工程实践 | `16:9` | 5 |

---

## 更诚实的常用触发词

```text
帮我先找适合我的热点，再写一篇公众号草稿
把这篇母稿拆成知乎和小红书两个版本
帮我把文章去掉一点 AI 味，再出一个封面 brief
为这篇内容生成一份多平台发布包，不直接代发
```

---

## 仓库结构

```text
config/      平台规则、人设模板、热点来源
examples/    真实示例输出
scripts/     安装脚本、依赖脚本、发布包生成脚本
skills/      主流程与子技能编排
assets/      README 展示图
```

---

## License

本项目采用 [MIT License](LICENSE)。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=veeicwgy/ip-publisher&type=Date)](https://star-history.com/#veeicwgy/ip-publisher&Date)
