---
name: multi-publisher
description: 多平台发布 Skill。Use for: 用户说发布文章、推送到某个平台、一键发布、同步内容到多个平台时。
---

# Multi Publisher

## Trigger when

- 用户说“发布文章”
- 用户说“推送到 XX 平台”
- 用户说“一键发布”
- 用户说“同步到多个平台”
- 用户说“先存草稿再发”

## Goal

基于 Wechatsync 封装发布流程，把文章与封面同步到用户选择的平台，并输出状态报告。

## Supported modes

- 草稿模式：推送到草稿箱，人工审核后发布
- 直发模式：直接发布，需提前授权

## Supported platforms

- 微信公众号（草稿箱）
- 知乎
- 微博
- 今日头条
- CSDN
- 掘金
- 小红书

## Output

| 平台 | 模式 | 状态 | 链接/备注 |
| --- | --- | --- | --- |
| 微信公众号 | draft | success | draft_id: xxx |

## Rules

- 若平台未授权，输出明确失败原因，不伪造成功。
- 若用户只想生成但不发布，终止在预发布检查。
- 若同一篇文章同步多个平台，保留每个平台的格式差异化版本。
