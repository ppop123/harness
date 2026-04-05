# Swift + SwiftUI — Harness Engineering 模板

**分类**：iOS / macOS 客户端
**语言**：Swift
**框架**：SwiftUI + Combine / Swift Concurrency

## 包含文件

| 文件 | 说明 |
|------|------|
| `claude/CLAUDE.md` | Claude / Claude Code 专属指令 |
| `codex/AGENTS.md` | Codex / Cursor / 通用 AI Agent 指令 |
| `config/lint-config.txt` | Lint / 类型检查配置 |
| `config/pre-commit-config.yaml` | Pre-commit hooks 配置 |
| `scripts/layer-check.sh` | 依赖层级结构测试（语言感知导入检查） |
| `scripts/init.sh` | 环境验证 + baseline 测试脚本 |
| `ci/ci.yml` | GitHub Actions CI 模板 |
| `docs/` | 架构、原则、领域模型（使用 common/ 的模板）|

## 使用方法

**推荐装载**（需先安装 `harness-init` skill）：

```text
从 https://github.com/ppop123/harness 装载 swift-ios 栈的 harness 工程结构到当前目录
```

**手动方式**：

1. Claude 用户可复制 `claude/CLAUDE.md` 到项目根目录；Codex 用户可复制 `codex/AGENTS.md`
2. 将 `config/` 中的配置合并到你的项目
3. 将 `common/docs/` 复制到 `docs/`
4. 填写 `[PROJECT_NAME]` 等占位符

## 工具链

| 工具 | 用途 |
|------|------|
| SwiftLint | 代码检查 |
| Swift 编译器（静态类型） | 类型检查 |
| XCTest | 测试 |
| swift-format | 格式化 |
| 自定义 Validator 或 ValidatedPropertyKit | 数据验证 |
