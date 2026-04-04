# 黄金原则 — Python AI / Data Science

> 这些原则是**机械规则**，每条对应一个 lint 或 CI 检查。

## 原则列表

| # | 原则 | 检查方式 |
|---|------|---------|
| G1 | 类型安全 | mypy (moderate) |
| G2 | 边界验证：外部数据必须校验 | Pydantic |
| G3 | 不重复（DRY）：>2 处重复必须提取 | 代码审计 |
| G4 | 错误必须处理：不允许静默吞掉 | Ruff |
| G5 | 禁止硬编码配置 | python-dotenv |
| G6 | 函数单一职责：上限 50 行 | Ruff |
| G7 | 关键路径必须有测试 | pytest |
| G8 | 依赖层级不可违反 | 结构测试 |

---

## G1 — 类型安全

```
❌ 禁止：# Jupyter notebook 里写 500 行 + 训练 + 部署

✅ 正确：# Notebook 只做探索；pipeline 代码在 src/pipelines/
```

## G2 — 数据边界验证

```
# ❌ 硬编码超参数
model = train(lr=0.001, epochs=50, batch_size=32)

# ✅ 配置化
@dataclass
class TrainConfig:
    lr: float = 0.001
    epochs: int = 50
    batch_size: int = 32
model = train(config=TrainConfig())
```

## G4 — 错误处理

所有错误必须被处理：要么向上抛出，要么记录日志。不允许空的 catch/except 块。

## G5 — 禁止硬编码

所有配置值（API keys、URL、端口等）必须通过 python-dotenv 管理。

## G6 — 函数单一职责

一个函数只做一件事。超过 50 行必须重新评估是否可拆分。

## G7 — 关键路径测试

以下必须有自动化测试：
- Service 层的核心业务逻辑
- API endpoint 的参数验证
- 涉及金额、权限的计算

## 违规处理

- **G1/G2/G4/G5 违规** → CI 自动拦截
- **G3/G6 违规** → 代码审计时标记
- **G7 违规** → PR review 时拒绝
