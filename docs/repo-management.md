# Harness Repo Management Guide

## 仓库目标

`harness` 不是示例应用仓库，而是一个 Harness Engineering 模版仓库。它的核心产出是：

- 对 AI 友好的入口文档
- 可执行的工程约束
- 可复制到不同技术栈的初始化脚本、CI 和检查脚本
- 跨 session 的任务与进度工件

这里最重要的原则不是“文档写得多”，而是“规则能被执行”。

## 事实来源

### 1. `generate_repo.py`

这是 stack 模板的主要事实来源，负责生成：

- `stacks/*/claude/CLAUDE.md`
- `stacks/*/codex/AGENTS.md`
- `stacks/*/docs/*`
- `stacks/*/scripts/*`
- `stacks/*/config/*`
- `stacks/*/ci/ci.yml`
- 根 `README.md`
- `manifest.json`
- `common/feature_list.json`
- `common/agent-progress.txt`

如果某个 stack 的约束、README、脚本、CI 需要改，默认都先改这里，再重新生成。

### 2. `common/`

`common/` 是所有 stack 共享的可直接编辑区，适合放：

- 领域模型模板
- ADR 模板
- 审计 / 文档整理 prompt
- `.env.example`

### 3. `skills/harness-init/`

`skills/harness-init/SKILL.md` 是 thin loader skill 的源码入口。

- 修改 skill 行为，改这里
- 重新打 release asset，运行 `python3 scripts/build_harness_init_skill.py`
- 不要直接把 `harness-init.skill` 当成唯一事实来源

### 4. 根级入口文档

根 `AGENTS.md` 和 `CLAUDE.md` 只做短入口，不承载完整维护手册。完整说明统一写在这里，避免双份长文档漂移。

## 日常修改规则

### 改某个技术栈模板

1. 修改 `generate_repo.py`
2. 先跑或补测试
3. 执行 `python3 generate_repo.py`
4. 抽查代表性生成结果

### 改共享模板

直接改 `common/`，必要时补测试或 README 说明。

### 改根级维护文档

改：

- `AGENTS.md`
- `CLAUDE.md`
- `docs/repo-management.md`

要求：

- 根入口继续保持短
- 不与生成器产出冲突
- 不硬编码过时文件名或路径

## 平台差异约定

### Claude

- `CLAUDE.md` 更适合对话式、分阶段、逐步汇报
- 可以强调“先说理解和计划”
- 但不能依赖一个并不存在的 `AGENTS.md`

### Codex / Cursor / Windsurf

- `AGENTS.md` 更适合统一入口和机械化执行
- 应优先强调固定验证命令、事实来源和修改边界
- 不应引用带平台品牌色彩的共享工件名

### 推荐安装入口

- 推荐流程是两步：
  1. 先安装一个很薄的 `harness-init` skill
  2. 再在具体项目里让它从 GitHub 按需拉取所需 stack 文件
- 对 Codex，推荐通过内置的 `$skill-installer` 从 `ppop123/harness` 的 `skills/harness-init` 安装这个 skill。
- 对 Claude，可以继续通过 release asset 安装 `harness-init.skill`，但这个 asset 也必须是 thin loader，而不是模板打包文件。
- 项目装载阶段的推荐请求形态是：
  `从 https://github.com/ppop123/harness 装载 ts-nextjs 栈的 harness 工程结构到当前目录`

### `harness-init` 的设计约束

- `harness-init.skill` 只负责收集参数、决定平台版本、从 GitHub 拉取文件。
- 不要在 skill 中内置各技术栈模板文件，不要再放 `assets/ts-nextjs/`、`assets/common/` 这类副本。
- GitHub 上的 `stacks/` 与 `common/` 才是模板事实来源；skill 只是 loader。
- skill 的源码应保存在仓库里，例如 `skills/harness-init/SKILL.md`，而不是只保留一个二进制 `.skill` 文件。

### 共享工件命名

跨工具共享的状态文件、进度文件、模板文件，尽量使用中性名称，例如：

- `agent-progress.txt`

避免出现只有某个平台能“认领”的命名。

## Harness Engineering 检查清单

每次做仓库级修改时，至少自查这几条：

1. 入口文件是否短小，详细规则是否下沉到 `docs/`
2. 关键规则是否有脚本、CI、测试或 pre-commit 做机械化执行
3. README 的 bootstrap 路径是否真的存在
4. 生成器、README、根入口文档是否口径一致
5. 代表性 stack 的生成产物是否能通过最小 smoke test

## 关于 `layer-check.sh`

当前版本的 `layer-check.sh` 已经不是简单的路径关键词扫描，而是：

- 对 Python 使用标准库 `ast` 解析 import
- 对 TypeScript、Dart、Go、Rust、Java、Kotlin、C#、Swift 使用语言感知的 import/use 提取
- 再将真实依赖目标与各层禁用别名做归一化匹配

这让它比纯 `grep` 更接近真正的结构约束，也更不容易被注释或普通字符串误报。

### 当前限制

- `layer-check.sh` 仍然是启发式静态检查，不是完整编译器插件。
- 对 Swift 这类同模块文件通常不会通过 import 表达本地分层依赖，因此仍然只能做保守回退，严格性弱于 Python / TypeScript / Go 这类导入路径更清晰的栈。
- 运行脚本需要 `python3` 或 `python` 作为分析运行时；脚本会在缺失时直接报错。

## 推荐验证顺序

```bash
python3 -m unittest discover -s tests -q
python3 generate_repo.py
python3 -m unittest discover -s tests -q
```

必要时再补：

- 手工运行某个生成出来的 `layer-check.sh`
- 抽查 `stacks/ts-nextjs/`、`stacks/swift-ios/` 这类能覆盖 Web 与客户端差异的模板

## 发布与维护

发布前建议确认：

- 生成器改动已重新生成
- 根 README 已更新
- `skills/harness-init/SKILL.md` 与 README 描述一致
- `python3 scripts/build_harness_init_skill.py` 能生成最新的 thin `harness-init.skill`
- skill 包中没有内置 stack/common 资产副本
- 代表性 stack README 没有乱码或路径漂移

未来如需继续加强严格性，优先顺序建议是：

1. 提高 `layer-check.sh` 的语言感知能力
2. 给 root docs / root README 增加更硬的回归测试
3. 让更多 stack 的 CI 与 README 示例完全一致
