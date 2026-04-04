# 上手指南 — Dart + Flutter

## 第一步：理解项目

```
1. AGENTS.md 或 CLAUDE.md  （项目概览）
2. docs/domain-model.md     （业务领域）
3. docs/architecture.md     （代码结构）
4. docs/golden-principles.md（代码规范）
```

## 第二步：环境配置

```bash
# 安装依赖
pub install  # 根据项目实际调整

# 启动开发
flutter run
```

## 第三步：开发工作流

```
1. 读 docs/domain-model.md → 确认涉及哪些实体
2. 读 docs/architecture.md → 确认在哪个层实现
3. 写代码（按层级顺序）
4. 运行检查：dart analyze && flutter test
5. 提交 PR
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `flutter run` | 启动开发 |
| `dart analyze && dart format --set-exit-if-changed .` | 代码检查 |
| `flutter test` | 运行测试 |
| `dart analyze && flutter test` | 完整检查（提交前跑） |

## 定期维护

| 频率 | 任务 |
|------|------|
| 每周 | 代码审计（`scripts/audit-prompt.md`）|
| 每周 | 文档更新（`scripts/doc-gardening-prompt.md`）|
