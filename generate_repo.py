#!/usr/bin/env python3
"""
Harness Engineering Templates — Full Repo Generator
Generates complete GitHub repo with 13 stacks × Claude/Codex dual versions.
"""

import os
import json
import textwrap
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
TODAY = date.today().isoformat()
PROGRESS_FILE = "agent-progress.txt"

LAYER_CHECK_ALIASES = {
    "ts-nextjs": [
        ["types"],
        ["config"],
        ["lib", "utils"],
        ["repositories"],
        ["services"],
        ["app/api", "api", "routes"],
        ["app", "components", "pages", "ui"],
    ],
    "ts-node": [
        ["types"],
        ["config"],
        ["utils", "lib"],
        ["repositories"],
        ["services"],
        ["controllers"],
        ["routes"],
    ],
    "python-fastapi": [
        ["models"],
        ["config"],
        ["utils", "common"],
        ["repositories"],
        ["services"],
        ["routes"],
    ],
    "python-django": [
        ["models"],
        ["managers"],
        ["services"],
        ["serializers"],
        ["views"],
        ["urls"],
    ],
    "python-ai": [
        ["config"],
        ["data"],
        ["models"],
        ["pipelines"],
        ["evaluation"],
        ["api", "ui"],
    ],
    "java-spring": [
        ["dto"],
        ["config"],
        ["repository"],
        ["service"],
        ["controller"],
    ],
    "csharp-dotnet": [
        ["DTOs"],
        ["Config"],
        ["Repositories", "repository"],
        ["Services", "service"],
        ["Controllers", "controller"],
    ],
    "go": [
        ["internal/domain", "domain"],
        ["internal/repository", "repository"],
        ["internal/service", "service"],
        ["internal/handler", "handler"],
        ["router", "cmd/server", "routes"],
    ],
    "rust": [
        ["models"],
        ["config"],
        ["repository"],
        ["service"],
        ["handler"],
        ["router"],
    ],
    "swift-ios": [
        ["Models"],
        ["Repositories"],
        ["Services"],
        ["ViewModels"],
        ["Views"],
    ],
    "kotlin-android": [
        ["data/model", "domain/model"],
        ["data/repository", "domain/repository"],
        ["domain/usecase"],
        ["presentation/viewmodel"],
        ["presentation/ui", "ui"],
    ],
    "dart-flutter": [
        ["models"],
        ["data/remote", "data/local"],
        ["repositories"],
        ["providers", "blocs"],
        ["ui"],
    ],
    "react-native": [
        ["types"],
        ["config"],
        ["services", "api"],
        ["hooks"],
        ["screens"],
        ["components"],
    ],
}

# ============================================================
# STACK DEFINITIONS
# ============================================================

