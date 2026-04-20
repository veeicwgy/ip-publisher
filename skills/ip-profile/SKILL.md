---
name: ip-profile
description: IP 人设整理 Skill。Use for: 用户说设置我的 IP、更新人设、整理写作风格、输出结构化 profile 时。默认返回对话内 YAML，不自动保存到本地文件。
---

# IP Profile

## Trigger when

- 用户说“设置我的 IP”
- 用户说“更新人设”
- 用户说“帮我整理写作风格”
- 用户说“给我建个人设档案”
- 用户说“把我的信息整理成 profile”

## Goal

引导用户完成 IP 人设配置向导，并输出结构化 YAML 与简短摘要，便于后续继续写作或人工保存。默认行为是**在对话中返回结果**，不是自动写入本地路径。

## Wizard flow

1. 询问 IP 名称或笔名。
2. 询问职业或领域。
3. 询问 3-5 个性格特征。
4. 询问写作风格。
5. 询问目标受众。
6. 询问核心价值观与擅长话题。
7. 询问禁忌话题。
8. 询问 2-3 个代表性金句。
9. 询问常用平台。

## YAML schema

```yaml
ip_profile:
  name: ""
  profession: ""
  personality: []
  writing_style: ""
  target_audience: ""
  core_values: []
  taboo_topics: []
  tone_examples: []
  preferred_platforms: []
```

## File boundary

只有当用户明确要求“保存到本地配置”或“导出为文件”时，才可以继续讨论本地落盘方案。在未获明确授权前，不要把本地保存当作默认目标。

## Output

- 完整的人设 YAML
- 一段 100 字以内的人设摘要
- 推荐优先使用的平台
- 若用户明确要求导出，再单独说明可选保存路径与注意事项
