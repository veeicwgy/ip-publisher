# Contributing to IP Publisher

感谢你关注 **IP Publisher**。本仓库欢迎针对 Skill 编排、平台配置、提示词工程、安装脚本和文档的改进。

## 贡献范围

| 类型 | 欢迎内容 | 暂不接受 |
| --- | --- | --- |
| Skill 改进 | 触发词覆盖、流程稳定性、输出模板优化 | 与项目定位无关的泛用 Skill |
| 平台适配 | 新平台配置、字段对齐、发布模式补充 | 未验证的闭源接口脚本 |
| 文档 | 快速开始、案例、参数说明 | 与代码无关的宣传文案堆砌 |
| 脚本 | 安装、测试、校验脚本增强 | 破坏现有目录结构的重构 |

## 贡献流程

1. Fork 本仓库并创建分支：`feat/xxx`、`fix/xxx` 或 `docs/xxx`。
2. 修改后确保 `bash scripts/test-run.sh` 能通过基础校验。
3. 在 Pull Request 中说明变更目的、影响范围和验证结果。

## Pull Request Checklist

- [ ] 没有改变主流程核心定位
- [ ] 新增或修改的 Skill 触发词包含中文口语表达
- [ ] 文档与配置保持一致
- [ ] 示例输出与平台调性匹配
- [ ] 安装脚本不会覆盖用户已有 `profile.yaml`

## Commit Message Convention

| 前缀 | 用途 |
| --- | --- |
| `feat:` | 新功能或新平台支持 |
| `fix:` | Bug 修复 |
| `docs:` | 文档更新 |
| `refactor:` | 不改变功能的结构调整 |
| `test:` | 测试与校验增强 |

## 如何提交新平台支持

新增平台时，请同时修改以下文件：

- `config/platforms.yaml`
- `skills/article-generator/SKILL.md`
- `skills/multi-publisher/SKILL.md`
- `docs/platform-guide.md`
- 至少一个 `examples/` 示例文件

## Issue 模板建议

提交 Issue 时，请尽量说明以下信息：

- 使用的 Skill 名称
- 目标平台
- 输入指令示例
- 实际输出与预期输出的差异
- 是否已完成 `setup.sh`

欢迎提交改进建议，也欢迎基于真实内容生产场景反馈问题。