STACKS = {
    # ---- Frontend / Fullstack Web ----
    "ts-nextjs": {
        "name": "TypeScript + Next.js",
        "category": "fullstack-web",
        "label": "全栈 Web（React 生态）",
        "lang": "TypeScript",
        "framework": "Next.js",
        "package_manager": "npm / pnpm",
        "linter": "ESLint + @typescript-eslint",
        "type_checker": "TypeScript strict mode",
        "test_runner": "Vitest",
        "formatter": "Prettier",
        "validation": "zod",
        "env_tool": "@t3-oss/env-nextjs",
        "layers": "Types → Config → Utils → Repositories → Services → API Routes → UI/Pages",
        "dir_structure": """src/
├── types/              # 类型定义
├── lib/                # 纯工具函数
├── config/             # 环境变量、常量
├── repositories/       # 数据访问层
├── services/           # 业务逻辑层
├── app/
│   ├── api/            # API Routes
│   └── (routes)/       # 页面
└── components/         # 共享 UI 组件""",
        "lint_config": """{
  "extends": ["next/core-web-vitals", "plugin:@typescript-eslint/recommended-type-checked"],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-floating-promises": "error",
    "no-empty": ["error", {"allowEmptyCatch": false}],
    "complexity": ["warn", 10],
    "max-lines-per-function": ["warn", {"max": 50, "skipBlankLines": true, "skipComments": true}]
  }
}""",
        "commands": {
            "dev": "npm run dev",
            "lint": "npm run lint && tsc --noEmit",
            "test": "npx vitest run",
            "check": "npm run lint && tsc --noEmit && npx vitest run"
        },
        "bad_example": 'function processUser(user: any) { ... }',
        "good_example": 'function processUser(user: User): ProcessedUser { ... }',
        "validation_example": """// ❌ 禁止
const data = await req.json()
await createUser(data.email)

// ✅ 正确
const body = await req.json()
const data = CreateUserSchema.parse(body)
await createUser(data.email)""",
    },

    "ts-node": {
        "name": "TypeScript + Node.js API",
        "category": "backend-api",
        "label": "后端 REST/GraphQL API",
        "lang": "TypeScript",
        "framework": "Express / Fastify / NestJS",
        "package_manager": "npm / pnpm",
        "linter": "ESLint + @typescript-eslint",
        "type_checker": "TypeScript strict mode",
        "test_runner": "Vitest / Jest",
        "formatter": "Prettier",
        "validation": "zod / class-validator (NestJS)",
        "env_tool": "dotenv + zod",
        "layers": "Types → Config → Utils → Repositories → Services → Controllers → Routes",
        "dir_structure": """src/
├── types/              # 类型定义 & DTOs
├── config/             # 环境变量
├── utils/              # 纯工具函数
├── repositories/       # 数据访问
├── services/           # 业务逻辑
├── controllers/        # 请求处理
├── routes/             # 路由定义
├── middleware/          # 中间件
└── tests/""",
        "lint_config": """{
  "extends": ["plugin:@typescript-eslint/recommended-type-checked"],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-floating-promises": "error",
    "no-empty": ["error", {"allowEmptyCatch": false}]
  }
}""",
        "commands": {
            "dev": "npx tsx watch src/index.ts",
            "lint": "eslint src/ && tsc --noEmit",
            "test": "npx vitest run",
            "check": "npm run lint && npm run test"
        },
        "bad_example": 'function processUser(user: any) { ... }',
        "good_example": 'function processUser(user: User): ProcessedUser { ... }',
        "validation_example": """// ❌
app.post('/users', (req, res) => { createUser(req.body.email) })

// ✅
const schema = z.object({ email: z.string().email() })
app.post('/users', (req, res) => {
  const data = schema.parse(req.body)
  createUser(data.email)
})""",
    },

    "python-fastapi": {
        "name": "Python + FastAPI",
        "category": "backend-api",
        "label": "Python 高性能 API",
        "lang": "Python",
        "framework": "FastAPI",
        "package_manager": "pip / uv / poetry",
        "linter": "Ruff",
        "type_checker": "mypy --strict",
        "test_runner": "pytest",
        "formatter": "Ruff format",
        "validation": "Pydantic v2",
        "env_tool": "pydantic-settings",
        "layers": "Models → Config → Utils → Repositories → Services → Routes",
        "dir_structure": """src/
├── models/             # Pydantic models & DB models
├── config/             # Settings (pydantic-settings)
├── utils/              # 纯工具函数
├── repositories/       # 数据访问
├── services/           # 业务逻辑
├── routes/             # FastAPI routers
├── middleware/          # 中间件
└── tests/""",
        "lint_config": """[tool.ruff.lint]
select = ["E","W","F","I","B","C4","UP","N","ANN","S","TRY","SIM"]

[tool.mypy]
strict = true""",
        "commands": {
            "dev": "uvicorn src.main:app --reload",
            "lint": "ruff check src/ && mypy src/",
            "test": "pytest tests/ -v",
            "check": "make lint && make test"
        },
        "bad_example": "def process_user(user):\n    return user['name']",
        "good_example": "def process_user(user: User) -> str:\n    return user.name",
        "validation_example": """# ❌
@app.post("/users")
def create_user(request: dict): ...

# ✅
class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1)

@app.post("/users")
def create_user(request: CreateUserRequest): ...""",
    },

    "python-django": {
        "name": "Python + Django",
        "category": "fullstack-web",
        "label": "Python 全栈 Web",
        "lang": "Python",
        "framework": "Django + DRF",
        "package_manager": "pip / uv / poetry",
        "linter": "Ruff",
        "type_checker": "mypy + django-stubs",
        "test_runner": "pytest-django",
        "formatter": "Ruff format",
        "validation": "Django serializers / Pydantic",
        "env_tool": "django-environ",
        "layers": "Models → Managers → Services → Serializers → Views → URLs",
        "dir_structure": """project/
├── apps/
│   └── <app_name>/
│       ├── models.py       # 数据模型
│       ├── managers.py     # 自定义 QuerySet
│       ├── services.py     # 业务逻辑（不放 views 里！）
│       ├── serializers.py  # API 序列化/验证
│       ├── views.py        # 请求处理
│       ├── urls.py         # 路由
│       └── tests/
├── config/                 # Django settings
└── common/                 # 共享工具""",
        "lint_config": """[tool.ruff.lint]
select = ["E","W","F","I","B","C4","UP","N","ANN","S","DJ"]

[tool.mypy]
strict = true
plugins = ["mypy_django_plugin.main"]""",
        "commands": {
            "dev": "python manage.py runserver",
            "lint": "ruff check . && mypy .",
            "test": "pytest --ds=config.settings.test",
            "check": "make lint && make test"
        },
        "bad_example": "# views.py 里写 300 行业务逻辑",
        "good_example": "# views.py 调用 services.py，services 调用 managers.py",
        "validation_example": """# ❌ View 里直接操作数据
class UserView(APIView):
    def post(self, request):
        User.objects.create(**request.data)  # 危险！

# ✅ 通过 Serializer 验证 + Service 处理
class UserView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_service.register(serializer.validated_data)""",
    },

    "python-ai": {
        "name": "Python AI / Data Science",
        "category": "ai-data",
        "label": "AI / ML / 数据项目",
        "lang": "Python",
        "framework": "PyTorch / LangChain / Pandas",
        "package_manager": "pip / uv / conda",
        "linter": "Ruff",
        "type_checker": "mypy (moderate)",
        "test_runner": "pytest",
        "formatter": "Ruff format",
        "validation": "Pydantic",
        "env_tool": "python-dotenv",
        "layers": "Config → Data → Models → Pipelines → Evaluation → API/UI",
        "dir_structure": """project/
├── src/
│   ├── config/          # 环境变量、超参数
│   ├── data/            # 数据加载/清洗
│   ├── models/          # 模型定义
│   ├── pipelines/       # 训练/推理流水线
│   ├── evaluation/      # 评估指标
│   └── api/             # 模型服务 API
├── notebooks/           # 探索性分析（不含业务逻辑）
├── experiments/         # 实验记录
└── tests/""",
        "lint_config": """[tool.ruff.lint]
select = ["E","W","F","I","B","UP","N","ANN"]
ignore = ["ANN101"]

[tool.mypy]
warn_return_any = true
disallow_untyped_defs = true""",
        "commands": {
            "dev": "jupyter lab",
            "lint": "ruff check src/",
            "test": "pytest tests/ -v",
            "check": "ruff check src/ && mypy src/ && pytest tests/"
        },
        "bad_example": "# Jupyter notebook 里写 500 行 + 训练 + 部署",
        "good_example": "# Notebook 只做探索；pipeline 代码在 src/pipelines/",
        "validation_example": """# ❌ 硬编码超参数
model = train(lr=0.001, epochs=50, batch_size=32)

# ✅ 配置化
@dataclass
class TrainConfig:
    lr: float = 0.001
    epochs: int = 50
    batch_size: int = 32
model = train(config=TrainConfig())""",
    },

    "java-spring": {
        "name": "Java + Spring Boot",
        "category": "backend-api",
        "label": "企业级 Java 后端",
        "lang": "Java",
        "framework": "Spring Boot 3",
        "package_manager": "Maven / Gradle",
        "linter": "Checkstyle + SpotBugs",
        "type_checker": "Java 编译器（静态类型）",
        "test_runner": "JUnit 5 + Mockito",
        "formatter": "google-java-format",
        "validation": "Jakarta Validation (Bean Validation)",
        "env_tool": "application.yml + @ConfigurationProperties",
        "layers": "DTO → Config → Repository → Service → Controller",
        "dir_structure": """src/main/java/com/example/project/
├── dto/                # 数据传输对象
├── entity/             # JPA 实体
├── config/             # 配置类
├── repository/         # Spring Data JPA
├── service/            # 业务逻辑
├── controller/         # REST 控制器
└── exception/          # 全局异常处理

src/test/java/com/example/project/
└── (镜像结构)""",
        "lint_config": """<!-- pom.xml -->
<plugin>
  <groupId>com.puppycrawl.tools</groupId>
  <artifactId>maven-checkstyle-plugin</artifactId>
  <configuration>
    <configLocation>google_checks.xml</configLocation>
    <failOnViolation>true</failOnViolation>
  </configuration>
</plugin>""",
        "commands": {
            "dev": "./mvnw spring-boot:run",
            "lint": "./mvnw checkstyle:check",
            "test": "./mvnw test",
            "check": "./mvnw verify"
        },
        "bad_example": "@Controller 里写 200 行数据库查询",
        "good_example": "Controller → Service → Repository，每层单一职责",
        "validation_example": """// ❌
@PostMapping("/users")
public User create(@RequestBody Map<String, Object> body) { ... }

// ✅
public record CreateUserRequest(
    @NotBlank @Email String email,
    @NotBlank @Size(min=1, max=100) String name
) {}

@PostMapping("/users")
public User create(@Valid @RequestBody CreateUserRequest request) { ... }""",
    },

    "csharp-dotnet": {
        "name": "C# + ASP.NET Core",
        "category": "backend-api",
        "label": ".NET 企业级后端",
        "lang": "C#",
        "framework": "ASP.NET Core 8+",
        "package_manager": "NuGet / dotnet CLI",
        "linter": ".NET Analyzers + StyleCop",
        "type_checker": "C# 编译器（静态类型） + Nullable reference types",
        "test_runner": "xUnit + Moq",
        "formatter": "dotnet format",
        "validation": "FluentValidation / DataAnnotations",
        "env_tool": "appsettings.json + IOptions<T>",
        "layers": "DTOs → Config → Repositories → Services → Controllers",
        "dir_structure": """src/
├── ProjectName.Api/          # API 入口
│   ├── Controllers/
│   ├── DTOs/
│   └── Program.cs
├── ProjectName.Core/         # 业务逻辑
│   ├── Entities/
│   ├── Interfaces/
│   └── Services/
├── ProjectName.Infrastructure/ # 数据访问
│   ├── Data/
│   └── Repositories/
└── ProjectName.Tests/""",
        "lint_config": """<!-- .editorconfig -->
[*.cs]
dotnet_analyzer_diagnostic.severity = warning
dotnet_diagnostic.CA1062.severity = error  # Validate arguments
dotnet_diagnostic.CS8600.severity = error  # Nullable reference""",
        "commands": {
            "dev": "dotnet run --project src/ProjectName.Api",
            "lint": "dotnet format --verify-no-changes",
            "test": "dotnet test",
            "check": "dotnet build --warnaserror && dotnet test"
        },
        "bad_example": "public object GetUser(dynamic id) => ...",
        "good_example": "public async Task<UserDto> GetUser(Guid id) => ...",
        "validation_example": """// ❌
[HttpPost] public IActionResult Create([FromBody] dynamic data) { ... }

// ✅
public class CreateUserRequest : IValidatableObject { ... }
[HttpPost] public IActionResult Create([FromBody] CreateUserRequest request) { ... }""",
    },

    "go": {
        "name": "Go",
        "category": "backend-api",
        "label": "Go 云原生后端",
        "lang": "Go",
        "framework": "标准库 / Gin / Fiber / Echo",
        "package_manager": "go mod",
        "linter": "golangci-lint",
        "type_checker": "Go 编译器（静态类型）",
        "test_runner": "go test + testify",
        "formatter": "gofmt / goimports",
        "validation": "go-playground/validator",
        "env_tool": "envconfig / viper",
        "layers": "Domain → Repository → Service → Handler → Router",
        "dir_structure": """project/
├── cmd/
│   └── server/main.go    # 入口
├── internal/
│   ├── domain/            # 实体 + 接口定义
│   ├── repository/        # 数据访问实现
│   ├── service/           # 业务逻辑
│   └── handler/           # HTTP 处理器
├── pkg/                   # 可导出的工具包
├── config/                # 配置
└── tests/""",
        "lint_config": """# .golangci.yml
linters:
  enable:
    - errcheck
    - govet
    - staticcheck
    - unused
    - gosimple
    - ineffassign
    - misspell
    - gocyclo
  settings:
    gocyclo:
      min-complexity: 10""",
        "commands": {
            "dev": "go run cmd/server/main.go",
            "lint": "golangci-lint run ./...",
            "test": "go test ./... -v -race",
            "check": "golangci-lint run ./... && go test ./... -v -race"
        },
        "bad_example": "func handleUser(w http.ResponseWriter, r *http.Request) {\n  // 200 行混合了 DB 查询 + 业务逻辑 + JSON 序列化\n}",
        "good_example": "Handler → Service → Repository，接口驱动依赖注入",
        "validation_example": """// ❌
func CreateUser(w http.ResponseWriter, r *http.Request) {
    var data map[string]interface{}
    json.NewDecoder(r.Body).Decode(&data)
}

// ✅
type CreateUserRequest struct {
    Email string `json:"email" validate:"required,email"`
    Name  string `json:"name"  validate:"required,min=1"`
}
func CreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    json.NewDecoder(r.Body).Decode(&req)
    validate.Struct(req)
}""",
    },

    "rust": {
        "name": "Rust",
        "category": "backend-systems",
        "label": "Rust 高性能后端 / 系统",
        "lang": "Rust",
        "framework": "Axum / Actix-web",
        "package_manager": "Cargo",
        "linter": "Clippy",
        "type_checker": "Rust 编译器（强类型 + 所有权）",
        "test_runner": "cargo test",
        "formatter": "rustfmt",
        "validation": "serde + validator",
        "env_tool": "config-rs / dotenvy",
        "layers": "Models → Config → Repository → Service → Handler → Router",
        "dir_structure": """src/
├── main.rs
├── config.rs           # 配置
├── models/             # 数据结构
├── repository/         # 数据访问
├── service/            # 业务逻辑
├── handler/            # HTTP 处理
├── router.rs           # 路由
├── error.rs            # 错误类型
└── tests/""",
        "lint_config": """# clippy.toml
cognitive-complexity-threshold = 10

# Cargo.toml
[lints.clippy]
unwrap_used = "deny"
expect_used = "warn"
missing_docs = "warn" """,
        "commands": {
            "dev": "cargo watch -x run",
            "lint": "cargo clippy -- -D warnings",
            "test": "cargo test",
            "check": "cargo clippy -- -D warnings && cargo test"
        },
        "bad_example": ".unwrap() 到处用，忽略错误处理",
        "good_example": "用 ? 运算符 + 自定义 Error 类型 + thiserror",
        "validation_example": """// ❌
let data: serde_json::Value = serde_json::from_slice(&body)?;
let email = data["email"].as_str().unwrap();

// ✅
#[derive(Deserialize, Validate)]
struct CreateUser {
    #[validate(email)] email: String,
    #[validate(length(min = 1))] name: String,
}
let req: CreateUser = serde_json::from_slice(&body)?;
req.validate()?;""",
    },

    "swift-ios": {
        "name": "Swift + SwiftUI",
        "category": "mobile",
        "label": "iOS / macOS 客户端",
        "lang": "Swift",
        "framework": "SwiftUI + Combine / Swift Concurrency",
        "package_manager": "Swift Package Manager",
        "linter": "SwiftLint",
        "type_checker": "Swift 编译器（静态类型）",
        "test_runner": "XCTest",
        "formatter": "swift-format",
        "validation": "自定义 Validator 或 ValidatedPropertyKit",
        "env_tool": "xcconfig / .plist",
        "layers": "Models → Repositories → Services → ViewModels → Views",
        "dir_structure": """App/
├── Models/             # 数据模型
├── Repositories/       # 网络/本地数据
├── Services/           # 业务逻辑
├── ViewModels/         # MVVM ViewModel
├── Views/              # SwiftUI View
├── Config/             # 环境配置
├── Utilities/          # 工具扩展
└── Tests/""",
        "lint_config": """# .swiftlint.yml
opt_in_rules:
  - force_unwrapping
  - implicitly_unwrapped_optional
  - missing_docs
disabled_rules: []
line_length: 120
function_body_length: 50""",
        "commands": {
            "dev": "xcodebuild (或 Xcode 运行)",
            "lint": "swiftlint lint --strict",
            "test": "xcodebuild test -scheme App",
            "check": "swiftlint lint --strict && xcodebuild test -scheme App"
        },
        "bad_example": "let name = data!.name  // force unwrap",
        "good_example": "guard let name = data?.name else { return }",
        "validation_example": """// ❌ View 里直接调网络
struct UserView: View {
    var body: some View {
        Button("Load") { URLSession.shared.dataTask(...) }
    }
}

// ✅ MVVM：View → ViewModel → Repository
struct UserView: View {
    @StateObject var vm = UserViewModel()
    var body: some View {
        Button("Load") { Task { await vm.loadUser() } }
    }
}""",
    },

    "kotlin-android": {
        "name": "Kotlin + Android",
        "category": "mobile",
        "label": "Android 客户端",
        "lang": "Kotlin",
        "framework": "Jetpack Compose + Hilt + Coroutines",
        "package_manager": "Gradle",
        "linter": "ktlint + detekt",
        "type_checker": "Kotlin 编译器（静态类型）",
        "test_runner": "JUnit 5 + Turbine",
        "formatter": "ktlint format",
        "validation": "Kotlin data class + sealed class",
        "env_tool": "BuildConfig / local.properties",
        "layers": "Data (Models) → Repository → UseCase → ViewModel → UI",
        "dir_structure": """app/src/main/java/com/example/app/
├── data/
│   ├── model/          # 数据模型
│   ├── remote/         # API 接口
│   └── repository/     # Repository 实现
├── domain/
│   ├── model/          # 领域模型
│   ├── repository/     # Repository 接口
│   └── usecase/        # 用例
├── presentation/
│   ├── ui/             # Composable 组件
│   └── viewmodel/      # ViewModel
├── di/                 # Hilt 依赖注入
└── util/""",
        "lint_config": """# detekt.yml
complexity:
  ComplexMethod:
    threshold: 10
  LongMethod:
    threshold: 50
style:
  ForbiddenComment:
    active: true""",
        "commands": {
            "dev": "./gradlew installDebug",
            "lint": "./gradlew ktlintCheck detekt",
            "test": "./gradlew test",
            "check": "./gradlew check"
        },
        "bad_example": "Activity 里写 500 行 UI + 网络 + 数据库",
        "good_example": "Clean Architecture: UI → ViewModel → UseCase → Repository",
        "validation_example": """// ❌
fun createUser(data: Map<String, Any>) { ... }

// ✅
data class CreateUserRequest(
    val email: String,
    val name: String
) {
    init {
        require(email.contains("@")) { "Invalid email" }
        require(name.isNotBlank()) { "Name required" }
    }
}""",
    },

    "dart-flutter": {
        "name": "Dart + Flutter",
        "category": "mobile-crossplatform",
        "label": "跨平台客户端（iOS + Android + Web）",
        "lang": "Dart",
        "framework": "Flutter + Riverpod / Bloc",
        "package_manager": "pub",
        "linter": "dart analyze + custom_lint",
        "type_checker": "Dart 编译器（静态类型）",
        "test_runner": "flutter test",
        "formatter": "dart format",
        "validation": "freezed + json_serializable",
        "env_tool": "flutter_dotenv",
        "layers": "Models → Data Sources → Repositories → Providers/Blocs → UI",
        "dir_structure": """lib/
├── models/             # 数据模型（freezed）
├── data/
│   ├── remote/         # API 客户端
│   └── local/          # 本地存储
├── repositories/       # 数据聚合
├── providers/          # 状态管理（Riverpod）
├── ui/
│   ├── screens/        # 页面
│   ├── widgets/        # 共享组件
│   └── theme/          # 主题
└── utils/""",
        "lint_config": """# analysis_options.yaml
analyzer:
  strong-mode:
    implicit-casts: false
    implicit-dynamic: false
  errors:
    missing_return: error
    dead_code: warning
linter:
  rules:
    - prefer_final_locals
    - avoid_dynamic_calls
    - always_declare_return_types""",
        "commands": {
            "dev": "flutter run",
            "lint": "dart analyze && dart format --set-exit-if-changed .",
            "test": "flutter test",
            "check": "dart analyze && flutter test"
        },
        "bad_example": "dynamic data = jsonDecode(response.body);",
        "good_example": "final user = User.fromJson(jsonDecode(response.body) as Map<String, dynamic>);",
        "validation_example": """// ❌
Widget build(context) {
  final resp = await http.get(url); // 在 build 里请求网络！
}

// ✅
// Repository → Provider → UI
final userProvider = FutureProvider((ref) =>
  ref.read(userRepoProvider).getUser());
Widget build(context, ref) {
  final userAsync = ref.watch(userProvider);
}""",
    },

    "react-native": {
        "name": "React Native (TypeScript)",
        "category": "mobile-crossplatform",
        "label": "跨平台客户端（JS 生态）",
        "lang": "TypeScript",
        "framework": "React Native + Expo",
        "package_manager": "npm / yarn",
        "linter": "ESLint + @typescript-eslint",
        "type_checker": "TypeScript strict",
        "test_runner": "Jest + React Native Testing Library",
        "formatter": "Prettier",
        "validation": "zod",
        "env_tool": "expo-constants + zod",
        "layers": "Types → Config → Services/API → Hooks → Screens → Components",
        "dir_structure": """src/
├── types/              # 类型定义
├── config/             # 环境变量
├── services/           # API 客户端 + 业务逻辑
├── hooks/              # 自定义 Hooks
├── screens/            # 页面组件
├── components/         # 共享 UI 组件
├── navigation/         # 导航配置
├── stores/             # 状态管理（Zustand）
└── utils/""",
        "lint_config": """{
  "extends": ["@react-native", "plugin:@typescript-eslint/recommended"],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "react-hooks/exhaustive-deps": "error"
  }
}""",
        "commands": {
            "dev": "npx expo start",
            "lint": "eslint src/ && tsc --noEmit",
            "test": "jest",
            "check": "eslint src/ && tsc --noEmit && jest"
        },
        "bad_example": 'const data: any = await fetch(url).then(r => r.json())',
        "good_example": 'const data = UserSchema.parse(await apiClient.getUser(id))',
        "validation_example": """// ❌ Screen 里直接 fetch
function ProfileScreen() {
  useEffect(() => { fetch('/api/user').then(...) }, [])
}

// ✅ Hook 封装
function useUser(id: string) {
  return useQuery({ queryKey: ['user', id], queryFn: () => userService.get(id) })
}
function ProfileScreen() {
  const { data: user } = useUser(userId)
}""",
    },
}

