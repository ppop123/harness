# 黄金原则 — Rust

> 这些原则是**机械规则**，每条对应一个 lint 或 CI 检查。

## 原则列表

| # | 原则 | 检查方式 |
|---|------|---------|
| G1 | 类型安全 | Rust 编译器（强类型 + 所有权） |
| G2 | 边界验证：外部数据必须校验 | serde + validator |
| G3 | 不重复（DRY）：>2 处重复必须提取 | 代码审计 |
| G4 | 错误必须处理：不允许静默吞掉 | Clippy |
| G5 | 禁止硬编码配置 | config-rs / dotenvy |
| G6 | 函数单一职责：上限 50 行 | Clippy |
| G7 | 关键路径必须有测试 | cargo test |
| G8 | 依赖层级不可违反 | 结构测试 |

---

## G1 — 类型安全

```
❌ 禁止：.unwrap() 到处用，忽略错误处理

✅ 正确：用 ? 运算符 + 自定义 Error 类型 + thiserror
```

## G2 — 数据边界验证

```
// ❌
let data: serde_json::Value = serde_json::from_slice(&body)?;
let email = data["email"].as_str().unwrap();

// ✅
#[derive(Deserialize, Validate)]
struct CreateUser {
    #[validate(email)] email: String,
    #[validate(length(min = 1))] name: String,
}
let req: CreateUser = serde_json::from_slice(&body)?;
req.validate()?;
```

## G4 — 错误处理

所有错误必须被处理：要么向上抛出，要么记录日志。不允许空的 catch/except 块。

## G5 — 禁止硬编码

所有配置值（API keys、URL、端口等）必须通过 config-rs / dotenvy 管理。

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
