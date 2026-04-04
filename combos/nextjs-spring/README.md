# Next.js 前端 + Spring Boot 后端 — 组合模版

企业级全栈组合。Next.js 现代前端 + Spring Boot 稳定后端。

## 组成

| 部分 | 模版 |
|------|------|
| 前端/客户端 | `stacks/ts-nextjs/` |
| 后端 | `stacks/java-spring/` |

## 使用方法

1. 分别从对应模版复制文件到前后端项目
2. 前后端共用 `common/docs/domain-model.md`（统一业务语言）
3. 在根目录创建一个 monorepo 级别的 `AGENTS.md` 或 `CLAUDE.md`，指向两边

## Monorepo 结构建议

```
project/
├── AGENTS.md (or CLAUDE.md)  ← 全局索引
├── docs/                      ← 共享业务文档
│   ├── domain-model.md
│   └── architecture.md
├── frontend/                  ← ts-nextjs
│   └── AGENTS.md (or CLAUDE.md)
└── backend/                   ← java-spring
    └── AGENTS.md (or CLAUDE.md)
```