# Common stack combos
COMBOS = {
    "nextjs-python-api": {
        "name": "Next.js 前端 + Python FastAPI 后端",
        "frontend": "ts-nextjs",
        "backend": "python-fastapi",
        "description": "最流行的 AI 应用全栈组合。Next.js 负责 UI，FastAPI 负责 AI/ML 服务。",
    },
    "react-go-api": {
        "name": "React SPA + Go 后端",
        "frontend": "ts-nextjs",
        "backend": "go",
        "description": "高性能微服务组合。React 前端 + Go 后端，适合高并发场景。",
    },
    "flutter-fastapi": {
        "name": "Flutter 客户端 + FastAPI 后端",
        "frontend": "dart-flutter",
        "backend": "python-fastapi",
        "description": "跨平台移动应用 + Python 后端，快速迭代。",
    },
    "nextjs-spring": {
        "name": "Next.js 前端 + Spring Boot 后端",
        "frontend": "ts-nextjs",
        "backend": "java-spring",
        "description": "企业级全栈组合。Next.js 现代前端 + Spring Boot 稳定后端。",
    },
    "rn-node": {
        "name": "React Native 客户端 + Node.js API",
        "frontend": "react-native",
        "backend": "ts-node",
        "description": "纯 TypeScript 全栈移动应用。前后端共享类型定义。",
    },
}

