# AGENTS.md

## 1. 项目定位

`Tender AI` 是一个面向标书生成场景的 Python 后端项目，当前阶段聚焦以下主链路：

- 招标文件上传与解析
- 知识库文档接入与检索增强生成
- 投标方案目录生成与正文扩写
- 文档导出

当前明确约束：

- 业务上按“企业即用户”建模，不区分企业主体与个人用户主体
- 文件统一使用 `rustfs` 存储
- 当前阶段不启用图库功能
- 架构采用分层单体，不做微服务拆分

## 2. 技术基线

- Python `3.11+`
- `FastAPI`
- `Celery + Redis`
- `PostgreSQL`
- `pgvector`
- `LangChain`
- `python-docx`
- `PyMuPDF`

## 3. 项目结构

```text
app/
├── main.py
├── api/            # 接口层与版本化路由
├── core/           # 配置、数据库、日志、安全、中间件
├── models/         # ORM 模型
├── schemas/        # Pydantic 模型
├── repositories/   # 数据访问层
├── services/       # 业务编排层
├── tasks/          # Celery 任务
├── ai/             # LangChain 基架层与统一 AI 能力封装
├── exporters/      # 文档导出
├── storage/        # 文件存储抽象，当前默认 rustfs
├── integrations/   # OCR、LLM、Embedding 等外部适配
├── domain/         # 枚举、值对象、轻领域规则
└── utils/          # 稳定通用工具
tests/
├── ai/
├── unit/
├── integration/
└── e2e/
```

当前阶段额外约束：

- 先固定目录骨架，目录内具体 `.py` 实现文件按任务逐步补充
- 未经明确要求，不要为了“补完整”预创建一批占位实现文件

## 4. 架构规则

### 4.1 分层单体

- 所有能力运行在一个主应用内
- 路由层保持薄，复杂流程统一收口到 `services/`
- `repositories/` 只做数据访问，`services/` 负责业务编排
- `integrations/` 只负责第三方 SDK/Client 接入
- `ai/` 负责 LangChain、Prompt、Retriever、Chain、Guardrail 等 AI 基架能力
- `exporters/`、`storage/` 提供基础能力，但不要直接承担接口层职责

### 4.2 AI 能力边界

`ai/` 负责承接统一 AI 基架能力：

- Prompt 模板管理
- LangChain chain 封装
- Retriever 与 RAG pipeline 组装
- 结构化输出 parser
- 输出校验、修复与兜底
- callback、trace、token usage 观测
- 对业务层暴露统一 AI gateway

AI 能力层不负责：

- 用户/项目/任务状态管理
- 权限控制
- ORM 模型定义
- 导出记录管理

业务流程不要在路由层散落调用 `LangChain` 组件，应通过 `services/` 统一编排；`services/` 可以调用 `ai/`，但不要直接拼装供应商 SDK。

### 4.3 外部适配

以下依赖统一放入 `integrations/`：

- `rustfs`
- OCR 服务
- LLM 服务
- embedding 服务
- vector store
- 通知服务

## 5. 编码规范

### 5.1 通用规范

- 默认使用 ASCII
- 优先写清晰代码，避免过早抽象
- 默认遵循 `PEP 8`、`PEP 257`、`PEP 484`
- 新增代码时应补充类型标注
- 公共函数、类、模块应有简洁 docstring
- 单个函数保持单一职责，避免超长函数
- 单个模块不应无限膨胀，超过合理复杂度时应主动拆分
- 避免把“工具函数”滥放到 `utils/`
- 不要创建含糊命名，如 `utils.py`、`helpers.py`、`service.py`、`manager.py`，除非作用域非常明确

### 5.2 命名规范

- 包、目录、模块名使用 `snake_case`
- 文件名使用 `snake_case`
- 类名使用 `PascalCase`
- 函数名、方法名、变量名使用 `snake_case`
- 常量名使用 `UPPER_SNAKE_CASE`
- 私有属性和私有函数使用前缀 `_`
- 布尔变量优先使用 `is_`、`has_`、`can_`、`should_` 前缀
- 避免无语义缩写，除通用缩写外不要使用单字符或模糊命名
- `id`、`url`、`ocr`、`llm` 这类行业通用缩写可保留

### 5.3 导入规范

- 导入顺序按“标准库、第三方、本地模块”分组
- 避免未使用导入
- 避免 `from x import *`
- 默认使用绝对导入
- 若发生循环依赖，不要用随意下沉导入糊弄过去，应先调整模块边界

### 5.4 类型与数据建模规范

- 跨层输入输出优先使用 `schemas`
- ORM 模型只表达持久化结构，不承担复杂业务逻辑
- 领域对象表达业务语义，不直接暴露底层存储细节
- 对可空值、集合、映射等类型应明确标注
- 不要在边界不清晰的地方滥用 `Any`

### 5.5 FastAPI 规范

- 路由函数保持薄，不直接承载复杂业务流程
- 请求和响应模型使用 `Pydantic`
- 不要在路由函数中直接操作数据库会话和第三方 SDK
- 路由命名、标签、前缀保持统一
- 健康检查、管理接口和业务接口要分开组织

### 5.6 SQLAlchemy 与 Repository 规范

- 数据访问统一通过 `repositories/`
- 不要在 `services/` 和 `api/` 中直接拼大量 SQL
- Repository 方法命名应体现查询意图，而不是暴露底层实现细节
- 一次改动尽量只影响必要的数据访问逻辑

