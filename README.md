# IP Publisher

<p align="right"><strong>简体中文</strong> | <a href="./README.en.md">English</a></p>

<p align="center"><img src="assets/logo.webp" alt="IP Publisher Logo" width="520"></p>

> 帮你把一个话题改写成 **小红书、公众号、知乎** 三个版本，并一键生成可审阅、可复制、可协作的 **发布包**。

<p align="center">
  <a href="https://clawhub.ai/veeicwgy/ip-publisher"><strong>👉 Install from ClawHub</strong></a> ·
  <a href="https://ippublisher-lwukxvsq.manus.space">官网</a> ·
  <a href="https://github.com/veeicwgy/ip-publisher">GitHub 仓库</a>
</p>

---

## 30 秒先看懂它能给你什么

| 你会看到什么 | 最短动作 | 最终得到什么 |
| --- | --- | --- |
| 一张结果预览图 | 打开下方示意图 | 先理解它不是“假装代发”，而是把三平台内容和发布信息整理好 |
| 一条命令 | `python3 scripts/quickstart.py` | 回答几个问题，直接生成多平台发布包 |
| 两个输出文件 | `outputs/*.md` + `outputs/*.json` | Markdown 便于人工审阅，JSON 便于继续接流程或二次处理 |

<p align="center"><img src="assets/one-click-demo.png" alt="IP Publisher 内容输出示意" width="980"></p>

我把这个仓库继续收窄以后，核心价值终于变得很清楚：**不是替你偷偷登录后台代发，而是把“同一话题拆成三种平台表达 + 整理成发布包”这件事做得更直给。** 这样更安全，因为你可以终审；也更适合团队协作，因为编辑、运营、作者都能看同一份结果。

---

## 现在就能跑通的方式

```bash
git clone https://github.com/veeicwgy/ip-publisher.git
cd ip-publisher
bash scripts/setup.sh
python3 scripts/quickstart.py
```

运行 `python3 scripts/quickstart.py` 之后，脚本会直接问你几个问题，例如：

```text
你想改写的主题是什么？
你最想强调的核心观点是什么？
你希望主要写给谁看？
目标平台是什么？
```

答完以后，它会直接生成：

| 文件 | 用途 |
| --- | --- |
| `outputs/*.md` | 给人直接看，适合审稿、复制、协作 |
| `outputs/*.json` | 给后续脚本、系统或自定义流程继续处理 |

---

## 同一个话题，三种平台会怎么变

我把 README 里最重要的价值前置成一个直观对比：同样是“**为什么我先把内容流程跑顺，再谈自动化**”，写法会完全不同。

| 平台 | 典型长度与语气 | 结果感 |
| --- | --- | --- |
| 小红书 | 约 200 字，短句、emoji、评论区互动、标签收口 | 适合快速吸引注意力 |
| 公众号 | 约 800 字，叙事展开、层次完整、结尾能承接转化 | 适合建立长期观点与信任 |
| 知乎 | 介于两者之间，更强调“先说结论 + 再给论证” | 适合回答型和观点型表达 |

### 小红书版

> 🌟 最近我一直在想「为什么我先把内容流程跑顺，再谈自动化」这件事。  
> 😵 真正让我卡住的，不是不会写，而是每个平台都要重写一次。  
> 🧭 我现在更稳的做法，是先把母稿讲清楚，再去拆小红书、公众号和知乎版本。  
> ✍️ 这样做最大的好处，不是省 5 分钟，而是内容终于不会越改越散。  
> 如果你也在做内容，你现在最卡的是选题、改写，还是发布？  
> #内容工作流 #小红书运营 #发布包

### 公众号版

> 最近我反复在想一件事：内容自动化之所以让很多人焦虑，不是因为工具不够多，而是因为每次动笔前都要重新决定角度、结构和平台。  
> 我现在更认可的判断是，先把母稿写清楚，再把改写和发布整理成可复用的后半段流程。这样做最直接的好处，是我不会再为了同一个话题来回重写三遍。  
> 这也是我为什么保留发布包这个中间结果。它让标题、正文、标签和封面建议都能先被审阅，再决定是否真的发出去。对于个人 IP 或小团队来说，这反而比直接代发更安全，因为你知道每个平台最终出现的到底是什么。

如果你想直接看仓库里的现成样例，也可以打开 `examples/article-output-xiaohongshu.md`、`examples/article-output-wechat.md` 和 `examples/article-output-zhihu.md`。

---

## 我为什么把“发布包不是代发”写成优势

| 方式 | 优点 | 代价 |
| --- | --- | --- |
| 直接代发 | 看起来更自动化 | 容易误发、难审阅、团队协作不透明 |
| 先生成发布包 | 更安全、可复核、适合多人协作，也方便继续接你自己的工具链 | 需要最后一步人工确认 |

所以这个仓库现在的承诺非常直接：**帮你改写内容，并把标题、正文、标签、封面建议整理成一份可交付结果。** 如果以后真的补了平台 API 或稳定代发链路，我会单独把那部分作为新的能力写清楚，而不是混在 README 里提前承诺。

---

## 现在仓库里哪些东西是真实可运行的

| 交付物 | 现在能做什么 | 文件位置 |
| --- | --- | --- |
| 安装脚本 | 初始化依赖、人设配置与本地 Skill 目录 | `scripts/setup.sh` |
| 交互式 quickstart | 问几个问题，直接生成三平台发布包 | `scripts/quickstart.py` |
| 发布包生成脚本 | 把一个话题改写成多平台版本，并输出 Markdown / JSON | `scripts/generate-publish-pack.py` |
| 平台规则配置 | 提供 7 个平台的长度、封面比例、标签规则 | `config/platforms.yaml` |
| 人设模板 | 提供本地 `profile.yaml` 的字段结构 | `config/ip-profile-template.yaml` |
| 示例内容 | 提供小红书、公众号、知乎、CSDN 的样例文案 | `examples/` |

---

## 适合谁用

| 场景 | 为什么适合 |
| --- | --- |
| 个人 IP 创作者 | 同一主题要反复改写成多个平台版本 |
| 小团队内容协作 | 作者、编辑、运营需要先看一份统一结果 |
| 想先把流程跑顺的人 | 不急着接 API，但想先把改写和整理做扎实 |
| 需要可复制输出的人 | 希望结果能落成 Markdown / JSON，而不是只停在聊天记录里 |

---

## 当前能力边界

| 模块 | 当前状态 | 说明 |
| --- | --- | --- |
| 话题改写 | 已可通过脚本生成小红书、公众号、知乎版本 | 默认走平台模板化改写 |
| 发布包整理 | 已可用 | 同时输出 Markdown 与 JSON |
| 人设配置 | 已可用 | 可复用本地 `~/.ip-publisher/profile.yaml` |
| 热点发现 | 主要由 Skill 工作流完成 | 当前仓库脚本不单独抓热点 |
| 自动代发 | 默认关闭 | 不伪造已发布成功 |

---

## 仓库结构

```text
assets/      README 展示图
config/      平台规则、人设模板、热点来源
docs/        补充说明与复盘文档
examples/    示例文章与示例发布包
scripts/     安装脚本、quickstart、发布包生成脚本
skills/      主流程与子技能编排
```

---

## License

本项目采用 [MIT License](LICENSE)。