# ============================================================
# GENERATORS
# ============================================================

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✅ {path.relative_to(BASE)}")


def gen_claude_md(stack: dict) -> str:
    return f"""# CLAUDE.md — Claude 工作指南（{stack['name']}）

> 本文件专为 Claude / Claude Code / Cowork 设计。
> 若项目中同时提供 `AGENTS.md`，可先读它获取跨工具共识；否则本文件可独立使用。

---

## 项目基本信息

```
项目名称: [PROJECT_NAME]
描述:     [ONE_LINE_DESCRIPTION]
技术栈:   {stack['name']}
负责人:   [OWNER]
```

## 快速导航

| 我想了解...         | 文件位置                        |
|--------------------|-------------------------------|
| 整体架构与层级      | `docs/architecture.md`        |
| 代码黄金原则        | `docs/golden-principles.md`   |
| 业务领域模型        | `docs/domain-model.md`        |
| 如何开始工作        | `docs/onboarding.md`          |
| 技术选型决策        | `docs/tech-decisions/`        |
| 功能需求追踪        | `feature_list.json`           |
| 跨 session 进度    | `{PROGRESS_FILE}`             |

## Claude 工作方式

### Session 启动仪式
1. 运行 `bash scripts/init.sh` 验证环境
2. 读 `{PROGRESS_FILE}` 了解上次进度
3. 读 `feature_list.json` 确认当前任务
4. 读本文件 + `docs/` 相关文档

### 任务执行
1. **先说你的理解和计划**，再写代码
2. 遇到不确定的概念 → 查 `docs/domain-model.md`，查不到就问我

### 代码生产
- 写**最小可运行**的变更，不顺手"优化"无关代码
- 按层级顺序实现：{stack['layers']}
- 每完成一个子任务，汇报进度再继续

### 上下文管理
- 先读架构文档，再读具体代码（不要一次读所有文件）
- 上下文不够时，告诉我优先需要哪些文件

### 完成标准
- [ ] `{stack['commands']['check']}` 全部通过
- [ ] `bash scripts/layer-check.sh` 无违规
- [ ] 新增模块已更新 `docs/domain-model.md`
- [ ] `feature_list.json` 状态已更新
- [ ] `{PROGRESS_FILE}` 已追加本次记录
- [ ] PR 描述写清楚了"为什么这样做"

## 不要做的事

```
❌ 不要修改与任务无关的文件
❌ 不要使用 {stack['bad_example'].split(chr(10))[0][:50]}
❌ 不要安装新依赖（先告知我，等确认）
❌ 不要删除注释或测试（除非明确要求）
```

## 定期维护

- 对我说"代码审计" → 按 `scripts/audit-prompt.md` 执行
- 对我说"更新文档" → 按 `scripts/doc-gardening-prompt.md` 执行
"""


def gen_agents_md(stack: dict) -> str:
    return f"""# AGENTS.md — AI Agent 项目指令（{stack['name']}）

> 本文件是所有 AI 编程工具（Codex、Cursor、Windsurf 等）的入口文件。
> 在开始任何任务前必须先读此文件。详细规则跟随链接查看。

---

## 项目信息

```
项目名称: [PROJECT_NAME]
描述:     [ONE_LINE_DESCRIPTION]
技术栈:   {stack['name']}
负责人:   [OWNER]
```

## 文档导航

| 文档                | 路径                              |
|--------------------|----------------------------------|
| 架构与依赖层级      | `docs/architecture.md`           |
| 代码黄金原则        | `docs/golden-principles.md`      |
| 业务领域模型        | `docs/domain-model.md`           |
| 上手指南           | `docs/onboarding.md`             |
| 技术决策记录        | `docs/tech-decisions/`           |
| 功能需求追踪        | `feature_list.json`              |
| 跨 session 进度    | `{PROGRESS_FILE}`                |

## Session 启动（每次必做）

```bash
bash scripts/init.sh       # 验证环境 + baseline tests
cat {PROGRESS_FILE}         # 了解上次进度
cat feature_list.json       # 确认当前任务
```

## 核心规则（不可违反）

1. **依赖方向单向流动** — `{stack['layers']}`，禁止反向
2. **边界必须验证** — 外部数据用 {stack['validation']} 验证，不猜测结构
3. **不重复** — 复用 utils/lib，超过 2 处重复必须提取
4. **类型安全** — 严格使用 {stack['type_checker']}
5. **错误必须处理** — 不允许静默吞掉 error
6. **配置集中** — 用 {stack['env_tool']} 管理环境变量，禁止硬编码

## 技术偏好

- 偏好**稳定且文档丰富**的技术（对 AI 训练集友好）
- 偏好**组合**而非继承
- 偏好**显式**而非隐式

## 任务完成标准

```bash
# 提交前必须通过
{stack['commands']['check']}
bash scripts/layer-check.sh  # 依赖层级检查
```

完成后更新：
- `feature_list.json` — 更新 status 和 files_touched
- `{PROGRESS_FILE}` — 追加 session 记录

## 禁止模式

```
❌ {stack['bad_example'].split(chr(10))[0]}
❌ 在 UI/Handler 层直接操作数据库
❌ 硬编码 API keys、URL、端口
❌ 空的错误处理块
❌ 超过 2 处的重复逻辑
```
"""


