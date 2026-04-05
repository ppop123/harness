---
name: harness-init
description: |
  为当前项目装载 Harness Engineering 工程结构。
  支持 13 种技术栈。自动拉取模版后会扫描项目实际情况并适配。
  输入 /harness-init 开始。
---

# Harness Init

为当前项目装载 Harness Engineering 工程结构。拉取模版只是第一步，**必须根据项目实际情况适配所有文件**。

## 核心原则

模版是起点，不是终点。装载完的文件必须能直接跑，不能留着模版里的假命令、假目录、假实体让 agent 跑偏。

## 规则

- 所有文件从 GitHub 实时拉取，不用本地缓存
- 拉取失败要明确告诉用户并停止
- 目标文件已存在时先问用户要不要覆盖
- **拉取后必须执行项目适配（Step 5），不能跳过**

## 必要输入

开始前确认这些参数（能推断就不问）：

1. `stack_id` — 技术栈 ID（见下方列表）
2. `platform` — `claude` / `codex` / `both`（默认按当前平台推断）

可选参数（有默认值）：
- `repo_url` — 默认 `https://github.com/ppop123/harness`
- `ref` — 默认 `main`

## 支持的 stack ID

`ts-nextjs` `ts-node` `python-fastapi` `python-django` `python-ai` `java-spring` `csharp-dotnet` `go` `rust` `swift-ios` `kotlin-android` `dart-flutter` `react-native`

## 执行步骤

### Step 1：收集参数

解析用户请求中的 stack_id 和 platform。如果能从当前项目推断就不问。

### Step 2：创建目录

```
docs/  docs/tech-decisions/  scripts/  .github/workflows/
```

### Step 3：从 GitHub 拉取文件

raw 基地址：`https://raw.githubusercontent.com/ppop123/harness/main`

**入口文件**（按 platform 选择）：
- `claude`：`stacks/$STACK/claude/CLAUDE.md` → `CLAUDE.md`
- `codex`：`stacks/$STACK/codex/AGENTS.md` → `AGENTS.md`
- `both`：两份都拉

**栈文件**：
- `stacks/$STACK/docs/architecture.md` → `docs/architecture.md`
- `stacks/$STACK/docs/golden-principles.md` → `docs/golden-principles.md`
- `stacks/$STACK/docs/onboarding.md` → `docs/onboarding.md`
- `stacks/$STACK/scripts/layer-check.sh` → `scripts/layer-check.sh`
- `stacks/$STACK/scripts/init.sh` → `scripts/init.sh`
- `stacks/$STACK/ci/ci.yml` → `.github/workflows/ci.yml`
- `stacks/$STACK/config/pre-commit-config.yaml` → `.pre-commit-config.yaml`

**通用文件**：
- `common/docs/domain-model.md` → `docs/domain-model.md`
- `common/docs/tech-decisions/000-template.md` → `docs/tech-decisions/000-template.md`
- `common/scripts/audit-prompt.md` → `scripts/audit-prompt.md`
- `common/scripts/doc-gardening-prompt.md` → `scripts/doc-gardening-prompt.md`
- `common/scripts/new-feature-prompt.md` → `scripts/new-feature-prompt.md`
- `common/feature_list.json` → `feature_list.json`
- `common/agent-progress.txt` → `agent-progress.txt`
- `common/.env.example` → `.env.example`

### Step 4：替换基本占位符

如果用户提供了项目名或描述：
- `[PROJECT_NAME]` → 项目名
- `[ONE_LINE_DESCRIPTION]` → 描述
- `[OWNER]` → 从 git config 或上下文获取
- `[DATE]` → 今天的日期

### Step 5：项目适配（必须执行，不可跳过）

这是最关键的一步。扫描当前项目的实际情况，把模版内容替换成真实信息。

#### 5.1 检测包管理器和工具链

扫描当前目录，确定实际使用的工具：

```
包管理器：查找 pnpm-lock.yaml / yarn.lock / package-lock.json / Cargo.lock / go.sum / Pipfile.lock / poetry.lock / pubspec.lock
Linter：查找 biome.json / .eslintrc* / .ruff.toml / .golangci.yml / clippy.toml / .swiftlint.yml / detekt.yml
Formatter：查找 biome.json / .prettierrc* / rustfmt.toml
Test runner：查找 vitest.config* / jest.config* / pytest.ini / Cargo.toml [dev-dependencies]
Type checker：查找 tsconfig.json (strict) / mypy.ini / pyproject.toml [tool.mypy]
```

然后替换以下文件中的命令：
- `scripts/init.sh` — 替换安装命令（npm install → pnpm install）、lint 命令（eslint → biome check）、test 命令
- `.github/workflows/ci.yml` — 替换所有构建/lint/test 步骤
- `.pre-commit-config.yaml` — 替换 hook 入口命令
- `CLAUDE.md` / `AGENTS.md` — 替换"完成标准"和"常用命令"中的命令
- `docs/onboarding.md` — 替换环境搭建和命令表

#### 5.2 扫描实际目录结构

运行 `ls` 或 `find` 扫描 src/ 或项目根目录的**实际顶层目录**。

然后：
- `docs/architecture.md` — 用实际目录结构替换模版中的示例目录树和分层定义
- `scripts/layer-check.sh` — 用实际目录名替换检查路径。如果项目结构不是典型分层（如 CLI 工具、monorepo），要重写规则或明确标注"此项目不适用标准分层检查"
- `CLAUDE.md` / `AGENTS.md` — 更新分层引用

**特别注意**：如果项目不是典型的 API 分层结构（比如 CLI 工具、桌面应用、库），不要硬套 `types → repositories → services → controllers` 这套模型。改为描述项目的实际模块关系。

#### 5.3 扫描已有类型定义和实体

在 src/ 中查找：
- TypeScript：`interface` / `type` / `class` 定义
- Python：Pydantic `BaseModel` / dataclass / Django Model
- Go：`type ... struct`
- Rust：`struct` / `enum`
- 其他语言类推

然后：
- `docs/domain-model.md` — 用扫描到的真实实体替换模版中的 `[Entity1 名称]` 占位符。至少填入实体名、关键字段、关联关系。如果能从代码推断业务含义就写上，推断不了就留 `[待补充]`
- 删除模版中明显不适用的示例内容（如"User registration"）

#### 5.4 清空示例占位内容

- `feature_list.json` — 删除 "User registration" 示例，只保留结构和一条空模版
- `.env.example` — 删除 `DATABASE_URL=postgresql://` 等示例，根据项目实际依赖填入（查 .env / docker-compose.yml / 配置文件）。没有就留空文件加注释

#### 5.5 验证适配结果

适配完成后，跑一遍基本验证：

```bash
bash scripts/init.sh        # 必须能跑通，不能报 command not found
bash scripts/layer-check.sh  # 必须检查真实目录，不能空跑通过
```

如果跑不通，继续修直到通过。

### Step 6：输出摘要

展示：
1. 写入了哪些文件
2. 做了哪些适配（检测到什么工具、替换了什么命令、扫描到哪些实体）
3. 下一步行动：
   - 补充 `docs/domain-model.md` 中标记 `[待补充]` 的部分
   - 确认 `docs/architecture.md` 的分层是否准确
   - 开始开发时先读 CLAUDE.md 或 AGENTS.md
