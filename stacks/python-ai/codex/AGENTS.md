# AGENTS.md — AI Agent 项目指令（Python AI / Data Science）

> 本文件是所有 AI 编程工具（Codex、Cursor、Windsurf 等）的入口文件。
> 在开始任何任务前必须先读此文件。详细规则跟随链接查看。

---

## 项目信息

```
项目名称: [PROJECT_NAME]
描述:     [ONE_LINE_DESCRIPTION]
技术栈:   Python AI / Data Science
负责人:   [OWNER]
```

## 文档导航

| 文档                | 路径                              |
|--------------------|----------------------------------|
| 架构与依赖层级      | `docs/architecture.md`           |
| 代码黄金原则        | `docs/golden-principles.md`      |
| 业务领域模型        | `docs/domain-model.md`           |
| 上手指南           | `docs/onboarding.md`             |
| 技术决策记录        | `docs/tech-decisions/`           |
| 功能需求追踪        | `feature_list.json`              |
| 跨 session 进度    | `agent-progress.txt`                |

## Session 启动（每次必做）

```bash
bash scripts/init.sh       # 验证环境 + baseline tests
cat agent-progress.txt         # 了解上次进度
cat feature_list.json       # 确认当前任务
```

## 核心规则（不可违反）

1. **依赖方向单向流动** — `Config → Data → Models → Pipelines → Evaluation → API/UI`，禁止反向
2. **边界必须验证** — 外部数据用 Pydantic 验证，不猜测结构
3. **不重复** — 复用 utils/lib，超过 2 处重复必须提取
4. **类型安全** — 严格使用 mypy (moderate)
5. **错误必须处理** — 不允许静默吞掉 error
6. **配置集中** — 用 python-dotenv 管理环境变量，禁止硬编码

## 技术偏好

- 偏好**稳定且文档丰富**的技术（对 AI 训练集友好）
- 偏好**组合**而非继承
- 偏好**显式**而非隐式

## 任务完成标准

```bash
# 提交前必须通过
ruff check src/ && mypy src/ && pytest tests/
bash scripts/layer-check.sh  # 依赖层级检查
```

完成后更新：
- `feature_list.json` — 更新 status 和 files_touched
- `agent-progress.txt` — 追加 session 记录

## 禁止模式

```
❌ # Jupyter notebook 里写 500 行 + 训练 + 部署
❌ 在 UI/Handler 层直接操作数据库
❌ 硬编码 API keys、URL、端口
❌ 空的错误处理块
❌ 超过 2 处的重复逻辑
```