def gen_architecture(stack: dict) -> str:
    return f"""# 架构文档 — {stack['name']}

## 核心原则

**依赖只能向下流动，禁止反向或跨层调用。**

## 依赖层级

```
{stack['layers']}
```

## 目录结构

```
{stack['dir_structure']}
```

## 各层职责

| 层级 | 职责 | 禁止 |
|------|------|------|
| 最底层（Types/Models） | 类型定义、数据结构 | 任何逻辑代码 |
| Config/Utils | 纯函数工具、配置读取 | 调用数据库或外部 API |
| Repository/Data | 数据库查询、缓存操作 | 业务逻辑判断 |
| Service/UseCase | 业务逻辑、跨 Repo 协调 | 处理 HTTP 请求/响应 |
| Controller/Handler/View | 请求解析、调用 Service、返回响应 | 直接数据库调用 |
| UI/Pages（如适用） | 渲染、用户交互 | 直接调用 Service 或 DB |

## 变更记录

| 日期 | 变更 | 原因 |
|------|------|------|
| [DATE] | 初始架构 | 项目创建 |
"""


def gen_golden_principles(stack: dict) -> str:
    return f"""# 黄金原则 — {stack['name']}

> 这些原则是**机械规则**，每条对应一个 lint 或 CI 检查。

## 原则列表

| # | 原则 | 检查方式 |
|---|------|---------|
| G1 | 类型安全 | {stack['type_checker']} |
| G2 | 边界验证：外部数据必须校验 | {stack['validation']} |
| G3 | 不重复（DRY）：>2 处重复必须提取 | 代码审计 |
| G4 | 错误必须处理：不允许静默吞掉 | {stack['linter']} |
| G5 | 禁止硬编码配置 | {stack['env_tool']} |
| G6 | 函数单一职责：上限 50 行 | {stack['linter']} |
| G7 | 关键路径必须有测试 | {stack['test_runner']} |
| G8 | 依赖层级不可违反 | 结构测试 |

---

## G1 — 类型安全

```
❌ 禁止：{stack['bad_example']}

✅ 正确：{stack['good_example']}
```

## G2 — 数据边界验证

```
{stack['validation_example']}
```

## G4 — 错误处理

所有错误必须被处理：要么向上抛出，要么记录日志。不允许空的 catch/except 块。

## G5 — 禁止硬编码

所有配置值（API keys、URL、端口等）必须通过 {stack['env_tool']} 管理。

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
"""


def gen_onboarding(stack: dict) -> str:
    return f"""# 上手指南 — {stack['name']}

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
{stack['package_manager']} install  # 根据项目实际调整

# 启动开发
{stack['commands']['dev']}
```

## 第三步：开发工作流

```
1. 读 docs/domain-model.md → 确认涉及哪些实体
2. 读 docs/architecture.md → 确认在哪个层实现
3. 写代码（按层级顺序）
4. 运行检查：{stack['commands']['check']}
5. 提交 PR
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `{stack['commands']['dev']}` | 启动开发 |
| `{stack['commands']['lint']}` | 代码检查 |
| `{stack['commands']['test']}` | 运行测试 |
| `{stack['commands']['check']}` | 完整检查（提交前跑） |

## 定期维护

| 频率 | 任务 |
|------|------|
| 每周 | 代码审计（`scripts/audit-prompt.md`）|
| 每周 | 文档更新（`scripts/doc-gardening-prompt.md`）|
"""


def gen_lint_config(stack: dict) -> str:
    return stack["lint_config"]


def gen_layer_check(stack: dict) -> str:
    """Generate a structural test script that enforces dependency layering."""
    layers = [l.strip() for l in stack["layers"].split("→")]
    lang = stack["lang"]
    aliases = _layer_check_aliases(stack)
    ext = _layer_check_extension(lang)
    comment = "#"  # Always bash comments in shell scripts

    if len(aliases) != len(layers):
        raise ValueError(
            f"Layer alias count mismatch for {stack['name']}: "
            f"{len(aliases)} aliases for {len(layers)} layers"
        )

    rules: list[dict[str, object]] = []
    for i, layer in enumerate(layers):
        forbidden = [token for group in aliases[i + 1:] for token in group]
        if forbidden:
            rules.append(
                {
                    "layer": layer,
                    "source_aliases": aliases[i],
                    "forbidden": forbidden,
                }
            )

    analyzer = _layer_check_embedded_python(lang, ext, rules)

    return f"""#!/usr/bin/env bash
{comment} layer-check.sh — Structural dependency test for {stack['name']}
{comment}
{comment} Enforces: {stack['layers']}
{comment} Lower layers MUST NOT depend on higher layers.
{comment} This script performs language-aware dependency extraction where possible.
{comment}
{comment} Usage: bash scripts/layer-check.sh [src_dir]
{comment}
{comment} Exit code 0 = pass, 1 = violations found, 2 = runtime error

set -euo pipefail

SRC_DIR="${{1:-.}}"
RED='\\033[0;31m'
NC='\\033[0m'

PYTHON_BIN="$(command -v python3 || command -v python || true)"
if [[ -z "$PYTHON_BIN" ]]; then
  echo -e "${{RED}}python3 or python is required for language-aware layer checks.${{NC}}"
  exit 2
fi

"$PYTHON_BIN" - "$SRC_DIR" <<'PY'
{analyzer}
PY
"""


def _layer_check_extension(lang: str) -> str:
    if lang == "TypeScript":
        return "ts"
    if lang == "Dart":
        return "dart"
    if lang == "Python":
        return "py"
    if lang == "Go":
        return "go"
    if lang == "Rust":
        return "rs"
    if lang == "Java":
        return "java"
    if lang == "C#":
        return "cs"
    if lang == "Kotlin":
        return "kt"
    if lang == "Swift":
        return "swift"
    return "*"


