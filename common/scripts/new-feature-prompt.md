# 新功能开发 Prompt 模版

> 每次开发新功能时，用这个模版给 Claude 下指令。
> 好的指令 = 好的代码。

---

## 模版（填写后发给 Claude）

```
我要实现一个新功能，请按照项目的 Harness Engineering 规范来开发。

## 功能描述
[用 1-3 句话描述这个功能是什么，解决什么问题]

## 涉及的业务概念
- 实体: [哪些 Entity 会被创建/修改/查询]
- 业务规则: [有哪些约束条件]
- 触发场景: [什么情况下触发]

## 期望的 API / 界面
[如果是 API：写出 endpoint、请求体、响应体的大致样子]
[如果是 UI：描述页面上有什么，用户能做什么]

## 不需要做的事（Non-goals）
[明确说明这次不做什么，防止 Claude 过度实现]

## 开发步骤要求
请按以下顺序实现：
1. 先在 docs/domain-model.md 里更新或新增相关实体描述
2. 在 types/ 定义类型
3. 实现 Repository 层（如需数据库操作）
4. 实现 Service 层（业务逻辑）
5. 实现 API 层（参数验证 + 调用 Service）
6. 实现 UI 层（如需要）
7. 为 Service 和 API 层写测试
8. 运行 make check / npm run check 确认通过

## 完成标准
- [ ] lint + typecheck 通过
- [ ] 关键路径有测试
- [ ] domain-model.md 已更新
- [ ] 没有违反 docs/golden-principles.md 中的任何规则
```

---

## 示例（填写后的样子）

```
我要实现一个新功能，请按照项目的 Harness Engineering 规范来开发。

## 功能描述
用户可以收藏文章，收藏后可以在"我的收藏"页面看到所有收藏过的文章。

## 涉及的业务概念
- 实体: User（已有）、Article（已有）、Bookmark（新增）
- 业务规则: 同一篇文章只能收藏一次；未登录用户不能收藏
- 触发场景: 用户点击文章旁边的"收藏"按钮

## 期望的 API
POST /api/bookmarks  { articleId: string }  → 201 Created
DELETE /api/bookmarks/:articleId  → 204 No Content
GET /api/bookmarks  → { bookmarks: Bookmark[] }

## 不需要做的事
- 不需要收藏夹分类
- 不需要分享收藏夹
- 不需要收藏数量统计

## 完成标准（同上）
```
