# 上手指南 — Swift + SwiftUI

## 第一步：理解项目

```
1. AGENTS.md 或 CLAUDE.md  （项目概览）
2. docs/domain-model.md     （业务领域）
3. docs/architecture.md     （代码结构）
4. docs/golden-principles.md（代码规范）
```

## 第二步：环境配置

```bash
# 安装依赖
Swift Package Manager install  # 根据项目实际调整

# 启动开发
xcodebuild (或 Xcode 运行)
```

## 第三步：开发工作流

```
1. 读 docs/domain-model.md → 确认涉及哪些实体
2. 读 docs/architecture.md → 确认在哪个层实现
3. 写代码（按层级顺序）
4. 运行检查：swiftlint lint --strict && xcodebuild test -scheme App
5. 提交 PR
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `xcodebuild (或 Xcode 运行)` | 启动开发 |
| `swiftlint lint --strict` | 代码检查 |
| `xcodebuild test -scheme App` | 运行测试 |
| `swiftlint lint --strict && xcodebuild test -scheme App` | 完整检查（提交前跑） |

## 定期维护

| 频率 | 任务 |
|------|------|
| 每周 | 代码审计（`scripts/audit-prompt.md`）|
| 每周 | 文档更新（`scripts/doc-gardening-prompt.md`）|