def _layer_check_embedded_python(lang: str, ext: str, rules: list[dict[str, object]]) -> str:
    rules_json = json.dumps(rules, ensure_ascii=False)
    return textwrap.dedent(
        f"""\
        import ast
        import json
        import pathlib
        import re
        import sys

        SRC_DIR = pathlib.Path(sys.argv[1]).resolve()
        LANG = {lang!r}
        EXT = {ext!r}
        RULES = json.loads({rules_json!r})

        RED = "\\033[0;31m"
        GREEN = "\\033[0;32m"
        NC = "\\033[0m"
        FALLBACK_SCAN_LANGS = ("Swift",)


        def iter_source_files(source_aliases):
            seen = set()
            results = []
            for alias in source_aliases:
                alias_parts = tuple(part for part in alias.split("/") if part)
                if not alias_parts:
                    continue
                for directory in SRC_DIR.rglob(alias_parts[-1]):
                    if not directory.is_dir():
                        continue
                    try:
                        rel_parts = directory.relative_to(SRC_DIR).parts
                    except ValueError:
                        continue
                    if len(rel_parts) < len(alias_parts):
                        continue
                    if rel_parts[-len(alias_parts):] != alias_parts:
                        continue
                    for path in directory.rglob("*." + EXT):
                        if not path.is_file():
                            continue
                        key = str(path.resolve())
                        if key in seen:
                            continue
                        seen.add(key)
                        results.append(path)
            return sorted(results)


        def strip_c_like_comments(text):
            text = re.sub(r"/\\*.*?\\*/", "", text, flags=re.S)
            return re.sub(r"//.*", "", text)


        def strip_hash_comments(text):
            return re.sub(r"#.*", "", text)


        def strip_strings(text):
            return re.sub(r'("([^"\\\\]|\\\\.)*"|\\'([^\\'\\\\]|\\\\.)*\\')', '""', text)


        def extract_python_targets(text):
            tree = ast.parse(text)
            targets = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    targets.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    targets.append(("." * node.level) + node.module)
            return targets


        def extract_typescript_targets(text):
            clean = strip_c_like_comments(text)
            patterns = [
                r'(?m)^\\s*import\\s+(?:type\\s+)?(?:[^"\\']+\\s+from\\s+)?["\\']([^"\\']+)["\\']',
                r'(?m)^\\s*export\\s+[^"\\']+\\s+from\\s+["\\']([^"\\']+)["\\']',
                r'(?m)(?:^|[=\\s(])require\\(\\s*["\\']([^"\\']+)["\\']\\s*\\)',
                r'(?m)\\bimport\\(\\s*["\\']([^"\\']+)["\\']\\s*\\)',
            ]
            targets = []
            for pattern in patterns:
                targets.extend(re.findall(pattern, clean))
            return targets


        def extract_dart_targets(text):
            clean = strip_c_like_comments(text)
            patterns = [
                r'(?m)^\\s*import\\s+["\\']([^"\\']+)["\\']',
                r'(?m)^\\s*export\\s+["\\']([^"\\']+)["\\']',
                r'(?m)^\\s*part(?:\\s+of)?\\s+["\\']([^"\\']+)["\\']',
            ]
            targets = []
            for pattern in patterns:
                targets.extend(re.findall(pattern, clean))
            return targets


        def extract_go_targets(text):
            clean = strip_c_like_comments(text)
            targets = []
            in_block = False
            for raw_line in clean.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                if line.startswith("import ("):
                    in_block = True
                    continue
                if in_block:
                    if line.startswith(")"):
                        in_block = False
                        continue
                    match = re.match(r'(?:[A-Za-z_][A-Za-z0-9_]*\\s+)?\\"([^\\"]+)\\"', line)
                    if match:
                        targets.append(match.group(1))
                    continue
                match = re.match(r'import\\s+(?:[A-Za-z_][A-Za-z0-9_]*\\s+)?\\"([^\\"]+)\\"', line)
                if match:
                    targets.append(match.group(1))
            return targets


        def extract_rust_targets(text):
            clean = strip_c_like_comments(text)
            return re.findall(r'(?m)^\\s*use\\s+([^;]+);', clean)


        def extract_java_like_targets(text):
            clean = strip_c_like_comments(text)
            return re.findall(r'(?m)^\\s*import\\s+([^\\s;]+)', clean)


        def extract_csharp_targets(text):
            clean = strip_c_like_comments(text)
            return re.findall(r'(?m)^\\s*using\\s+([^\\s;=]+)\\s*;', clean)


        def extract_swift_targets(text):
            clean = strip_c_like_comments(text)
            return re.findall(r'(?m)^\\s*import\\s+([^\\s]+)', clean)


        EXTRACTORS = {{
            "Python": extract_python_targets,
            "TypeScript": extract_typescript_targets,
            "Dart": extract_dart_targets,
            "Go": extract_go_targets,
            "Rust": extract_rust_targets,
            "Java": extract_java_like_targets,
            "Kotlin": extract_java_like_targets,
            "C#": extract_csharp_targets,
            "Swift": extract_swift_targets,
        }}


        def normalize_target(target):
            normalized = target.replace("\\\\", "/")
            normalized = normalized.replace("::", "/")
            normalized = normalized.replace(".", "/")
            normalized = re.sub(r"^(package:|crate/|self/|super/|global/)", "", normalized)
            normalized = re.sub(r"^[@~]/", "", normalized)
            normalized = normalized.lstrip("./")
            normalized = re.sub(r"^src/", "", normalized)
            parts = [
                part.lower()
                for part in normalized.split("/")
                if part and part.lower() not in {{"src", "crate", "self", "super", "global"}}
            ]
            return "/".join(parts)


        def target_matches(target, forbidden):
            normalized_target = normalize_target(target)
            normalized_forbidden = normalize_target(forbidden)
            if not normalized_target or not normalized_forbidden:
                return False
            if normalized_target == normalized_forbidden:
                return True

            target_parts = [part for part in normalized_target.split("/") if part]
            if len(target_parts) <= 1:
                return False

            directory_blob = "/" + "/".join(target_parts[:-1]) + "/"
            needle = "/" + normalized_forbidden + "/"
            return needle in directory_blob


        def extract_dependency_view(path):
            text = path.read_text(encoding="utf-8", errors="ignore")
            extractor = EXTRACTORS.get(LANG)
            try:
                targets = extractor(text) if extractor else []
            except SyntaxError as exc:
                return None, None, "parse error: %s" % exc

            fallback_blob = None
            if LANG in FALLBACK_SCAN_LANGS:
                fallback_blob = normalize_target(strip_strings(strip_c_like_comments(text)))
            return targets, fallback_blob, None


        def print_violation(message, detail):
            print("%sVIOLATION%s: %s" % (RED, NC, message))
            print(detail)


        violations = 0
        for rule in RULES:
            files = iter_source_files(rule["source_aliases"])
            if not files:
                continue
            for path in files:
                relative = path.relative_to(SRC_DIR)
                targets, fallback_blob, error = extract_dependency_view(path)
                if error is not None:
                    print_violation(
                        "%s could not be parsed" % relative,
                        "  -> %s" % error,
                    )
                    violations += 1
                    continue

                for forbidden in rule["forbidden"]:
                    matched_target = None
                    for target in targets:
                        if target_matches(target, forbidden):
                            matched_target = target
                            break
                    if matched_target is not None:
                        print_violation(
                            "'%s' imports higher-layer dependency '%s'" % (rule["layer"], forbidden),
                            "  -> %s via %s" % (relative, matched_target),
                        )
                        violations += 1
                        continue

                    if fallback_blob and target_matches(fallback_blob, forbidden):
                        print_violation(
                            "'%s' references higher-layer dependency '%s' (fallback scan)" % (
                                rule["layer"],
                                forbidden,
                            ),
                            "  -> %s" % relative,
                        )
                        violations += 1

        if violations == 0:
            print("%s✅ Layer check passed — no dependency violations found.%s" % (GREEN, NC))
            sys.exit(0)

        print("\\n%s❌ Found %s layer violation(s). Fix before committing.%s" % (RED, violations, NC))
        sys.exit(1)
        """
    ).rstrip()


def gen_init_sh(stack: dict) -> str:
    """Generate init.sh — environment verification + dev server + baseline tests."""
    return f"""#!/usr/bin/env bash
# init.sh — Environment setup & baseline verification for {stack['name']}
#
# Run this at the start of every AI agent session to ensure:
# 1. Dependencies are installed
# 2. Dev server starts successfully
# 3. Baseline tests pass
#
# Usage: bash scripts/init.sh

set -euo pipefail

RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

echo "🔧 [{stack['name']}] Initializing environment..."

# Step 1: Check required tools
echo -e "\\n${{YELLOW}}[1/4] Checking tools...${{NC}}"
MISSING=0
for cmd in {_required_tools(stack)}; do
  if ! command -v "$cmd" &>/dev/null; then
    echo -e "${{RED}}  ✗ $cmd not found${{NC}}"
    MISSING=1
  else
    echo "  ✓ $cmd $(command -v "$cmd")"
  fi
done
[[ $MISSING -eq 1 ]] && echo -e "${{RED}}Install missing tools before continuing.${{NC}}" && exit 1

# Step 2: Install dependencies
echo -e "\\n${{YELLOW}}[2/4] Installing dependencies...${{NC}}"
{_install_cmd(stack)}

# Step 3: Run baseline checks (lint + typecheck)
echo -e "\\n${{YELLOW}}[3/4] Running lint & type checks...${{NC}}"
{stack['commands']['lint']}

# Step 4: Run tests
echo -e "\\n${{YELLOW}}[4/4] Running tests...${{NC}}"
{stack['commands']['test']}

echo -e "\\n${{GREEN}}✅ Environment verified. All checks passed. Ready to code.${{NC}}"
"""


