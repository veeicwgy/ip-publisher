# Platform Support

## 仓库默认平台 bundle

IP Publisher 现在把平台口径固定成一个 canonical bundle，而不是 README、Skill、脚本各说各话。

默认 bundle：

- `wechat_official`
- `xiaohongshu`
- `zhihu`
- `juejin`
- `csdn`
- `toutiao`
- `weibo`

## 为什么是这 7 个

- 覆盖中文内容运营里最常见的长文、问答、技术社区和热点导流场景
- 同时兼顾品牌传播和技术内容
- 都能映射到 [Wechatsync](https://github.com/wechatsync/Wechatsync) 适配器
- 适合“一次生成，多平台改写，再统一审稿”的低门槛工作流

## 平台矩阵

| 平台 | 角色 | 默认格式 | 长度上限 | 标签建议 | 直发方式 |
| --- | --- | --- | --- | --- | --- |
| 微信公众号 | 品牌长文 / 深度文章 | `html` | 20000 | 0 | Wechatsync 草稿同步 |
| 小红书 | 推荐帖 / 短内容 | `markdown` | 1000 | 8 | Wechatsync 草稿同步 |
| 知乎 | 问答 / 观点长文 | `markdown` | 5000 | 5 | Wechatsync 草稿同步 |
| 掘金 | 技术实践 / 开发者文章 | `markdown` | 10000 | 5 | Wechatsync 草稿同步 |
| CSDN | 教程 / 排障 | `markdown` | 10000 | 6 | Wechatsync 草稿同步 |
| 头条号 | 热点扩写 / 泛流量内容 | `html` | 5000 | 5 | Wechatsync 草稿同步 |
| 微博 | 摘要导流 | `text` | 140 | 2 | Wechatsync 草稿同步 |

## 和 Wechatsync 29+ 平台是什么关系

Wechatsync 当前支持 29+ 平台，这对后续扩展很有价值。  
但仓库默认只把上面 7 个平台定义成标准输出，原因是：

- 这是当前运营最常用的一组
- 这组平台足够覆盖长文、问答、技术、热点和短摘要
- 第一次接入 ClawHub 或运营团队时，7 平台更容易管理和验收

后续如果要扩到更多平台，可以继续沿用 `ip_publisher/config/platform_rules.yaml` 和 `config/platforms.yaml` 的结构追加。
