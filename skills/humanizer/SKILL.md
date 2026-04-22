---
name: humanizer
description: 中文去 AI 味 Skill。Use for: 用户说去掉 AI 味、像人写的、口语一点、别那么机器化时。
---

# Humanizer

## Trigger when

- 用户说“去掉 AI 味”
- 用户说“让这篇更像人写的”
- 用户说“口语一点”
- 用户说“别那么像模型写的”
- 用户说“帮我润色得自然一点”

## Goal

参考 Humanizer-zh 的思路，对中文内容做专项去 AI 味处理，并从 `profile.yaml` 的 `tone_examples` 中注入个人语气。仓库默认内置的是轻量 humanizer，目标是降低门槛，不在第一步就引入复杂外部依赖。

## Processing rules

- 替换常见 AI 套话黑名单中的表达
- 删除“首先、其次、最后、总的来说、值得注意的是”等模板词
- 打散过于工整的并列句式
- 增加个人判断、语气词和真实感细节
- 如果用户有人设金句，优先模仿其节奏和语气

## Integration hint

- 优先读取 `tone_examples`
- 若无金句样本，则从 `personality` 与 `writing_style` 反推语气
- 若处在仓库模式中，可把它放在“知识库主稿生成”和“发布包输出”之间

## Output

- 处理后的正文
- 关键改写说明
- 保留原文核心观点，不改立场
