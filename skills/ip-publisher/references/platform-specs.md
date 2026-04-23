# Platform Specs

7 平台发布包的格式规格，供生成 payload 时参考。

| 平台 | 文件名 | 格式 | 字数上限 | 备注 |
|---|---|---|---|---|
| 微信公众号 | `wechat_official.md` | HTML | 20,000 | 富文本，支持图片、分割线 |
| 小红书 | `xiaohongshu.md` | Markdown | 1,000 | 图文笔记，标题+正文+标签 |
| 知乎 | `zhihu.md` | Markdown | 5,000 | 支持 Markdown 渲染 |
| 掘金 | `juejin.md` | Markdown | 10,000 | 技术类读者，支持代码块 |
| CSDN | `csdn.md` | Markdown | 10,000 | 技术类读者，支持代码块 |
| 头条号 | `toutiao.md` | HTML | 5,000 | 富文本 |
| 微博 | `weibo.md` | 纯文本 | 140 | 无 Markdown，文件内无 `# 标题` |

## 注意事项

- 微博正文文件通常不含 `# 标题` 行，发布时需通过 `--title` 参数单独传入标题。
- 微信公众号和头条号为 HTML 格式，不能直接用 Markdown 渲染器预览。
- 小红书字数限制严格，正文需精简，重点在标签和视觉引导。
