# Tender AI

面向标书生成场景的 `AI + 知识库` 应用，当前阶段以 `Python` 模块化单体架构为目标方案。

## 当前定位

- 以招标文件解析、知识库增强生成、方案编辑与导出为主链路
- 当前按“企业即用户”建模，不单独区分企业主体与个人用户主体
- 文件统一使用 `rustfs` 作为存储
- 当前阶段暂不启用图库功能

## 文档索引

- 产品需求文档：[docs/prd/tender-agent-prd.md](/home/resonxu/workspace/java_workspace/tender-ai/docs/prd/tender-agent-prd.md)
- 全局技术设计：[docs/tech/tender-agent-global-tech-design.md](/home/resonxu/workspace/java_workspace/tender-ai/docs/tech/tender-agent-global-tech-design.md)

## 推荐技术方向

- 后端：`FastAPI`
- AI 编排：`LangChain`
- 数据库：`PostgreSQL`
- 向量检索：`pgvector`
- 文件存储：`rustfs`
- 缓存/任务支撑：`Redis + Celery`
- 文档导出：`python-docx`

## 架构原则

- 先采用模块化单体，避免过早微服务化
- 在单体内部按领域合理拆分：用户、项目、文件、知识库、招标解析、生成、导出、任务、外部集成
- 长耗时链路统一任务化，避免把解析与生成逻辑杂糅在接口层
- 使用 `LangChain` 作为 AI 工作流编排层，但业务状态与领域规则仍保留在项目自身代码中

详细设计以技术文档为准。
