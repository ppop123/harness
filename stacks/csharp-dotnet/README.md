# C# + ASP.NET Core — Harness Engineering 模版

**分类**：.NET 企业级后端
**语言**：C#
**框架**：ASP.NET Core 8+

## 包含文件

| 文件 | 说明 |
|------|------|
| `claude/CLAUDE.md` | Claude / Claude Code 专属指令 |
| `codex/AGENTS.md` | Codex / Cursor / 通用 AI Agent 指令 |
| `config/lint-config.txt` | Lint / 类型检查配置 |
| `config/pre-commit-config.yaml` | Pre-commit hooks 配置 |
| `scripts/layer-check.sh` | 依赖层级结构测试（语言感知导入检查） |
| `scripts/init.sh` | 环境验证 + baseline 测试脚本 |
| `ci/ci.yml` | GitHub Actions CI 模版 |
| `docs/` | 架构、原则、领域模型（使用 common/ 的模版）|

## 使用方法

1. Claude 用户复制 `claude/CLAUDE.md` 到项目根目录；Codex 用户复制 `codex/AGENTS.md`
2. 将 `config/` 中的配置合并到你的项目
3. 将 `common/docs/` 复制到 `docs/`
4. 填写 `[PROJECT_NAME]` 等占位符

## 工具链

| 工具 | 用途 |
|------|------|
| .NET Analyzers + StyleCop | 代码检查 |
| C# 编译器（静态类型） + Nullable reference types | 类型检查 |
| xUnit + Moq | 测试 |
| dotnet format | 格式化 |
| FluentValidation / DataAnnotations | 数据验证 |
