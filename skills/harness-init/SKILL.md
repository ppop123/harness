---
name: harness-init
description: |
  为当前项目生成 Harness Engineering 工程结构。
  已有项目自动扫描生成，新项目交互引导生成。输入 /harness-init 开始。
---

# Harness Init

为当前项目生成量身定制的 Harness Engineering 工程结构。

支持两种场景：
- **已有项目**：扫描代码后动态生成，所有文件反映真实情况
- **全新项目**：交互引导选择技术栈和偏好，生成标准骨架 + Harness 结构

---

## Step 0：判断项目类型

检查当前目录是否有代码文件：

```
package.json / tsconfig.json / pyproject.toml / setup.py / go.mod /
Cargo.toml / pom.xml / build.gradle / *.csproj / Package.swift / pubspec.yaml /
src/ / lib/ / app/ / cmd/
```

- **找到任何一个** → 走 **路径 A：已有项目（扫描流程）**
- **全都没有**（空目录或只有 README/.git） → 走 **路径 B：全新项目（引导流程）**

---

# 路径 A：已有项目

适用于已经有代码的项目。先扫描，再生成。

## A1：扫描项目

### 技术栈检测

```
package.json / tsconfig.json → TypeScript (Next.js / Node / React Native / Expo)
pyproject.toml / setup.py / Pipfile → Python (FastAPI / Django / AI)
go.mod → Go
Cargo.toml → Rust
pom.xml / build.gradle → Java / Kotlin
*.csproj / *.sln → C# / .NET
Package.swift → Swift
pubspec.yaml → Dart / Flutter
```

检测不到或有多个时问用户。

### 工具链检测

```
包管理器：pnpm-lock.yaml / yarn.lock / package-lock.json / Cargo.lock / go.sum / poetry.lock / uv.lock
Linter：biome.json / .eslintrc* / eslint.config.* / ruff.toml / pyproject.toml[tool.ruff] / .golangci.yml / clippy.toml
Formatter：biome.json / .prettierrc* / rustfmt.toml
Test runner：vitest.config* / jest.config* / pytest.ini / pyproject.toml[tool.pytest]
Type checker：tsconfig.json(strict) / mypy.ini / pyproject.toml[tool.mypy]
```

读 package.json 的 scripts 字段确认 dev/lint/test/build 的真实命令。

### 目录结构扫描

获取项目的真实目录树（排除 node_modules/.git/dist 等），识别顶层模块划分：
- 典型分层？（types / services / controllers）
- 功能模块？（daemon / analyzer / commands）
- 领域驱动？（user / order / payment）
- monorepo？（packages/ / apps/）

### 实体和类型扫描

```
TypeScript: grep -rn 'export (interface|type|class) ' src/
Python: grep -rn 'class .*(BaseModel|Model):' src/ 或 @dataclass
Go: grep -rn 'type .* struct'
Rust: grep -rn 'pub struct\|pub enum' src/
Java/Kotlin: grep -rn 'public class\|data class' src/
Swift: grep -rn 'struct\|class\|enum' Sources/
Dart: grep -rn 'class .* {' lib/
```

### 现有配置检测

检查是否已有 CLAUDE.md / AGENTS.md / .github/workflows / .pre-commit-config.yaml / docs/，已有的不覆盖或问用户合并策略。

## A2：确认生成方案

把扫描结果展示给用户：

```
检测到：TypeScript + Next.js / pnpm / Biome / Vitest
目录结构：功能模块（daemon / analyzer / generator / commands）
实体：RawObservation, Observation, AnalysisResult, Config

将生成 N 个文件，确认？
```

用户确认后进入 A3。

## A3：动态生成文件

所有文件基于扫描结果生成。**生成完每个文件后自检：文件中是否还残留模版占位内容？有就立刻修。**

### CLAUDE.md / AGENTS.md

从 GitHub 拉取对应栈的模版骨架，然后**逐行检查并替换所有动态内容**：

```
https://raw.githubusercontent.com/ppop123/harness/main/stacks/$STACK/claude/CLAUDE.md
https://raw.githubusercontent.com/ppop123/harness/main/stacks/$STACK/codex/AGENTS.md
```

必须替换：
- `[PROJECT_NAME]` / `[OWNER]` / `[DATE]` → 真实值
- 分层引用（如 `Types → Config → Repositories → Services → Controllers`） → 项目实际模块结构
- 命令引用（如 `npm run lint`、`npx vitest run`） → 项目实际命令（如 `pnpm lint`、`pnpm test`）
- `<!-- harness-init 适配 -->` 注释处 → 真实内容
- 实体描述 → 从扫描结果填入，不要留模版中的示例实体

