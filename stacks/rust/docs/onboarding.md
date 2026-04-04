# 上手指南 — Rust

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
Cargo install  # 根据项目实际调整

# 启动开发
cargo watch -x run
```

## 第三步：开发工作流

```
1. 读 docs/domain-model.md → 确认涉及哪些实体
2. 读 docs/architecture.md → 确认在哪个层实现
3. 写代码（按层级顺序）
4. 运行检查：cargo clippy -- -D warnings && cargo test
5. 提交 PR
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `cargo watch -x run` | 启动开发 |
| `cargo clippy -- -D warnings` | 代码检查 |
| `cargo test` | 运行测试 |
| `cargo clippy -- -D warnings && cargo test` | 完整检查（提交前跑） |

## 定期维护

| 频率 | 任务 |
|------|------|
| 每周 | 代码审计（`scripts/audit-prompt.md`）|
| 每周 | 文档更新（`scripts/doc-gardening-prompt.md`）|
