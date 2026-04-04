# CLAUDE.md — Claude 工作指南（Python AI / Data Science）

> 本文件专为 Claude / Claude Code / Cowork 设计。
> 若项目中同时提供 `AGENTS.md`，可先读它获取跨工具共识；否则本文件可独立使用。

---

## 项目基本信息

```
项目名称: [PROJECT_NAME]
描述:     [ONE_LINE_DESCRIPTION]
技术栈:   Python AI / Data Science
负责人:   [OWNER]
```

## 快速导航

| 我想了解...         | 文件位置                        |
|--------------------|-------------------------------|
| 整体架构与层级      | `docs/architecture.md`        |
| 代码黄金原则        | `docs/golden-principles.md`   |
| 业务领域模型        | `docs/domain-model.md`        |
| 如何开始工作        | `docs/onboarding.md`          |
| 技术选型决策        | `docs/tech-decisions/`        |
| 功能需求追踪        | `feature_list.json`           |
| 跨 session 进度    | `agent-progress.txt`             |

## Claude 工作方式

### Session 启动仪式
1. 运行 `bash scripts/init.sh` 验证环境
2. 读 `agent-progress.txt` 了解上次进度
3. 读 `feature_list.json` 确认当前任务
4. 读本文件 + `docs/` 相关文档

### 任务执行
1. **先说你的理解和计划**，再写代码
2. 遇到不确定的概念 → 查 `docs/domain-model.md`，查不到就问我

### 代码生产
- 写**最小可运行**的变更，不顺手"优化"无关代码
- 按层级顺序实现：Config → Data → Models → Pipelines → Evaluation → API/UI
- 每完成一个子任务，汇报进度再继续

### 上下文管理
- 先读架构文档，再读具体代码（不要一次读所有文件）
- 上下文不够时，告诉我优先需要哪些文件

### 完成标准
- [ ] `ruff check src/ && mypy src/ && pytest tests/` 全部通过
- [ ] `bash scripts/layer-check.sh` 无违规
- [ ] 新增模块已更新 `docs/domain-model.md`
- [ ] `feature_list.json` 状态已更新
- [ ] `agent-progress.txt` 已追加本次记录
- [ ] PR 描述写清楚了"为什么这样做"

## 不要做的事

```
❌ 不要修改与任务无关的文件
❌ 不要使用 # Jupyter notebook 里写 500 行 + 训练 + 部署
❌ 不要安装新依赖（先告知我，等确认）
❌ 不要删除注释或测试（除非明确要求）
```

## 定期维护

- 对我说"代码审计" → 按 `scripts/audit-prompt.md` 执行
- 对我说"更新文档" → 按 `scripts/doc-gardening-prompt.md` 执行
