# 架构文档 — Python AI / Data Science

## 核心原则

**依赖只能向下流动，禁止反向或跨层调用。**

## 依赖层级

```
Config → Data → Models → Pipelines → Evaluation → API/UI
```

## 目录结构

```
project/
├── src/
│   ├── config/          # 环境变量、超参数
│   ├── data/            # 数据加载/清洗
│   ├── models/          # 模型定义
│   ├── pipelines/       # 训练/推理流水线
│   ├── evaluation/      # 评估指标
│   └── api/             # 模型服务 API
├── notebooks/           # 探索性分析（不含业务逻辑）
├── experiments/         # 实验记录
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
