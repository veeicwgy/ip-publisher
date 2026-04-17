# ClawHub SEO Findings for IP Publisher

## Current page observations

- 当前标题为 `IP Publisher（个人IP内容自动化）`，对 `ip publisher` 有一定词法匹配，但对 `personal ip`、`ai content workflow`、`xiaohongshu`、`zhihu` 的首屏语义承载不足。
- 当前简介为英文一句话摘要，覆盖了 personal IP content creation 与 multi-platform publishing，但没有显式覆盖 `AI content workflow`、`Xiaohongshu`、`Zhihu`、`WeChat Official Account` 等更具体搜索词。
- 当前标签里已经出现 `wechat`、`xiaohongshu`、`zhihu`、`personal-ip`，说明页面层面已有部分关键词，但 SKILL.md 主体中的英文关键词密度仍明显不足。

## Local SKILL.md embedding analysis

- 当前 embedding 总长度约 2690 字符，远低于 12000 字符上限，不存在截断问题。
- 当前 `ip publisher` 仅出现 1 次，密度约 3.72 / 10K。
- 当前 `personal ip`、`ai content workflow`、`xiaohongshu`、`wechat official account`、`zhihu` 均几乎没有有效英文覆盖。
- `wechat` 仅出现 2 次，且主要落在 Wechatsync 依赖说明里，不足以支撑更广泛的搜索语义。
- slug 与 name 目前都能拆出 `ip` 与 `publisher` 词元，因此 `ip publisher` 具有一定 lexical boost，但其他目标词基本没有名称级加分。

## Main optimization direction

- 在 frontmatter 的 `name` 与 `description` 中补足主搜索词与平台词。
- 在 README 主体前半段增加英文/双语表达，尤其是 `personal IP content workflow`、`AI content workflow`、`Xiaohongshu`、`WeChat Official Account`、`Zhihu`。
- 增加更强的安装转化段落，例如 who-it-is-for、what-you-get、installation trigger、platform coverage 与 search-friendly examples。
- 保持安全边界与依赖声明不弱化，避免为了 SEO 牺牲 OpenClaw 风险判定结果。

## After optimization snapshot

- embedding 长度从约 2690 提升到约 4184，仍明显低于 12000 字符上限。
- `ip publisher` 从 1 次提升到 5 次，并进入 `name` 与 `description`。
- `personal ip` 从 0 次提升到 8 次，并进入 `name` 与 `description`。
- `ai content workflow` 从 0 次提升到 6 次，并进入 `name` 与 `description`。
- `xiaohongshu`、`wechat official account`、`zhihu` 都已进入 `description` 与主体正文，平台覆盖表达明显增强。
- `name` 现在可直接提供 `ip publisher`、`personal ip`、`ai content workflow` 的词元级 lexical 支撑，但 `xiaohongshu`、`wechat`、`zhihu` 仍主要依赖向量语义匹配而不是名称级匹配。

### Live verification after publishing v1.0.2

新版 `v1.0.2` 已出现在详情页，显示名称为 `IP Publisher（Personal IP AI Content Workflow）`，标签中已包含 `ip-publisher`、`personal-ip`、`ai-content-workflow`、`wechat`、`xiaohongshu`、`zhihu`。当前安全扫描状态仍为 `VirusTotal Pending`。

在列表页以 `ip publisher` 进行搜索时，结果页显示约 25 个相关技能，但当前首屏结果中尚未看到本 Skill。这意味着页面内容优化已经生效到详情页，但列表检索侧很可能仍受 **索引刷新延迟**、**安全扫描未完成导致可见性受限** 或 **当前相关性排序竞争较强** 的影响，安装转化改善需要等扫描完成并继续做二轮验证。

进一步在列表页使用精确关键词 `ip-publisher` 搜索时，本 Skill 已出现在结果首位，说明 **slug 级检索** 与 **品牌词连字符写法** 已经生效。与之相比，空格写法 `ip publisher` 仍未在首屏稳定出现，说明后续若要继续提升自然搜索曝光，需要进一步增强摘要前段对空格写法和高频使用场景的覆盖，并等待平台索引刷新完成。
在列表页使用 `personal ip` 搜索时，当前首屏结果主要被 IP 地址、IP 查询类技能占据，本 Skill 未进入首屏。这说明虽然详情页文案已经覆盖 `personal IP`，但该词在 ClawHub 中存在强同形竞争，短期内不适合作为主拉新词，后续更应依赖 `ip-publisher`、`xiaohongshu publisher`、`wechat publisher`、`zhihu publisher` 等更具意图约束的组合词获取曝光。

在 `xiaohongshu publisher` 搜索下，结果页高度拥挤，首屏几乎全部是专门面向小红书发布的垂直技能，本 Skill 当前未进入首屏。这说明平台词补充有助于相关性建立，但如果要靠平台词抢安装量，仍需进一步把摘要前半段做得更像“Xiaohongshu / WeChat / Zhihu publisher with full workflow”，而不只是“personal IP workflow”。

在 `wechat publisher` 与 `zhihu publisher` 搜索下，本 Skill 当前同样未进入首屏，首屏被更窄、更强动作导向的专门发布技能占据，例如直接写明 `WeChat Publisher`、`Zhihu Post`、`Auto Publisher` 的条目。这进一步说明：

1. 当前版本已经把 **品牌词检索** 做到了可命中；
2. 但在 **平台发布意图词** 上，摘要前半段的动作表达仍然不够强；
3. 若目标是提升安装量，而不仅是被搜到，下一版应把标题或摘要第一句进一步收敛为“为小红书 / 微信公众号 / 知乎生成并准备发布内容”，把 `workflow` 放到后半段，而不是继续把 `personal IP` 置于最前。