**禁止**：生成的文件中不允许出现 `[PROJECT_NAME]`、`[OWNER]`、`[ONE_LINE_DESCRIPTION]`、`[DATE]`、`<!-- harness-init` 等未替换的占位符。生成后 grep 检查，有就修。

**禁止**：生成的文件中不允许出现乱码（如 `M-oM-?M-=` 或 `���`）。生成后检查编码，有乱码就重写该行。

### docs/architecture.md

**完全根据扫描结果生成**——用真实目录树、真实模块职责、真实依赖方向。

**禁止**：不允许出现扫描中不存在的目录名（如项目没有 `repositories/` 就不能写 `repositories/`）。
**禁止**：不允许描述与代码实现不一致的通信方式（如代码用 HTTP POST，文档不能写"通过 WebSocket 发送"）。

### docs/golden-principles.md

从 GitHub 拉取对应栈的黄金原则模版，把执行工具替换为项目实际使用的（ESLint→Biome 等）。

### scripts/layer-check.sh

**根据扫描到的目录结构生成**：
- 典型分层 → 标准分层检查
- 功能模块 → 模块边界检查（每个模块不应直接 import 另一个模块的内部实现）
- 无法确定 → 带 TODO 注释的骨架，但至少检查基本规则

### scripts/init.sh

**根据扫描到的工具链生成**，所有命令必须能在当前项目直接跑通。

**关键**：必须兼容非交互环境（CI、Codex 子进程等）。规则：
- 安装命令加 `--frozen-lockfile`（pnpm）或 `--ci`（npm）或等效 flag，避免交互提示
- 如果检测到 `CI` 环境变量，跳过可能触发交互的步骤
- 具体写法：

```bash
if [[ -n "${CI:-}" ]]; then
  pnpm install --frozen-lockfile
else
  pnpm install
fi
```

### CI / pre-commit

同理，用实际命令。已有配置时问用户合并还是跳过。

### docs/domain-model.md

**基于 A1 实体扫描结果生成**。必须包含：
- 每个扫描到的实体名、关键字段（从代码中读取真实字段名和类型）、所在文件路径
- 实体间的关联关系（从 import 关系推断）
- 推断不了的写 `[待补充]`

**禁止**：不允许出现扫描中不存在的实体（如代码中没有 User 就不能写 User）。
**禁止**：不允许描述与代码不一致的字段（如代码字段是 `path`，文档不能写 `url`）。

### docs/onboarding.md

基于实际命令生成，命令表必须能直接复制执行。

### feature_list.json

**禁止**：不允许保留任何示例内容（"User registration"、"POST /api/register" 等）。
正确做法：features 数组为空 `[]`，只保留结构。

```json
{
  "_comment": "功能追踪。每个 session 结束后更新。",
  "project": "[实际项目名]",
  "last_updated": "[今天日期]",
  "features": [],
  "status_values": ["not_started", "in_progress", "blocked", "testing", "done"]
}
```

### .env.example

**禁止**：不允许保留模版中的假变量（DATABASE_URL=postgresql://...、SECRET_KEY=... 等）。
正确做法：从项目中的 .env / .env.local / docker-compose.yml / 代码中的 process.env 引用推断实际需要的变量。没有就留空文件加注释 `# 暂无环境变量`。

### agent-progress.txt

只保留头部说明格式，不保留任何示例 session 记录。

### 静态文件（从 GitHub 拉取，不需适配）

```
common/docs/tech-decisions/000-template.md → docs/tech-decisions/000-template.md
common/scripts/audit-prompt.md → scripts/audit-prompt.md
common/scripts/doc-gardening-prompt.md → scripts/doc-gardening-prompt.md
common/scripts/new-feature-prompt.md → scripts/new-feature-prompt.md
```

## A4：验证

### 自动验证

```bash
CI=true bash scripts/init.sh   # 必须跑通（含非交互模式）
bash scripts/layer-check.sh    # 必须检查真实目录，不能空跑
```

### 内容验证（逐条检查）

1. grep 所有生成的文件，确认无残留占位符：`[PROJECT_NAME]`、`[OWNER]`、`[DATE]`、`[Entity1`、`[YOUR FEATURE]`、`[待补充]` 以外的方括号占位
2. grep 所有生成的文件，确认无乱码：`���`、`M-o`
3. 检查 feature_list.json 的 features 数组是否为空
4. 检查 .env.example 是否已清除模版内容
5. 检查 docs/domain-model.md 中的实体是否与 src/ 中的类型定义一致

任何验证失败就修，直到全部通过。

## A5：输出摘要

展示生成的文件列表、检测结果、下一步行动。明确列出哪些文件标注了 `[待补充]`，提醒用户补完。

---

# 路径 B：全新项目

适用于空目录。通过交互引导收集偏好，生成标准骨架 + Harness 结构。

## B1：交互引导

依次收集以下信息（能合并就合并问，尽量少打扰）：

