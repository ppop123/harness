# 上手指南 — Python AI / Data Science

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
pip / uv / conda install  # 根据项目实际调整

# 启动开发
jupyter lab
```

## 第三步：开发工作流

```
1. 读 docs/domain-model.md → 确认涉及哪些实体
2. 读 docs/architecture.md → 确认在哪个层实现
3. 写代码（按层级顺序）
4. 运行检查：ruff check src/ && mypy src/ && pytest tests/
5. 提交 PR
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `jupyter lab` | 启动开发 |
| `ruff check src/` | 代码检查 |
| `pytest tests/ -v` | 运行测试 |
| `ruff check src/ && mypy src/ && pytest tests/` | 完整检查（提交前跑） |

## 定期维护

| 频率 | 任务 |
|------|------|
| 每周 | 代码审计（`scripts/audit-prompt.md`）|
| 每周 | 文档更新（`scripts/doc-gardening-prompt.md`）|
