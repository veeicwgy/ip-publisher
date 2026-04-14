---
name: ip-profile
description: IP 人设定义与更新 Skill。Use for: 用户说设置我的 IP、更新人设、我是一个什么类型的人、保存写作风格时。
---

# IP Profile

## Trigger when

- 用户说“设置我的 IP”
- 用户说“更新人设”
- 用户说“我是一个 XX”
- 用户说“帮我保存我的写作风格”
- 用户说“给我建个人设档案”

## Goal

引导用户完成 IP 人设配置向导，并将结果保存到 `~/.ip-publisher/profile.yaml`。

## Wizard flow

1. 询问 IP 名称或笔名。
2. 询问职业或领域，例如产品经理、AI 研究者、独立开发者。
3. 询问 3-5 个性格特征。
4. 询问写作风格，如接地气、有数据支撑、观点鲜明。
5. 询问目标受众。
6. 询问核心价值观与擅长话题。
7. 询问禁忌话题。
8. 询问 2-3 个代表性金句，用于学习个人语气。
9. 询问常用发布平台。

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

## Output

- 完整的人设 YAML
- 一段 100 字以内的人设摘要
- 推荐优先使用的平台
