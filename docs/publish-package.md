# Publish Package

## 发布包是什么

发布包不是“已经发出去了”的结果，而是一份 **审核通过后可进入分发** 的结构化交付物。

当前发布包由两部分组成：

1. 人可以直接审阅的 `article.md`
2. 系统可以直接消费的 `publish_package.json`

## `publish_package.json` 包含什么

- `package_version`
- `publisher`
- `audit_gate`
- `review_checklist`
- `publisher_notes`
- `platform_payloads`

其中 `platform_payloads` 里会按平台输出：

- `title`
- `summary`
- `body_markdown`
- `format`
- `tags`
- `cover_brief`
- `direct_publish`
- `checks`

## 直发字段怎么理解

`direct_publish` 不是“已经发布成功”，而是：

- 是否支持直发
- 通过什么桥接方式直发
- 默认是不是草稿
- 对应的适配器 ID
- 如果走 Wechatsync，应执行什么命令

示例：

```json
{
  "supported": true,
  "via": "wechatsync",
  "draft_only": true,
  "adapter": "weixin",
  "cli_example": "wechatsync sync outputs/<task_id>/platforms/wechat_official.md -p weixin"
}
```

## 为什么不直接接账号密码

- 平台差异大，官方公开 API 并不统一
- 账号密码直登风险高，也不适合放进仓库或 ClawHub 运行时
- [Wechatsync](https://github.com/wechatsync/Wechatsync) 已经验证了更低门槛的方式：用浏览器已登录态和平台 Web API 走草稿同步

所以仓库当前推荐路径是：

1. 生成文章
2. 通过审核
3. 输出发布包
4. 如已准备好浏览器登录态，再进入 Wechatsync 草稿同步

## 什么时候允许进入发布

只有满足以下条件，才应该进入发布：

- `audit_report.status == pass`
- 平台 payload 都在格式和长度限制内
- 关键词和热点命中标题 / 简介 / 正文
- 关键声明都能回溯到知识库 chunk
- 人工终审已经确认