def _required_tools(stack: dict) -> str:
    """Return space-separated tool names to check in init.sh."""
    lang = stack["lang"]
    tools = {
        "TypeScript": "node npm npx",
        "Python": "python3 pip",
        "Go": "go",
        "Rust": "cargo rustc",
        "Java": "java mvn",
        "C#": "dotnet",
        "Kotlin": "java",
        "Swift": "swift xcodebuild",
        "Dart": "dart flutter",
    }
    return tools.get(lang, "echo")


def _install_cmd(stack: dict) -> str:
    """Return the install command for init.sh."""
    pm = stack["package_manager"].split("/")[0].strip()
    lang = stack["lang"]
    cmds = {
        "npm": "npm install",
        "pip": "pip install -r requirements.txt 2>/dev/null || pip install -e '.[dev]' 2>/dev/null || echo 'No requirements found, skipping'",
        "go mod": "go mod download",
        "Cargo": "cargo build",
        "Maven": "./mvnw compile -q || mvn compile -q",
        "NuGet": "dotnet restore",
        "Gradle": "./gradlew build -x test || gradle build -x test",
        "Swift Package Manager": "swift package resolve",
        "pub": "flutter pub get",
    }
    return cmds.get(pm, f"echo 'Install dependencies with {pm}'")


def gen_feature_list_json() -> str:
    """Generate feature_list.json template for cross-session progress tracking."""
    return json.dumps({
        "_comment": "Feature tracking for AI agents. JSON format prevents accidental overwrites. Update status as you implement.",
        "project": "[PROJECT_NAME]",
        "last_updated": "[DATE]",
        "features": [
            {
                "id": "F-001",
                "name": "Example: User registration",
                "description": "Users can sign up with email and password",
                "status": "not_started",
                "acceptance_criteria": [
                    "POST /api/register accepts email + password",
                    "Passwords are hashed with bcrypt",
                    "Duplicate email returns 409",
                    "Success returns JWT token"
                ],
                "files_touched": [],
                "notes": ""
            },
            {
                "id": "F-002",
                "name": "[YOUR FEATURE]",
                "description": "[WHAT IT DOES]",
                "status": "not_started",
                "acceptance_criteria": [],
                "files_touched": [],
                "notes": ""
            }
        ],
        "status_values": ["not_started", "in_progress", "blocked", "testing", "done"]
    }, ensure_ascii=False, indent=2)


def gen_claude_progress() -> str:
    """Generate agent-progress.txt template for cross-session handoffs."""
    return """# Agent Progress Log
#
# Purpose: Track work across multiple AI agent sessions.
# Each session MUST append an entry before ending.
# Next session MUST read this file before starting work.
#
# Format:
# === Session [N] — [DATE] ===
# Goal: What was attempted
# Done: What was completed
# Decisions: Key choices made and why
# Blocked: What couldn't be finished (and why)
# Next: What the next session should do first
# Files changed: List of modified files
# Tests: pass/fail status
# ================================

=== Session 1 — [DATE] ===
Goal: [Initial setup / Feature X / Bug fix Y]
Done:
  - [What was completed]
Decisions:
  - [Choice made] — because [reason]
Blocked:
  - [Issue] — needs [resolution]
Next:
  - [ ] [First thing next session should do]
  - [ ] [Second thing]
Files changed:
  - [file1.py] (new)
  - [file2.py] (modified)
Tests: all passing / N failures
================================
"""


def gen_github_ci(stack: dict) -> str:
    """Generate GitHub Actions CI workflow for the stack."""
    lang = stack["lang"]
    check_cmd = stack["commands"]["check"]

    if lang == "TypeScript":
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: Lint & Typecheck
        run: {stack['commands']['lint']}
      - name: Test
        run: {stack['commands']['test']}
      - name: Layer check
        run: bash scripts/layer-check.sh src/
"""
    elif lang == "Python":
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install -e '.[dev]' || pip install -r requirements.txt
      - name: Lint & Typecheck
        run: {stack['commands']['lint']}
      - name: Test
        run: {stack['commands']['test']}
      - name: Layer check
        run: bash scripts/layer-check.sh src/
"""
    elif lang == "Go":
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - name: Lint
        uses: golangci/golangci-lint-action@v4
      - name: Test
        run: {stack['commands']['test']}
      - name: Layer check
        run: bash scripts/layer-check.sh .
"""
    elif lang == "Rust":
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      - name: Lint
        run: {stack['commands']['lint']}
      - name: Test
        run: {stack['commands']['test']}
      - name: Format check
        run: cargo fmt --check
"""
    elif lang == "Java":
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
          cache: 'maven'
      - name: Build & Test
        run: {check_cmd}
"""
    elif lang == "C#":
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'
      - name: Build & Test
        run: {check_cmd}
"""
    elif lang == "Kotlin":
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
          cache: 'gradle'
      - name: Check
        run: {check_cmd}
"""
    elif lang == "Swift":
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: {stack['commands']['lint']}
      - name: Test
        run: {stack['commands']['test']}
"""
    elif lang == "Dart":
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.x'
      - run: flutter pub get
      - name: Analyze
        run: {stack['commands']['lint']}
      - name: Test
        run: {stack['commands']['test']}
"""
    else:
        return f"""# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Full check
        run: {check_cmd}
"""


def gen_pre_commit_config(stack: dict) -> str:
    """Generate .pre-commit-config.yaml for the stack."""
    lang = stack["lang"]

    if lang == "TypeScript":
        return """# .pre-commit-config.yaml
# Install: pip install pre-commit && pre-commit install
repos:
  - repo: local
    hooks:
      - id: lint
        name: ESLint + TypeCheck
        entry: bash -c 'npx eslint src/ && npx tsc --noEmit'
        language: system
        types: [ts, tsx]
        pass_filenames: false
      - id: layer-check
        name: Dependency layer check
        entry: bash scripts/layer-check.sh src/
        language: system
        pass_filenames: false
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-json
      - id: check-yaml
"""
    elif lang == "Python":
        return """# .pre-commit-config.yaml
# Install: pip install pre-commit && pre-commit install
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: local
    hooks:
      - id: mypy
        name: mypy type check
        entry: mypy src/
        language: system
        types: [python]
        pass_filenames: false
      - id: layer-check
        name: Dependency layer check
        entry: bash scripts/layer-check.sh src/
        language: system
        pass_filenames: false
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-json
      - id: check-yaml
"""
    elif lang == "Go":
        return """# .pre-commit-config.yaml
# Install: pip install pre-commit && pre-commit install
repos:
  - repo: https://github.com/golangci/golangci-lint
    rev: v1.59.0
    hooks:
      - id: golangci-lint
  - repo: local
    hooks:
      - id: go-test
        name: Go tests
        entry: go test ./... -race -short
        language: system
        types: [go]
        pass_filenames: false
      - id: layer-check
        name: Dependency layer check
        entry: bash scripts/layer-check.sh .
        language: system
        pass_filenames: false
"""
    elif lang == "Rust":
        return """# .pre-commit-config.yaml
# Install: pip install pre-commit && pre-commit install
repos:
  - repo: local
    hooks:
      - id: cargo-clippy
        name: Clippy
        entry: cargo clippy -- -D warnings
        language: system
        types: [rust]
        pass_filenames: false
      - id: cargo-fmt
        name: Rustfmt
        entry: cargo fmt --check
        language: system
        types: [rust]
        pass_filenames: false
      - id: cargo-test
        name: Tests
        entry: cargo test
        language: system
        types: [rust]
        pass_filenames: false
"""
    else:
        return f"""# .pre-commit-config.yaml
# Install: pip install pre-commit && pre-commit install
repos:
  - repo: local
    hooks:
      - id: check
        name: Full check ({stack['name']})
        entry: bash -c '{stack["commands"]["check"]}'
        language: system
        pass_filenames: false
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
"""


def gen_readme(stack_id: str, stack: dict) -> str:
    return f"""# {stack['name']} — Harness Engineering 模版

