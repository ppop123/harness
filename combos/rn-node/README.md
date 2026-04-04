# React Native 客户端 + Node.js API — 组合模版

纯 TypeScript 全栈移动应用。前后端共享类型定义。

## 组成

| 部分 | 模版 |
|------|------|
| 前端/客户端 | `stacks/react-native/` |
| 后端 | `stacks/ts-node/` |

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
├── frontend/                  ← react-native
│   └── AGENTS.md (or CLAUDE.md)
└── backend/                   ← ts-node
    └── AGENTS.md (or CLAUDE.md)
```
