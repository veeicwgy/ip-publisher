# Phase 1 Scaffold

## 目标

第一阶段只解决三件事：

- 知识库驱动生成
- 审核引擎
- Markdown / JSON 交付

默认不做自动发布，也不管理账号密码。

## 入口命令

```bash
python3 -m ip_publisher.cli.run_phase1 \
  --request data/tasks/demo-request.json
```

## 产物

执行完成后会在 `outputs/<task_id>/` 下生成：

- `request.json`
- `draft.json`
- `audit_report.json`
- `article.md`

## 模块边界

| 目录 | 责任 |
| --- | --- |
| `ip_publisher/kb` | 文档加载、标准化、切块、检索 |
| `ip_publisher/planner` | 关键词规划、热点合并、大纲生成 |
| `ip_publisher/generator` | 草稿生成、引用映射、平台改写 |
| `ip_publisher/auditor` | 事实锚定、关键词、结构、平台规则审核 |
| `ip_publisher/workflows` | 串联 Phase 1 流程 |
| `ip_publisher/storage` | 产物写盘 |

## 当前限制

- 检索先使用 `SQLite + FTS5`
- 生成器当前是 grounded scaffold，不是最终生产级写作器
- 审核优先做“有无来源、关键词是否命中、是否符合大纲和平台规则”