**分类**：{stack['label']}
**语言**：{stack['lang']}
**框架**：{stack['framework']}

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
| {stack['linter']} | 代码检查 |
| {stack['type_checker']} | 类型检查 |
| {stack['test_runner']} | 测试 |
| {stack['formatter']} | 格式化 |
| {stack['validation']} | 数据验证 |
"""


def gen_combo_readme(combo_id: str, combo: dict) -> str:
    return f"""# {combo['name']} — 组合模版

{combo['description']}

## 组成

| 部分 | 模版 |
|------|------|
| 前端/客户端 | `stacks/{combo['frontend']}/` |
| 后端 | `stacks/{combo['backend']}/` |

## 使用方法

1. 分别从对应模版复制文件到前后端项目
2. 前后端共用 `common/docs/domain-model.md`（统一业务语言）
3. 在根目录创建一个 monorepo 级别的 `AGENTS.md` 或 `CLAUDE.md`，指向两边

## Monorepo 结构建议

```
project/
├── AGENTS.md (or CLAUDE.md)  ← 全局索引
├── docs/                      ← 共享业务文档
│   ├── domain-model.md
│   └── architecture.md
├── frontend/                  ← {combo['frontend']}
│   └── AGENTS.md (or CLAUDE.md)
└── backend/                   ← {combo['backend']}
    └── AGENTS.md (or CLAUDE.md)
```
"""


def gen_root_readme() -> str:
    stack_table = ""
    for sid, s in STACKS.items():
        stack_table += f"| [{s['name']}](stacks/{sid}/) | {s['label']} | {s['lang']} | {s['framework']} |\n"

    combo_table = ""
    for cid, c in COMBOS.items():
        combo_table += f"| [{c['name']}](combos/{cid}/) | `{c['frontend']}` + `{c['backend']}` |\n"

    return f"""# Harness Engineering Templates

> 基于 [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) 思想，
> 为 **13 种主流技术栈** 提供标准化的 AI-first 项目模版。
> 每个技术栈同时支持 **Claude（CLAUDE.md）** 和 **Codex（AGENTS.md）** 双版本。

---

## 支持的技术栈

| 技术栈 | 分类 | 语言 | 框架 |
|--------|------|------|------|
{stack_table}

## 常用组合

| 组合 | 组成 |
|------|------|
{combo_table}

## 仓库结构

```
harness/
├── common/              # 所有项目通用的文档和脚本
│   ├── docs/            # 领域模型、ADR 模版
│   ├── scripts/         # AI 审计/维护 prompt
│   ├── feature_list.json    # 功能追踪模版（JSON 防误改）
│   └── {PROGRESS_FILE}      # 跨 session 进度日志模版
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

### 方式 1：手动复制

```bash
# 1. 克隆仓库
git clone https://github.com/ppop123/harness.git

# 2. 选择你的技术栈（例如 ts-nextjs）
cp stacks/ts-nextjs/claude/CLAUDE.md your-project/CLAUDE.md
cp stacks/ts-nextjs/codex/AGENTS.md your-project/AGENTS.md
cp -r common/docs your-project/docs
cp -r common/scripts your-project/scripts
cp common/{PROGRESS_FILE} your-project/{PROGRESS_FILE}
```

### 方式 2：通过 Cowork Skill 自动加载

安装 `harness-init.skill` 后，对 Claude 说"初始化项目"，自动从本仓库拉取最新模版。

### 方式 3：curl 快速初始化

```bash
# 替换 ppop123 和 STACK_NAME
REPO="https://raw.githubusercontent.com/ppop123/harness/main"
STACK="ts-nextjs"

# Claude / Claude Code
curl -o CLAUDE.md "$REPO/stacks/$STACK/claude/CLAUDE.md"

# Codex / Cursor / Windsurf
curl -o AGENTS.md "$REPO/stacks/$STACK/codex/AGENTS.md"

mkdir -p docs scripts .github/workflows
curl -o docs/architecture.md "$REPO/stacks/$STACK/docs/architecture.md"
curl -o docs/golden-principles.md "$REPO/stacks/$STACK/docs/golden-principles.md"
curl -o docs/domain-model.md "$REPO/common/docs/domain-model.md"
curl -o scripts/audit-prompt.md "$REPO/common/scripts/audit-prompt.md"
curl -o scripts/layer-check.sh "$REPO/stacks/$STACK/scripts/layer-check.sh"
curl -o scripts/init.sh "$REPO/stacks/$STACK/scripts/init.sh"
curl -o .github/workflows/ci.yml "$REPO/stacks/$STACK/ci/ci.yml"
curl -o .pre-commit-config.yaml "$REPO/stacks/$STACK/config/pre-commit-config.yaml"
curl -o feature_list.json "$REPO/common/feature_list.json"
curl -o {PROGRESS_FILE} "$REPO/common/{PROGRESS_FILE}"
```

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

*Generated on {TODAY}*
"""


def _stack_id_for(stack: dict) -> str:
    for stack_id, candidate in STACKS.items():
        if candidate is stack or candidate["name"] == stack["name"]:
            return stack_id
    raise KeyError(f"Unknown stack config: {stack.get('name', stack)}")


def _layer_check_aliases(stack: dict) -> list[list[str]]:
    stack_id = _stack_id_for(stack)
    aliases = LAYER_CHECK_ALIASES.get(stack_id)
    if aliases is None:
        raise KeyError(f"No layer-check aliases configured for {stack_id}")
    return aliases


# ============================================================
# MAIN
# ============================================================

def main():
    print(f"🚀 Generating Harness Engineering Templates repo at {BASE}\n")

    # --- Common docs ---
    # common/ files are maintained directly (not generated).
    # Only verify they exist; do NOT overwrite.
    common_expected = [
        "common/docs/domain-model.md",
        "common/docs/tech-decisions/000-template.md",
        "common/scripts/audit-prompt.md",
        "common/scripts/doc-gardening-prompt.md",
        "common/scripts/new-feature-prompt.md",
        "common/.env.example",
    ]
    for rel in common_expected:
        p = BASE / rel
        if not p.exists():
            print(f"  ⚠️  Missing common file: {rel}")

    # --- Common generated templates ---
    print("\n📄 Generating common templates...")
    write(BASE / "common" / "feature_list.json", gen_feature_list_json())
    write(BASE / "common" / PROGRESS_FILE, gen_claude_progress())

    # --- Per-stack generation ---
    for stack_id, stack in STACKS.items():
        print(f"\n📦 Generating: {stack['name']}")
        base = BASE / "stacks" / stack_id

        # Claude & Codex versions
        write(base / "claude" / "CLAUDE.md", gen_claude_md(stack))
        write(base / "codex" / "AGENTS.md", gen_agents_md(stack))

        # Docs (architecture & principles are stack-specific)
        write(base / "docs" / "architecture.md", gen_architecture(stack))
        write(base / "docs" / "golden-principles.md", gen_golden_principles(stack))
        write(base / "docs" / "onboarding.md", gen_onboarding(stack))

        # Config
        write(base / "config" / "lint-config.txt", gen_lint_config(stack))

        # Enforcement & automation (NEW: harness mechanical enforcement)
        write(base / "scripts" / "layer-check.sh", gen_layer_check(stack))
        write(base / "scripts" / "init.sh", gen_init_sh(stack))
        write(base / "ci" / "ci.yml", gen_github_ci(stack))
        write(base / "config" / "pre-commit-config.yaml", gen_pre_commit_config(stack))

        # README
        write(base / "README.md", gen_readme(stack_id, stack))

    # --- Combos ---
    print("\n🔗 Generating combos...")
    for combo_id, combo in COMBOS.items():
        write(BASE / "combos" / combo_id / "README.md", gen_combo_readme(combo_id, combo))

    write(BASE / "README.md", gen_root_readme())

    # --- Manifest ---
    manifest = {
        "generated": TODAY,
        "stacks": {k: {"name": v["name"], "category": v["category"], "lang": v["lang"]}
                   for k, v in STACKS.items()},
        "combos": {k: {"name": v["name"], "frontend": v["frontend"], "backend": v["backend"]}
                   for k, v in COMBOS.items()},
    }
    write(BASE / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    # Count
    count = sum(1 for _ in BASE.rglob("*") if _.is_file())
    print(f"\n✅ Done! Generated {count} files.")


if __name__ == "__main__":
    main()
