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
- 包管理：`uv`
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

## 启动方式

当前项目已经具备最小可运行后端骨架，可以按下面步骤启动。

推荐直接使用启动脚本：

```bash
bash scripts/dev.sh
```

脚本会自动完成：

- 检查 `uv`
- 创建 `.venv`
- 安装依赖
- 生成 `.env`
- 启动 `uvicorn`

如果你希望手动执行，也可以按下面步骤启动。

1. 安装 `uv`

如果本机还没有 `uv`，可以先执行：

```bash
pip install uv
```

2. 创建并激活虚拟环境

```bash
uv venv
source .venv/bin/activate
```

3. 安装依赖

```bash
uv pip install -e . --no-build-isolation
```

4. 准备环境变量

```bash
cp .env.example .env
```

当前基础框架启动时不强依赖数据库、Redis 或其他外部服务；如果暂时不配置这些变量，也可以先启动服务。

5. 启动 FastAPI

```bash
uvicorn app.main:app --reload
```

默认启动地址：

- `http://127.0.0.1:8000`

6. 验证服务是否正常

打开：

- `http://127.0.0.1:8000/v1/health`

预期返回：

```json
{
  "status": "ok",
  "app": "Tender AI",
  "env": "local"
}
```

如果后续补了锁文件，也可以直接使用：

```bash
uv sync
```

## 架构原则

- 先采用单体应用，避免过早微服务化
- 顶层按接口、配置、数据模型、仓储、服务、任务、AI 基架与基础能力分层组织
- `integrations/` 负责第三方 client，`ai/` 负责 LangChain 基架与统一 AI 能力封装
- 长耗时链路统一任务化，避免把解析与生成逻辑杂糅在接口层
- 当前仓库先固定目录骨架，再逐步补充每层实现文件

详细设计以技术文档为准。
