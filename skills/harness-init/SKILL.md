---
name: harness-init
description: |
  安装一次、重复使用的 Harness Engineering 薄装载 skill。
  当用户要求“装载 harness”“加载某个 stack 的 harness 结构”“从 GitHub 拉取 harness 模板”时使用。
  本 skill 只负责收集参数并从 GitHub 按需拉取当前栈文件，不内置栈模板副本。
---

# Harness Init

`harness-init` 是一个 thin loader。

- 安装阶段：只安装这一个 skill
- 项目阶段：根据用户请求，从 GitHub 按需拉取 stack 文件到当前目录
- 事实来源：`https://github.com/ppop123/harness`

## 设计约束

- 从 GitHub 按需拉取，不要依赖 skill 内部模板副本。
- 不要在 skill 中内置各技术栈模板文件。
- 不要静默回退到本地旧副本；GitHub 拉取失败时，要明确告诉用户并停止。
- 不要无提示覆盖用户已有文件；若目标文件已存在，先确认覆盖策略。

## 必要输入

在开始前，确认或推断这些参数：

1. `stack_id`
2. `repo_url`
   默认：`https://github.com/ppop123/harness`
3. `ref`
   默认：`main`
4. `target_dir`
   默认：当前工作目录
5. `platform`
   可选：`claude`、`codex`、`both`
   默认：按当前平台推断；若用户明确说“两边都要”，则写两份入口文件

## 支持的 stack ID

- `ts-nextjs`
- `ts-node`
- `python-fastapi`
- `python-django`
- `python-ai`
- `java-spring`
- `csharp-dotnet`
- `go`
- `rust`
- `swift-ios`
- `kotlin-android`
- `dart-flutter`
- `react-native`

## 拉取规则

将 GitHub 仓库 URL 转成 raw 基地址，然后按需拉取。

默认 raw 基地址：

```text
https://raw.githubusercontent.com/ppop123/harness/main
```

### 入口文件

- `claude`：拉取 `stacks/$STACK/claude/CLAUDE.md` 到 `CLAUDE.md`
- `codex`：拉取 `stacks/$STACK/codex/AGENTS.md` 到 `AGENTS.md`
- `both`：两份都拉

### stack 文件

- `stacks/$STACK/docs/architecture.md` -> `docs/architecture.md`
- `stacks/$STACK/docs/golden-principles.md` -> `docs/golden-principles.md`
- `stacks/$STACK/docs/onboarding.md` -> `docs/onboarding.md`
- `stacks/$STACK/scripts/layer-check.sh` -> `scripts/layer-check.sh`
- `stacks/$STACK/scripts/init.sh` -> `scripts/init.sh`
- `stacks/$STACK/ci/ci.yml` -> `.github/workflows/ci.yml`
- `stacks/$STACK/config/pre-commit-config.yaml` -> `.pre-commit-config.yaml`

### shared 文件

- `common/docs/domain-model.md` -> `docs/domain-model.md`
- `common/docs/tech-decisions/000-template.md` -> `docs/tech-decisions/000-template.md`
- `common/scripts/audit-prompt.md` -> `scripts/audit-prompt.md`
- `common/scripts/doc-gardening-prompt.md` -> `scripts/doc-gardening-prompt.md`
- `common/scripts/new-feature-prompt.md` -> `scripts/new-feature-prompt.md`
- `common/feature_list.json` -> `feature_list.json`
- `common/agent-progress.txt` -> `agent-progress.txt`
- `common/.env.example` -> `.env.example`

## 执行步骤

1. 解析用户请求中的 `stack_id`、平台和可选仓库地址。
2. 若缺少关键参数，只问最少的澄清问题。
3. 创建所需目录：
   - `docs/`
   - `docs/tech-decisions/`
   - `scripts/`
   - `.github/workflows/`
4. 按规则从 GitHub 拉取文件。
5. 若用户提供了项目名或一句话描述，可替换常见占位符。
6. 输出结果摘要与下一步建议。

## 默认下一步建议

- 先读刚写入的 `AGENTS.md` 或 `CLAUDE.md`
- 填写 `docs/domain-model.md`
- 运行 `bash scripts/init.sh`
- 确认 `.env.example` 和 CI 配置是否需要合并到现有项目

## 用户可直接这样说

```text
从 https://github.com/ppop123/harness 装载 ts-nextjs 栈的 harness 工程结构到当前目录
```

也可以明确补充：

- “只要 Codex 版本”
- “Claude 和 Codex 都要”
- “使用某个 tag / branch”