**必填**：
1. **项目名称** — 自由输入
2. **技术栈** — 从列表选择：
   - TypeScript + Next.js (`ts-nextjs`)
   - TypeScript + Node.js API (`ts-node`)
   - Python + FastAPI (`python-fastapi`)
   - Python + Django (`python-django`)
   - Python AI / Data Science (`python-ai`)
   - Java + Spring Boot (`java-spring`)
   - C# + ASP.NET Core (`csharp-dotnet`)
   - Go (`go`)
   - Rust (`rust`)
   - Swift + SwiftUI (`swift-ios`)
   - Kotlin + Android (`kotlin-android`)
   - Dart + Flutter (`dart-flutter`)
   - React Native (`react-native`)
3. **AI 工具** — Claude / Codex / 都要

**可选**（有默认值）：
4. **包管理器偏好** — 根据栈给默认值（如 TypeScript 默认 pnpm，Python 默认 uv）
5. **Linter 偏好** — 根据栈给默认值（如 TypeScript 默认 Biome，Python 默认 Ruff）
6. **一句话描述** — 项目做什么

## B2：生成目录骨架

根据选择的技术栈，生成该栈的标准项目目录结构。

从 GitHub 拉取该栈的标准定义：

```
https://raw.githubusercontent.com/ppop123/harness/main/stacks/$STACK/docs/architecture.md
```

读取其中的目录结构部分，在当前目录创建对应的空目录：

```bash
# 示例：ts-nextjs
mkdir -p src/types src/lib src/config src/repositories src/services src/app/api src/components
mkdir -p docs docs/tech-decisions scripts .github/workflows
```

**每个目录下创建一个 .gitkeep 文件**，确保空目录能被 git 跟踪。

## B3：生成 Harness 文件

以下文件全部从 GitHub 拉取对应栈的模版，然后替换占位符：

### 从 GitHub 拉取并替换占位符的文件

```
stacks/$STACK/claude/CLAUDE.md → CLAUDE.md
stacks/$STACK/codex/AGENTS.md → AGENTS.md
stacks/$STACK/docs/architecture.md → docs/architecture.md
stacks/$STACK/docs/golden-principles.md → docs/golden-principles.md
stacks/$STACK/docs/onboarding.md → docs/onboarding.md
stacks/$STACK/scripts/layer-check.sh → scripts/layer-check.sh
stacks/$STACK/scripts/init.sh → scripts/init.sh
stacks/$STACK/ci/ci.yml → .github/workflows/ci.yml
stacks/$STACK/config/pre-commit-config.yaml → .pre-commit-config.yaml
stacks/$STACK/config/lint-config.txt → 放到对应位置（.eslintrc.json / pyproject.toml 等）
common/docs/domain-model.md → docs/domain-model.md
common/docs/tech-decisions/000-template.md → docs/tech-decisions/000-template.md
common/scripts/audit-prompt.md → scripts/audit-prompt.md
common/scripts/doc-gardening-prompt.md → scripts/doc-gardening-prompt.md
common/scripts/new-feature-prompt.md → scripts/new-feature-prompt.md
```

占位符替换：
- `[PROJECT_NAME]` → 项目名
- `[ONE_LINE_DESCRIPTION]` → 描述
- `[OWNER]` → 从 git config 获取
- `[DATE]` → 今天日期

### 根据用户偏好调整的文件

如果用户选的包管理器或 linter 和模版默认不同，替换以下文件中的命令：
- `scripts/init.sh` — 安装命令和 lint 命令
- `.github/workflows/ci.yml` — 构建步骤
- `.pre-commit-config.yaml` — hook 命令
- `CLAUDE.md` / `AGENTS.md` — 完成标准中的命令
- `docs/onboarding.md` — 常用命令表

### 生成空模版

- `feature_list.json` — features 数组为空
- `agent-progress.txt` — 只有头部说明
- `.env.example` — 根据栈生成典型变量名（如 DATABASE_URL、API_KEY），值留空

## B4：输出摘要

```
✅ 项目骨架 + Harness 已生成

项目：[name]
技术栈：[stack]
包管理器：[pm]
Linter：[linter]

生成了 N 个文件 + M 个目录

下一步：
1. 安装依赖：[实际安装命令]
2. 填写 docs/domain-model.md（定义你的业务实体）
3. 开始开发时先读 CLAUDE.md
4. 第一个功能完成后运行 bash scripts/layer-check.sh 验证分层
```

---

## 通用规则

- 拉取文件失败时明确告诉用户并停止，不静默跳过
- 目标文件已存在时先问用户覆盖策略
- 不编造不存在的实体、命令或配置
- 推断不了的内容标注 `[待补充]`
- 生成的脚本必须有可执行权限（chmod +x）
