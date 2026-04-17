# ClawHub 风险复核记录

## 当前线上页面暴露的主要问题

| 风险点 | 线上表现 | 对应处置 |
| --- | --- | --- |
| 默认本地持久化用户画像 | 线上 `skills/ip-publisher/SKILL.md` 写明检查并写入 `~/.ip-publisher/profile.yaml` | 改为仅在用户明确同意时才落盘，默认使用会话态 |
| 自动发布表述过强 | 线上写明调用 wechatsync 推送至多个平台并输出发布状态 | 改为默认输出手动发布包，只有在用户明确授权且本地插件/登录条件满足时才尝试执行 |
| 依赖与接口未声明充分 | 线上未清晰声明热点来源、发布依赖、凭证边界 | 新增外部依赖表和安全边界章节 |
| 旧模块名与现状不一致 | 线上仍出现 wewrite、baoyu-cover-image 等旧描述 | 改为引用仓库内实际子 Skill 名称与当前限制 |

## 复核目标

重新发布后重点确认 ClawHub 页面中的 `skills/ip-publisher/SKILL.md` 已显示新版安全边界、依赖声明与真实发布限制。

## 重新发布后状态

| 项目 | 当前结果 |
| --- | --- |
| ClawHub 页面 | `https://clawhub.ai/veeicwgy/ip-publisher` |
| 当前版本 | `v1.0.1` |
| 文件体积 | `SKILL.md 5.7 KB`，`prompt.md 1.1 KB` |
| 发布结果 | 页面已出现 `Published ip-publisher@1.0.1` |
| 安全扫描状态 | 当前为 `Security scan in progress`，VirusTotal 仍显示 `Pending` |
| 旧风险文案 | 当前页面已不再展示旧版 `Suspicious / medium confidence` 提示，但最终结论仍需等待扫描完成后复核 |
