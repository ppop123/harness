---
name: harness-init
description: |
  为当前项目生成 Harness Engineering 工程结构。
  先扫描项目再生成，不拉预置模版。输入 /harness-init 开始。
---

# Harness Init

为当前项目生成量身定制的 Harness Engineering 工程结构。

**核心原则：先扫描，再生成。不拉固定模版。**

所有生成的文件必须反映项目的真实情况——真实的包管理器、真实的目录结构、真实的实体、真实的命令。生成出来的 init.sh 必须能直接跑通，layer-check.sh 必须检查真实目录。

---

## 执行流程

### Phase 1：扫描项目

在做任何事之前，先收集项目的完整画像。

#### 1.1 技术栈检测

扫描以下文件确定语言和框架：

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

如果检测不到或有多个，问用户。

#### 1.2 工具链检测

```
包管理器：pnpm-lock.yaml / yarn.lock / package-lock.json / Cargo.lock / go.sum / poetry.lock / uv.lock / pubspec.lock
Linter：biome.json / biome.jsonc / .eslintrc* / eslint.config.* / ruff.toml / pyproject.toml[tool.ruff] / .golangci.yml / clippy.toml / .swiftlint.yml / detekt.yml
Formatter：biome.json / .prettierrc* / rustfmt.toml / pyproject.toml[tool.ruff.format]
Test runner：vitest.config* / jest.config* / pytest.ini / pyproject.toml[tool.pytest] / Cargo.toml / go test
Type checker：tsconfig.json(strict) / mypy.ini / pyproject.toml[tool.mypy]
```

读 package.json 的 scripts 字段，确认 dev / lint / test / build 的真实命令。

#### 1.3 目录结构扫描

运行 `find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/__pycache__/*' -maxdepth 4` 或等效命令，获取项目的真实目录树。

重点关注 src/ 或项目根目录下的**顶层模块划分**：
- 是典型分层吗？（types / services / controllers / routes）
- 还是功能模块？（daemon / analyzer / generator / commands）
- 还是领域驱动？（user / order / payment）
- 还是 monorepo？（packages/ / apps/）

#### 1.4 实体和类型扫描

根据语言扫描代码中的类型定义：

```
TypeScript: grep -rn 'export (interface|type|class) ' src/
Python: grep -rn 'class .*(BaseModel|Model):' src/ 或 grep -rn '@dataclass' src/
Go: grep -rn 'type .* struct' .
Rust: grep -rn 'pub struct\|pub enum' src/
Java/Kotlin: grep -rn 'public class\|data class' src/
Swift: grep -rn 'struct\|class\|enum' Sources/
Dart: grep -rn 'class .* {' lib/
```

记录每个实体的名称、关键字段、所在文件。

#### 1.5 现有配置检测

检查项目是否已有：
- CLAUDE.md / AGENTS.md（不覆盖，或问用户合并策略）
- .github/workflows/（已有 CI 就不生成新的，或合并）
- .pre-commit-config.yaml（同上）
- docs/ 目录

### Phase 2：确认生成方案

把扫描结果汇总给用户确认：

```
检测到的技术栈：TypeScript + Next.js
包管理器：pnpm
Linter：Biome
Test runner：Vitest
目录结构类型：功能模块（daemon / analyzer / generator / commands）
检测到的实体：RawObservation, Observation, AnalysisResult, Config

将生成：
- CLAUDE.md — Claude 工作指令
- AGENTS.md — Codex/Cursor 工作指令
- docs/architecture.md — 基于实际目录结构
- docs/golden-principles.md — 8 条黄金原则（使用 Biome 执行）
- docs/domain-model.md — 基于扫描到的实体
- docs/onboarding.md — 基于实际命令
- scripts/layer-check.sh — 基于实际模块依赖
- scripts/init.sh — 基于实际工具链
- .github/workflows/ci.yml — 基于实际命令
- .pre-commit-config.yaml — 基于实际工具
- feature_list.json — 空模版
- agent-progress.txt — 空日志

确认？
```

用户确认后才生成。

### Phase 3：生成文件

以下是每个文件的生成规则。所有内容都基于 Phase 1 的扫描结果，**不从 GitHub 拉预置模版**。

#### 3.1 CLAUDE.md / AGENTS.md

从 GitHub 仓库拉取对应栈的模版作为**骨架**，然后用扫描结果替换所有动态内容：

```
拉取：https://raw.githubusercontent.com/ppop123/harness/main/stacks/$STACK/claude/CLAUDE.md
拉取：https://raw.githubusercontent.com/ppop123/harness/main/stacks/$STACK/codex/AGENTS.md
```

必须替换的内容：
- `[PROJECT_NAME]` → 项目名
- `[ONE_LINE_DESCRIPTION]` → 描述
- `[OWNER]` → 从 git config user.name / user.email 获取
- `[DATE]` → 今天日期
- 分层引用 → 替换为项目实际模块结构
- 命令引用 → 替换为项目实际命令（如 `pnpm lint` 而不是 `npm run lint`）
- `<!-- harness-init 适配 -->` 注释处 → 替换为真实内容