### 5.7 异常与日志规范

- 不要吞异常
- 只在能提供更多上下文的位置包装异常
- 日志要包含必要上下文，但不要泄露敏感信息
- 不要使用 `print` 代替日志
- 错误信息应有助于排查，不要只写“failed”或“error”

### 5.8 注释规范

- 代码应优先自解释
- 关键代码块、核心业务流程、复杂规则、边界条件处应添加中文注释
- 每个函数、方法在定义上方应有中文注释，简要说明其功能、输入输出或调用场景
- 只在复杂规则、边界条件或不直观设计意图处添加说明性注释
- 注释应解释“为什么”，不要机械解释“做了什么”
- 注释应简洁准确，优先说明设计意图、业务含义和约束条件
- 不要保留过期注释和被注释掉的大段旧代码

## 6. 文件与目录约束

- `core/` 只放基础设施与框架初始化
- `schemas/` 不承载业务逻辑
- `models/` 不直接承担复杂业务编排
- `repositories/` 只做数据访问，不写业务决策
- `services/` 负责业务编排，但不要直接耦合第三方 SDK
- `ai/` 负责统一 AI 基架能力，不承载业务状态流转
- `exporters/` 只放导出能力
- `storage/` 默认按 `rustfs` 方案组织，不要扩展出与当前方向无关的多套存储实现
- `integrations/` 统一收口外部系统适配
- `utils/` 只允许放真正跨层稳定的通用工具

## 7. 最小改动原则

- 代码生成和代码修改应尽可能小
- 优先做局部改动，不要为了“更优雅”顺手大面积重构
- 若不是当前任务明确要求，不要移动文件、重命名模块、重写已有结构
- 一次提交尽量只解决一个问题或一个小功能
- 不要顺手修复与当前任务无关的问题，除非它阻塞当前实现
- 若必须做结构调整，应控制在最小必要范围，并同步更新文档
- 新增抽象前先确认重复是否真实存在，而不是为未来假设提前设计
- 优先复用现有模式，避免同一项目内出现多套并行写法

## 8. 任务与异步规范

- 长耗时流程必须优先考虑异步化
- 解析、知识库入库、生成、导出应通过 `tasks/` 编排
- Celery task 应尽量薄，复杂业务编排放到 `services/`
- 所有任务要具备可重试、可追踪、可记录失败原因的能力

## 9. 测试规范

当前测试目录：

- `tests/ai/`
- `tests/unit/`
- `tests/integration/`
- `tests/e2e/`

建议原则：

- 业务编排优先覆盖 `services/`
- AI 基架能力优先补 `tests/ai/`
- 解析、检索、生成等能力按需要继续细分到对应测试目录
- 关键主链路至少保留可串联的端到端验证入口

## 10. 分支协作规范

- 所有非微小改动都应在独立分支上进行
- 分支应聚焦单一主题，不要把多个无关需求混在一个分支
- 分支命名建议使用：
  - `feature/<short-name>`
  - `fix/<short-name>`
  - `refactor/<short-name>`
  - `docs/<short-name>`
  - `chore/<short-name>`
- 分支名称使用英文小写和短横线，不使用空格和中文
- 未经明确要求，不要直接在主分支上开发

## 11. PR 规范

- 一个 PR 只解决一个清晰问题
- PR 尽量小而完整，便于评审和回滚
- PR 标题应明确说明改动主题
- PR 描述至少应包含：
  - 改了什么
  - 为什么改
  - 影响范围
  - 是否需要迁移、配置变更或数据调整
  - 如何验证
- 若有风险点或后续待做项，应明确写出
- 若改动涉及文档、配置、接口或数据模型，应在 PR 中主动说明
- 未完成的大功能应优先拆成多个可评审的小 PR

建议 PR 标题风格：

- `feat: add tender analysis workflow skeleton`
- `fix: correct project generation state transition`
- `refactor: split ai orchestration from generation service`
- `docs: update global tech design for langchain`

## 12. 文档同步要求

当出现以下变化时，必须同步更新文档：

- 架构分层变化
- 新增或移除核心模块
- 文件存储方案变化
- AI 编排方案变化
- 核心业务假设变化

优先同步：

- `README.md`
- `docs/prd/tender-agent-prd.md`
- `docs/tech/tender-agent-global-tech-design.md`

## 13. 代理工作规则

代理或自动化修改代码时必须遵守：

- 先理解所在模块边界，再修改代码
- 不要把业务逻辑塞回路由层
- 不要把第三方调用散落到业务代码
- 不要随意扩大 `utils/` 目录职责
- 不要在未经确认的情况下引入图库相关设计
- 不要把“企业”和“用户”重新拆成两套主体
- 文件存储默认按 `rustfs` 方案处理
- 默认采取最小可行改动
- 不要制造与当前任务无关的大面积格式化差异
- 若改动会影响多个模块，应先确保依赖方向仍然正确

## 14. 优先实现顺序

建议后续开发顺序：

1. `core` + `api` + `main.py`
2. `models` + `schemas` + `repositories`
3. `integrations` + `ai`
4. `services`
5. `storage`
6. `parsers`
7. `retrieval`
8. `generation`
9. `exporters`
10. `tasks`
11. `tests`

## 15. 成功标准

一个合格的改动应满足：

- 符合模块边界
- 不破坏当前架构方向
- 能让主链路更清晰，而不是更混乱
- 文档与代码口径一致
- 改动范围与任务规模匹配
