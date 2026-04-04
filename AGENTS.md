# AGENTS.md — Harness Repo Entry

> 本文件是 harness 仓库给 Codex / Cursor / Windsurf 等工具的短入口。
> 完整维护规则见 `docs/repo-management.md`，用户视角说明见 `README.md`。

## 项目定位

- 这是一个 Harness Engineering 模版仓库，核心资产是约束系统而不是示例代码。
- `generate_repo.py` 是生成器和主要事实来源。
- `stacks/` 下是生成产物，不要手改。

## 先读什么

1. `docs/repo-management.md`
2. `README.md`
3. 与当前任务相关的生成目标或 `common/` 文件

## 修改边界

- 改某个技术栈模板：编辑 `generate_repo.py`，然后重新生成。
- 改共享文档或共享 prompt：直接编辑 `common/`。
- 改根级仓库说明：编辑本文件、`CLAUDE.md`、`docs/repo-management.md`。
- 不要直接手改 `stacks/*` 里的生成文件，除非是在验证生成结果后立刻重跑生成器覆盖。

## 工作流

```bash
python3 -m unittest discover -s tests -q
python3 generate_repo.py
python3 -m unittest discover -s tests -q
```

- 先补或更新测试，再改生成器。
- 生成后抽查根 README、代表性 stack README、Claude/Codex 入口文档和 `layer-check.sh`。
- 涉及跨 session 约定时，统一使用 `common/agent-progress.txt`。

## 平台约定

- `AGENTS.md` 面向跨工具通用入口，强调统一规则和可执行验证。
- `CLAUDE.md` 面向 Claude / Claude Code，允许更强的对话式节奏，但不能和这里的事实冲突。
- 两者的详细差异说明统一写在 `docs/repo-management.md`，避免双份长文档漂移。

## 完成标准

- 测试通过。
- 重新生成后无明显 contract 漂移。
- 根入口文件保持短小，详细信息下沉到 `docs/`。
