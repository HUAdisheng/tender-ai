# Tender AI

面向标书生成场景的 `AI + 知识库` 应用，当前阶段以 `Python` 单体后端骨架为目标方案。

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

## 当前骨架

当前代码结构先按全局分层骨架落目录，目录内具体 `.py` 实现文件后续再定。

```text
app/
├── main.py
├── api/
│   └── v1/
├── core/
├── models/
├── schemas/
├── repositories/
├── services/
├── tasks/
├── ai/
├── exporters/
├── storage/
├── integrations/
├── domain/
└── utils/

tests/
├── ai/
├── unit/
├── integration/
└── e2e/
```

## 架构原则

- 先采用单体应用，避免过早微服务化
- 顶层按接口、配置、数据模型、仓储、服务、任务、AI 基架与基础能力分层组织
- `integrations/` 负责第三方 client，`ai/` 负责 LangChain 基架与统一 AI 能力封装
- 长耗时链路统一任务化，避免把解析与生成逻辑杂糅在接口层
- 当前仓库先固定目录骨架，再逐步补充每层实现文件

详细设计以技术文档为准。
