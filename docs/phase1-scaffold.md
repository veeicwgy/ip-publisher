# Phase 1 Scaffold

## 目标

Phase 1 现在解决的是一条完整闭环，而不只是“出一版草稿”：

- 知识库驱动生成
- AI 友好结构编排
- 审核引擎
- 7 平台发布包
- Wechatsync 草稿同步就绪信息

默认仍然不托管账号密码，不做账号池。

## 入口命令

```bash
python3 -m ip_publisher.cli.run_phase1 \
  --request data/tasks/demo-request.json
```

## 产物

执行后会在 `outputs/<task_id>/` 下生成：

- `request.json`
- `draft.json`
- `audit_report.json`
- `publish_package.json`
- `article.md`
- `platforms/*.md`

## 模块边界

| 目录 | 责任 |
| --- | --- |
| `ip_publisher/kb` | 文档加载、标准化、切块、检索 |
| `ip_publisher/planner` | 关键词规划、热点合并、大纲生成 |
| `ip_publisher/generator` | 主稿生成、humanize、平台 payload |
| `ip_publisher/auditor` | grounding、关键词、结构、质量、平台规则审核 |
| `ip_publisher/publisher` | 发布包定义、Wechatsync 直发桥接信息 |
| `ip_publisher/workflows` | 串联 Phase 1 流程 |
| `ip_publisher/storage` | 产物写盘 |

## 审核门槛

Phase 1 会检查：

- 断言是否有来源
- 关键词是否命中标题 / 简介 / 正文
- 热点是否至少出现在标题 / 简介 / 正文之一
- 是否具备 H1 / H2 / H3、Q&A、对比表格、实体标注
- 可引用声明数、事实密度、权威信号数是否过线
- 各平台长度和格式是否合规

## 当前限制

- 检索先使用 `SQLite + FTS5`
- 当前 humanizer 是仓库内置轻量版，参考 Humanizer-zh 思路
- 当前直发推荐 Wechatsync，不做统一官方 API 聚合，也不支持账号密码直登