#### 3.2 docs/architecture.md

**完全根据扫描结果生成**，不用模版：

```markdown
# 架构文档 — [项目名]

## 模块结构

[从 1.3 的扫描结果生成目录树]

## 模块职责

| 模块 | 职责 | 依赖 |
|------|------|------|
[从代码的 import/require 关系推断每个模块的职责和依赖方向]

## 依赖方向

[画出实际的依赖方向，不要硬套 types → services → controllers]

## 变更记录

| 日期 | 变更 | 原因 |
|------|------|------|
| [TODAY] | 初始架构（由 harness-init 从代码扫描生成） | 项目装载 Harness |
```

#### 3.3 docs/golden-principles.md

从 GitHub 拉取对应栈的黄金原则模版，但把**执行工具替换为项目实际使用的**：

```
拉取：https://raw.githubusercontent.com/ppop123/harness/main/stacks/$STACK/docs/golden-principles.md
```

替换：
- linter 名称（ESLint → Biome）
- type checker（tsc → biome check）
- 验证库（zod → 项目实际使用的）
- 环境变量工具（@t3-oss/env-nextjs → 项目实际使用的）

#### 3.4 scripts/layer-check.sh

**完全根据扫描结果生成**：

- 如果项目是典型分层（types/services/controllers），生成标准分层检查
- 如果项目是功能模块（daemon/analyzer/generator），生成**模块边界检查**——每个模块不应该直接 import 另一个模块的内部文件
- 如果无法确定合理的依赖规则，生成一个带注释的骨架，标注 `# TODO: 根据项目实际情况补充依赖规则`
- 不允许生成一个"什么都不检查"的空壳脚本——至少检查一些基本规则

#### 3.5 scripts/init.sh

**完全根据扫描结果生成**，所有命令必须是项目里真实可运行的：

```bash
#!/usr/bin/env bash
# init.sh — 环境验证

set -euo pipefail

echo "🔧 验证环境..."

# 工具检查（从 1.2 检测到的工具）
for cmd in [实际工具列表]; do
  command -v "$cmd" &>/dev/null || { echo "✗ $cmd not found"; exit 1; }
done

# 安装依赖（从 1.2 检测到的包管理器）
[实际安装命令]

# Lint（从 1.2 检测到的 linter）
[实际 lint 命令]

# 测试（从 1.2 检测到的 test runner）
[实际 test 命令]

echo "✅ 环境验证通过"
```

#### 3.6 .github/workflows/ci.yml

同理，所有步骤使用实际命令。如果项目已有 CI 配置，问用户是合并还是跳过。

#### 3.7 .pre-commit-config.yaml

同理。如果项目已有，问用户。

#### 3.8 docs/domain-model.md

基于 1.4 扫描到的实体生成：

```markdown
# 业务领域模型

## 核心实体

### [EntityName]
描述: [从代码注释或命名推断，推断不了写 [待补充]]
关键字段:
  - [field1]: [type]
  - [field2]: [type]
所在文件: [file path]
关联实体: [从 import 关系推断]
```

没扫描到的部分标注 `[待补充]`，不要编造。

#### 3.9 docs/onboarding.md

基于实际命令生成，常用命令表必须能直接复制执行。

#### 3.10 其他文件

以下文件从 GitHub 拉取即可，不需要动态生成：

```
common/docs/tech-decisions/000-template.md → docs/tech-decisions/000-template.md
common/scripts/audit-prompt.md → scripts/audit-prompt.md
common/scripts/doc-gardening-prompt.md → scripts/doc-gardening-prompt.md
common/scripts/new-feature-prompt.md → scripts/new-feature-prompt.md
```

以下文件生成空模版：

```
feature_list.json — 只保留结构，features 数组为空
agent-progress.txt — 只保留头部说明
.env.example — 从项目已有的 .env / .env.local / docker-compose.yml 推断需要的变量，没有就留空
```

### Phase 4：验证

生成完所有文件后，必须验证：

```bash
bash scripts/init.sh         # 必须跑通
bash scripts/layer-check.sh  # 必须检查真实目录，不能空跑通过
```

如果失败，修正后重新验证，直到通过。

### Phase 5：输出摘要

```
✅ Harness 已装载

生成了 N 个文件：
- CLAUDE.md / AGENTS.md
- docs/ (architecture, golden-principles, domain-model, onboarding)
- scripts/ (init.sh, layer-check.sh, audit/doc-gardening/new-feature prompts)
- CI + pre-commit
- feature_list.json + agent-progress.txt

检测结果：
- 技术栈：[xxx]
- 包管理器：[xxx]
- Linter：[xxx]
- 模块结构：[xxx]
- 扫描到 N 个实体

下一步：
1. 检查 docs/architecture.md 的模块描述是否准确
2. 补充 docs/domain-model.md 中标记 [待补充] 的部分
3. 开始开发时先读 CLAUDE.md
```
