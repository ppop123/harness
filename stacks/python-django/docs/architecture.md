# 架构文档 — Python + Django

## 核心原则

**依赖只能向下流动，禁止反向或跨层调用。**

## 依赖层级

```
Models → Managers → Services → Serializers → Views → URLs
```

## 目录结构

```
project/
├── apps/
│   └── <app_name>/
│       ├── models.py       # 数据模型
│       ├── managers.py     # 自定义 QuerySet
│       ├── services.py     # 业务逻辑（不放 views 里！）
│       ├── serializers.py  # API 序列化/验证
│       ├── views.py        # 请求处理
│       ├── urls.py         # 路由
│       └── tests/
├── config/                 # Django settings
└── common/                 # 共享工具
```

## 各层职责

| 层级 | 职责 | 禁止 |
|------|------|------|
| 最底层（Types/Models） | 类型定义、数据结构 | 任何逻辑代码 |
| Config/Utils | 纯函数工具、配置读取 | 调用数据库或外部 API |
| Repository/Data | 数据库查询、缓存操作 | 业务逻辑判断 |
| Service/UseCase | 业务逻辑、跨 Repo 协调 | 处理 HTTP 请求/响应 |
| Controller/Handler/View | 请求解析、调用 Service、返回响应 | 直接数据库调用 |
| UI/Pages（如适用） | 渲染、用户交互 | 直接调用 Service 或 DB |

## 变更记录

| 日期 | 变更 | 原因 |
|------|------|------|
| [DATE] | 初始架构 | 项目创建 |
