# Flutter 客户端 + FastAPI 后端 — 组合模板

跨平台移动应用 + Python 后端，快速迭代。

## 组成

| 部分 | 模板 |
|------|------|
| 前端/客户端 | `stacks/dart-flutter/` |
| 后端 | `stacks/python-fastapi/` |

## 使用方法

1. 分别从对应模板复制文件到前后端项目
2. 前后端共用 `common/docs/domain-model.md`（统一业务语言）
3. 在根目录创建一个 monorepo 级别的 `AGENTS.md` 或 `CLAUDE.md`，指向两边

## Monorepo 结构建议

```
project/
├── AGENTS.md (or CLAUDE.md)  ← 全局索引
├── docs/                      ← 共享业务文档
│   ├── domain-model.md
│   └── architecture.md
├── frontend/                  ← dart-flutter
│   └── AGENTS.md (or CLAUDE.md)
└── backend/                   ← python-fastapi
    └── AGENTS.md (or CLAUDE.md)
```
