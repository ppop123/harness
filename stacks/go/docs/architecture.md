# 架构文档 — Go

## 核心原则

**依赖只能向下流动，禁止反向或跨层调用。**

## 依赖层级

```
Domain → Repository → Service → Handler → Router
```

## 目录结构

```
project/
├── cmd/
│   └── server/main.go    # 入口
├── internal/
│   ├── domain/            # 实体 + 接口定义
│   ├── repository/        # 数据访问实现
│   ├── service/           # 业务逻辑
│   └── handler/           # HTTP 处理器
├── pkg/                   # 可导出的工具包
├── config/                # 配置
└── tests/
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
