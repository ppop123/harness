# CLAUDE.md — Harness Repo Entry

> 本文件是 harness 仓库给 Claude / Claude Code / Cowork 的短入口。
> 完整维护规则见 `docs/repo-management.md`，跨工具共识见 `AGENTS.md`。

## 项目定位

- 这是一个多技术栈 Harness Engineering 模板仓库。
- 关键目标是让生成出来的项目对 AI 更可读、更可验证、更不容易偏航。
- `generate_repo.py` 负责生成 `stacks/`、根 README 和 `manifest.json`。

## Claude 工作方式

1. 先读 `docs/repo-management.md`，再读当前任务涉及的生成目标。
2. 先说理解和计划，再改文件。
3. 先补 failing tests，再改生成器或根文档。
4. 改完后重新生成，并把验证结果讲清楚。

## 修改边界

- `stacks/` 是生成物，默认不手改。
- `common/` 是共享模板区，可以直接编辑。
- 根级入口文件要保持短小，长说明写进 `docs/`。
- 跨 session 记录统一使用 `common/agent-progress.txt`。

## 推荐验证

```bash
python3 -m unittest discover -s tests -q
python3 generate_repo.py
python3 -m unittest discover -s tests -q
```

## 这次最常见的改动类型

- 修生成器里的平台契约错误。
- 修 `layer-check.sh` 这类“看起来像约束、实际上不够硬”的脚本。
- 修 README / 入口文档漂移，让仓库自己也遵守 Harness Engineering。

## 完成标准

- 根入口文件不超过 100 行。
- 生成器、README、根入口文档三者口径一致。
- Claude/Codex 的 bootstrap 路径清晰且互不打架。
