---
name: hotspot-fetcher
description: 热点抓取与筛选 Skill。Use for: 用户说抓取热点、今天有什么热门话题、给我看看热点、挑适合我的热点时。
---

# Hotspot Fetcher

## Trigger when

- 用户说“抓取热点”
- 用户说“今天有什么热门话题”
- 用户说“给我看看热点”
- 用户说“最近有什么值得写的”
- 用户说“给我筛几个适合我的选题”

## Goal

调用 wewrite 的热点抓取模块，按人设领域过滤，输出 Top 10 热点列表，包含来源、热度指数、与 IP 的结合建议。

## Data sources

- 微博热搜
- 知乎热榜
- 今日头条
- 36氪
- 微信热文

## Integration example

```python
from wewrite.hotspot import fetch_hotspots
hotspots = fetch_hotspots(domains=profile.core_values, limit=10)
```

## Output format

| 排名 | 热点标题 | 来源 | 热度指数 | 结合建议 |
| --- | --- | --- | --- | --- |
| 1 | 示例热点 | 微博 | 98 | 从 AI 产品经理视角切入 |

## Rules

- 优先保留与 `core_values` 高相关的话题。
- 若热点过泛，补充可执行切入角度。
- 若用户只要一个选题，返回 Top 3 即可。
