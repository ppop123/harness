# 业务领域模型（完整示例：在线书店）

> 本文件是项目的"业务词典"。AI agent 在处理任何业务逻辑前必须先读本文件。
> 每当新增一个业务概念（实体、服务、流程），必须同步更新此文件。
>
> **这是一个填写完整的示例**，展示一个"在线书店"项目的领域模型。
> 实际使用时，复制 `domain-model.md`（空模板）并参考本文件填写。

---

## 项目概述

```
项目: BookHive
核心业务: 在线图书销售平台，支持搜索、购买、评价图书
主要用户: 读者（买书）、出版商（上架书籍）、运营团队（管理内容和订单）
```

---

## 核心实体（Entities）

### User（用户）

```
描述:     系统中的注册账户，可以是读者或出版商
创建时机: 用户通过邮箱注册或第三方 OAuth 登录
关键字段:
  - id: UUID，唯一标识
  - email: 邮箱，登录凭证，全局唯一
  - name: 显示名称
  - role: reader | publisher | admin
  - created_at: 注册时间
关联实体: Order, Review, Address
```

### Book（图书）

```
描述:     可售卖的图书商品
创建时机: 出版商上架新书，经运营审核通过后可见
关键字段:
  - id: UUID
  - isbn: 国际标准书号，全局唯一
  - title: 书名
  - author: 作者（可多个）
  - publisher_id: 关联出版商 User
  - price: 售价（分，整数，避免浮点误差）
  - stock: 库存数量
  - status: draft | pending_review | active | discontinued
关联实体: Category, Review, OrderItem
```

### Order（订单）

```
描述:     用户的一次购买行为，包含一或多本书
创建时机: 用户从购物车发起结算
关键字段:
  - id: UUID
  - user_id: 下单用户
  - total_amount: 订单总金额（分）
  - status: pending_payment | paid | shipping | delivered | cancelled | refunded
  - created_at: 下单时间
  - paid_at: 支付时间（可为空）
关联实体: User, OrderItem, Payment
```

### OrderItem（订单明细）

```
描述:     订单中的每一行商品
创建时机: 随订单创建
关键字段:
  - id: UUID
  - order_id: 所属订单
  - book_id: 商品图书
  - quantity: 数量
  - unit_price: 下单时的单价快照（防止价格变动后对不上）
关联实体: Order, Book
```

### Review（评价）

```
描述:     用户对已购买图书的评价
创建时机: 用户在订单完成后对某本书提交评价
关键字段:
  - id: UUID
  - user_id: 评价者
  - book_id: 被评价的书
  - order_id: 关联订单（确保真实购买）
  - rating: 1-5 整数
  - content: 评价文本
关联实体: User, Book, Order
```

---

## 核心业务流程（Workflows）

### 流程 1：图书上架

```
触发条件: 出版商提交新书信息
参与实体: Book, User(publisher)
步骤:
  1. 出版商填写书籍信息（title, isbn, price, 封面等）
  2. 系统创建 Book（status=draft）
  3. 出版商提交审核（status → pending_review）
  4. 运营审核通过（status → active），图书在搜索中可见
  5. 审核拒绝 → 退回修改（status → draft），附拒绝原因
结果: Book status=active，可被搜索和购买
异常情况:
  - ISBN 重复 → 拒绝创建，提示已存在
  - 价格为 0 或负数 → 验证失败
```

### 流程 2：下单购买

```
触发条件: 用户点击"结算"按钮
参与实体: User, Order, OrderItem, Book, Payment
步骤:
  1. 校验购物车中所有 Book 的库存（stock >= quantity）
  2. 锁定库存（stock -= quantity，乐观锁）
  3. 创建 Order（status=pending_payment）+ OrderItems
  4. 调用支付接口，生成支付链接
  5. 用户完成支付 → 支付回调 → Order status → paid
  6. 触发发货流程（status → shipping → delivered）
结果: Order status=delivered，库存已扣减
异常情况:
  - 库存不足 → 回滚，返回错误，不创建订单
  - 支付超时（30 分钟）→ 取消订单，恢复库存
  - 支付失败 → 订单保持 pending_payment，可重试
```

### 流程 3：退款

```
触发条件: 用户在收货后 7 天内申请退款
参与实体: Order, Payment, User
步骤:
  1. 校验订单状态为 delivered 且在退款期内
  2. 创建退款申请（Order status → refunded 待审核）
  3. 运营审核退款
  4. 审核通过 → 调用支付接口退款 → 恢复库存
结果: Order status=refunded，金额原路返回
异常情况:
  - 超过退款期 → 拒绝
  - 已评价的订单仍可退款（评价保留）
```

---

## 业务规则（Business Rules）

```
BR-001: 一本书的 ISBN 全局唯一，不可修改
         一旦创建，isbn 字段不允许 UPDATE

BR-002: 订单金额必须 > 0
         total_amount 和 unit_price 使用整数（分），不允许负数

BR-003: 已发货的订单不可取消
         status 为 shipping/delivered 时，cancel 操作被拒绝

BR-004: 评价必须基于真实购买
         创建 Review 时必须验证 user_id 有该 book_id 的已完成订单

BR-005: 库存不能为负
         下单时使用 WHERE stock >= quantity 乐观锁，避免超卖

BR-006: 价格快照不可变
         OrderItem.unit_price 在创建时从 Book.price 复制，之后不跟随变化

BR-007: 出版商只能管理自己的书
         publisher_id 校验贯穿所有 Book 写操作
```

---

## 状态机（State Machines）

### Book 状态流转

```
draft --[出版商提交审核]--> pending_review
pending_review --[运营通过]--> active
pending_review --[运营拒绝]--> draft
active --[出版商下架]--> discontinued
discontinued --[出版商重新上架]--> pending_review

有效状态: draft, pending_review, active, discontinued
终态（不可变更）: 无（均可流转）
可购买状态: active
```

### Order 状态流转

```
pending_payment --[支付成功]--> paid
pending_payment --[超时30分钟]--> cancelled
paid --[发货]--> shipping
shipping --[确认收货]--> delivered
delivered --[申请退款且审核通过]--> refunded
pending_payment --[用户取消]--> cancelled

有效状态: pending_payment, paid, shipping, delivered, cancelled, refunded
终态（不可变更）: cancelled, refunded, delivered（超过退款期后）
```

---

## 术语表（Glossary）

| 术语 | 含义 | 注意 |
|------|------|------|
| User | 系统账户，含 reader/publisher/admin 三种角色 | 不要与"顾客"混淆，publisher 也是 User |
| Book | 可售卖的图书商品 | 不是"电子书"，本系统只卖实体书 |
| Order | 一次购买行为 | 一个 Order 可包含多个 OrderItem |
| OrderItem | 订单中的一行商品 | 注意 unit_price 是快照，不是 Book.price 的引用 |
| stock | Book 的可售库存数量 | 下单时扣减，取消/退款时恢复 |
| 分 | 金额单位，1 元 = 100 分 | 所有金额字段都用整数（分），前端显示时 / 100 |

---

## 变更记录

| 日期 | 变更内容 | 原因 |
|------|---------|------|
| 2026-04-04 | 初始创建 | 项目启动 |
| 2026-04-04 | 新增 Review 实体 + BR-004 | 第一版评价功能上线 |
