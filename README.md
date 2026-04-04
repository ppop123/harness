# Harness Engineering Templates

> 基于 [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) 思想，
> 为 **13 种主流技术栈** 提供标准化的 AI-first 项目模版。
> 每个技术栈同时支持 **Claude（CLAUDE.md）** 和 **Codex（AGENTS.md）** 双版本。

---

## 支持的技术栈

| 技术栈 | 分类 | 语言 | 框架 |
|--------|------|------|------|
| [TypeScript + Next.js](stacks/ts-nextjs/) | 全栈 Web（React 生态） | TypeScript | Next.js |
| [TypeScript + Node.js API](stacks/ts-node/) | 后端 REST/GraphQL API | TypeScript | Express / Fastify / NestJS |
| [Python + FastAPI](stacks/python-fastapi/) | Python 高性能 API | Python | FastAPI |
| [Python + Django](stacks/python-django/) | Python 全栈 Web | Python | Django + DRF |
| [Python AI / Data Science](stacks/python-ai/) | AI / ML / 数据项目 | Python | PyTorch / LangChain / Pandas |
| [Java + Spring Boot](stacks/java-spring/) | 企业级 Java 后端 | Java | Spring Boot 3 |
| [C# + ASP.NET Core](stacks/csharp-dotnet/) | .NET 企业级后端 | C# | ASP.NET Core 8+ |
| [Go](stacks/go/) | Go 云原生后端 | Go | 标准库 / Gin / Fiber / Echo |
| [Rust](stacks/rust/) | Rust 高性能后端 / 系统 | Rust | Axum / Actix-web |
| [Swift + SwiftUI](stacks/swift-ios/) | iOS / macOS 客户端 | Swift | SwiftUI + Combine / Swift Concurrency |
| [Kotlin + Android](stacks/kotlin-android/) | Android 客户端 | Kotlin | Jetpack Compose + Hilt + Coroutines |
| [Dart + Flutter](stacks/dart-flutter/) | 跨平台客户端（iOS + Android + Web） | Dart | Flutter + Riverpod / Bloc |
| [React Native (TypeScript)](stacks/react-native/) | 跨平台客户端（JS 生态） | TypeScript | React Native + Expo |


## 常用组合

| 组合 | 组成 |
|------|------|
| [Next.js 前端 + Python FastAPI 后端](combos/nextjs-python-api/) | `ts-nextjs` + `python-fastapi` |
| [React SPA + Go 后端](combos/react-go-api/) | `ts-nextjs` + `go` |
| [Flutter 客户端 + FastAPI 后端](combos/flutter-fastapi/) | `dart-flutter` + `python-fastapi` |
| [Next.js 前端 + Spring Boot 后端](combos/nextjs-spring/) | `ts-nextjs` + `java-spring` |
| [React Native 客户端 + Node.js API](combos/rn-node/) | `react-native` + `ts-node` |


## 仓库结构

```
harness/
├── common/              # 所有项目通用的文档和脚本
│   ├── docs/            # 领域模型、ADR 模版
│   ├── scripts/         # AI 审计/维护 prompt
│   ├── feature_list.json    # 功能追踪模版（JSON 防误改）
│   └── agent-progress.txt      # 跨 session 进度日志模版
├── stacks/              # 按技术栈分类
│   └── <stack-name>/
│       ├── claude/      # CLAUDE.md（Claude 专属）
│       ├── codex/       # AGENTS.md（Codex / 通用）
│       ├── config/      # Lint + pre-commit 配置
│       ├── scripts/     # layer-check.sh + init.sh（机械化执行）
│       ├── ci/          # GitHub Actions CI 模版
│       └── docs/        # 架构、原则（技术栈专属）
└── combos/              # 常用前后端组合
```

## 使用方式

### 方式 1：安装薄装载 Skill（推荐）

**Codex / Cursor / Windsurf**：

```text
请用 $skill-installer 从 ppop123/harness 的 skills/harness-init 安装 harness-init
```

**Claude Code**：

```bash
curl -sL https://github.com/ppop123/harness/releases/latest/download/harness-init.skill -o /tmp/harness-init.skill && claude skill install /tmp/harness-init.skill
```

安装完成后，`harness-init` 只负责收集参数并从 GitHub 按需拉取当前栈文件，不内置栈模板副本。

### 方式 2：在项目目录装载

```text
从 https://github.com/ppop123/harness 装载 ts-nextjs 栈的 harness 工程结构到当前目录
```

> 把 `ts-nextjs` 替换为你的技术栈 ID（见上方表格）。
> 你也可以在请求里明确写 `Claude`、`Codex` 或 `都要`，skill 会据此决定写入 `CLAUDE.md`、`AGENTS.md` 或两者都写。

### 方式 3：手动复制

```bash
git clone https://github.com/ppop123/harness.git
cp stacks/ts-nextjs/claude/CLAUDE.md your-project/CLAUDE.md
cp stacks/ts-nextjs/codex/AGENTS.md your-project/AGENTS.md
cp -r common/docs your-project/docs
cp -r common/scripts your-project/scripts
```

### 方式 4：curl 完整初始化（fallback）

```bash
STACK=ts-nextjs && REPO=https://raw.githubusercontent.com/ppop123/harness/main && \
curl -sL "$REPO/stacks/$STACK/codex/AGENTS.md" -o AGENTS.md && \
mkdir -p docs scripts && \
curl -sL "$REPO/stacks/$STACK/docs/architecture.md" -o docs/architecture.md && \
curl -sL "$REPO/stacks/$STACK/docs/golden-principles.md" -o docs/golden-principles.md && \
curl -sL "$REPO/common/docs/domain-model.md" -o docs/domain-model.md && \
curl -sL "$REPO/stacks/$STACK/scripts/layer-check.sh" -o scripts/layer-check.sh && \
curl -sL "$REPO/stacks/$STACK/scripts/init.sh" -o scripts/init.sh && \
curl -sL "$REPO/common/feature_list.json" -o feature_list.json && \
curl -sL "$REPO/common/agent-progress.txt" -o agent-progress.txt && \
echo "Harness installed. Run: bash scripts/init.sh"
```

> 把 `ts-nextjs` 替换为你的技术栈 ID（见上方表格）

## Claude vs Codex：区别在哪？

| 维度 | CLAUDE.md | AGENTS.md |
|------|-----------|-----------|
| 消费者 | Claude Code / Cowork | Codex CLI / Cursor / Windsurf / 通用 |
| 交互风格 | 对话式、渐进式 | 机械化、跨工具通用 |
| 上下文策略 | 更强调分层阅读和汇报 | 更强调统一入口与可执行规则 |
| 建议 | Claude 用户首选 | 多工具团队首选 |

## 核心理念

来自 OpenAI Harness Engineering：

1. **你的产出不是代码，是约束系统** — 设计让 AI 不得不写出好代码的环境
2. **入口文件要短** — 根入口只做索引，细节下沉到 `docs/`
3. **黄金原则机械化** — 用 linter/CI/脚本执行，不靠 prompt 嘱咐
4. **自动垃圾回收** — 定期让 AI 审计代码，自动清理与补文档
5. **为 AI 可读性优化** — 写类型、写文档、写注释，是给下一次 AI 看的

---

*Generated on 2026-04-04*
