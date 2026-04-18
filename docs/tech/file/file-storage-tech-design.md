# Tender AI 文件能力说明

## 1. 设计范围

本文档整理当前项目中文件相关能力的用法、边界和配置方式，覆盖以下内容：

- 文件上传接口的当前行为
- `FileService` 在项目中的复用方式
- `rustfs` 存储适配的当前实现
- 本地开发环境下 `rustfs` 相关配置应该如何设置

本文档基于以下实现整理：

- [`app/api/v1/files.py`](../../../app/api/v1/files.py)
- [`app/services/file_service.py`](../../../app/services/file_service.py)
- [`app/storage/rustfs.py`](../../../app/storage/rustfs.py)
- [`app/common/settings.py`](../../../app/common/settings.py)
- [`app/models/user.py`](../../../app/models/user.py)

## 2. 当前文件能力概览

### 2.1 当前已实现能力

当前项目已落地的文件能力只有一个主入口：

- `POST /api/v1/api/files/upload`

该接口负责：

- 接收单个上传文件
- 从登录 token 中提取 `user_id`
- 通过 `FileService` 做统一校验与存储编排
- 将文件保存到 `rustfs` 适配层
- 返回文件原始名称、实际落盘名称、存储相对路径和文件大小

### 2.2 当前未实现能力

当前阶段尚未实现以下文件相关能力：

- 文件元数据入库
- 文件下载接口
- 文件访问权限校验
- 文件删除、覆盖、版本管理
- 文件与业务实体的关系表

## 3. 当前代码中的文件用法

### 3.1 接口层用法

文件上传接口位于 [`app/api/v1/files.py`](../../../app/api/v1/files.py)。

当前路由层职责非常明确：

- 解析 `UploadFile`
- 解析认证用户
- 注入 `FileService`
- 调用 `file_service.save_upload_file(...)`
- 返回统一响应

当前接口使用 token 中的 `sub` 作为 `user_id`，这一点与 [`t_users`](../../../app/models/user.py) 的主键语义保持一致。

### 3.2 服务层用法

文件服务位于 [`app/services/file_service.py`](../../../app/services/file_service.py)。

当前 `FileService` 提供两个主要入口：

- `save_upload_file(user_id, upload_file, policy=None)`
- `save_bytes(user_id, filename, body, content_type=None, policy=None)`

适用场景如下：

`save_upload_file(...)`

- 适合 FastAPI 路由直接接收 `UploadFile` 后调用
- 内部会分块读取上传内容，避免默认一次性读完整文件

`save_bytes(...)`

- 适合其他业务服务复用
- 适合调用方已经拿到二进制内容的场景
- 不依赖 FastAPI，可被后续知识库、招标文件、导出归档等服务复用

### 3.3 存储层用法

存储适配位于 [`app/storage/rustfs.py`](../../../app/storage/rustfs.py)。

当前 `RustFsClient` 负责的只有存储层职责：

- 根据配置决定使用远端 `rustfs` 或本地目录回退模式
- 按 `user_id` 做一级目录隔离
- 按 `namespace` 做业务子目录隔离
- 净化文件名，避免路径穿越
- 处理同名文件冲突
- 返回真实落盘文件名和相对路径

当前存储模式说明：

- 当 `RUSTFS_ENDPOINT`、`RUSTFS_ACCESS_KEY`、`RUSTFS_SECRET_KEY`、`RUSTFS_BUCKET` 都配置完整时，走真实 `rustfs` 的 S3 兼容上传
- 当上述配置不完整时，回退到本地目录模式

存储层不负责：

- HTTP 请求解析
- 文件类型校验
- 文件大小校验
- 业务权限判断
- 文件归属关系持久化

## 4. 当前上传规则

### 4.1 默认规则

当前 `FileService` 的默认上传策略如下：

- 默认允许后缀：`.pdf`、`.docx`
- 默认最大文件大小：`20 MB`
- 默认命名空间：`uploads`

### 4.2 当前路径组织方式

当前存储相对路径组织格式如下：

```text
<user_id>/<namespace>/<stored_filename>
```

默认上传接口的实际路径格式为：

```text
<user_id>/uploads/<stored_filename>
```

例如：

```text
8a3f8fd0-0e8b-4f34-9b22-4f580c7b6736/uploads/tender.pdf
8a3f8fd0-0e8b-4f34-9b22-4f580c7b6736/uploads/tender_1.pdf
```

### 4.3 当前响应字段

上传成功后，当前返回字段如下：

- `original_filename`
- `stored_filename`
- `path`
- `size_bytes`
- `content_type`

其中：

- `original_filename` 表示客户端上传时的原始文件名
- `stored_filename` 表示净化并处理重名后的真实落盘文件名
- `path` 表示相对于 `rustfs` 根目录的路径

## 5. 其他服务应该如何复用

### 5.1 路由直接上传

如果某个接口直接接收 `UploadFile`，建议复用 `save_upload_file(...)`：

```python
from fastapi import Depends, UploadFile

from app.api.v1.files import get_file_service
from app.services.file_service import FileSavePolicy, FileService


async def upload_tender_source(
    file: UploadFile,
    current_user: dict,
    file_service: FileService = Depends(get_file_service),
):
    return await file_service.save_upload_file(
        user_id=str(current_user["sub"]),
        upload_file=file,
        policy=FileSavePolicy(namespace="tenders/source"),
    )
```

### 5.2 业务服务内部复用

如果其他服务已经拿到了文件字节内容，建议复用 `save_bytes(...)`：

```python
saved = file_service.save_bytes(
    user_id=user_id,
    filename="knowledge.docx",
    body=file_bytes,
    policy=FileSavePolicy(namespace="knowledge_base/raw_documents"),
)
```

### 5.3 推荐复用方式

后续各业务服务复用时，建议遵循以下规则：

- 统一复用 `FileService`，不要各自直接写文件
- 通过 `namespace` 区分不同业务目录
- 文件类型、大小限制通过 `FileSavePolicy` 覆盖
- 文件和业务实体的关联关系留给各自业务服务或仓储层处理

推荐命名空间示例：

- `uploads`
- `tenders/source`
- `knowledge_base/raw_documents`
- `exports/generated_docs`

## 6. rustfs 配置应该怎么设置

### 6.1 当前代码实际读取的配置项

当前配置定义位于 [`app/common/settings.py`](../../../app/common/settings.py)：

- `RUSTFS_ENDPOINT`
- `RUSTFS_ACCESS_KEY`
- `RUSTFS_SECRET_KEY`
- `RUSTFS_BUCKET`

当前配置生效规则：

- 如果 `RUSTFS_ENDPOINT`、`RUSTFS_ACCESS_KEY`、`RUSTFS_SECRET_KEY`、`RUSTFS_BUCKET` 都配置完整，则使用远端 `rustfs`
- 如果四项中任意一项缺失，则回退到本地目录模式
- 本地目录模式下，`RUSTFS_BUCKET` 表示本地文件落盘根目录
- 远端模式下，`RUSTFS_BUCKET` 表示对象存储中的 bucket 名称
- 远端模式依赖 `minio` Python 客户端，更新依赖后需要执行 `uv sync` 或重新安装项目依赖

### 6.2 本地开发建议配置

本地开发环境建议这样设置：

```env
RUSTFS_BUCKET=./data/rustfs_bucket
RUSTFS_ENDPOINT=
RUSTFS_ACCESS_KEY=
RUSTFS_SECRET_KEY=
```

说明：

- `RUSTFS_BUCKET` 当前在本地适配实现中表示“文件落盘根目录”
- 建议使用项目内相对路径，如 `./data/rustfs_bucket`
- 若不设置 `RUSTFS_BUCKET`，代码会默认落到 `data/rustfs_bucket`

### 6.3 如果使用绝对路径

如果你希望把文件落到固定目录，也可以这样配置：

```env
RUSTFS_BUCKET=/data/tender-ai/rustfs_bucket
RUSTFS_ENDPOINT=
RUSTFS_ACCESS_KEY=
RUSTFS_SECRET_KEY=
```

适用场景：

- Docker 容器挂载宿主机目录
- 本地希望把文件和代码目录分开

### 6.4 远端 rustfs 配置示例

如果已经有公网或内网可访问的 `rustfs`，建议这样配置：

```env
RUSTFS_ENDPOINT=http://69.5.20.251:9000
RUSTFS_ACCESS_KEY=rustfsadmin
RUSTFS_SECRET_KEY=rustfsadmin
RUSTFS_BUCKET=tenderai
```

说明：

- `RUSTFS_ENDPOINT` 填写对象存储 S3 兼容服务地址
- `RUSTFS_BUCKET` 需要是已经存在或允许自动创建的 bucket
- 当前实现会在首次上传时检查 bucket 是否存在；若不存在，会尝试自动创建
- 若你使用公网地址，建议尽快改掉默认账号密码，并优先使用 HTTPS

## 7. 当前使用建议

当前阶段建议这样使用文件能力：

- 本地开发时优先使用本地目录模式
- 联调或部署时再配置完整远端 `rustfs` 信息
- 路由层统一调用 `FileService`
- 后续不同业务通过 `namespace` 区分子目录
- 文件元数据入库、业务关系绑定和权限判断放到后续业务服务中实现

不建议当前阶段这样做：

- 在业务代码中直接 `Path.write_bytes(...)`
- 让路由层自行拼存储路径
- 用原始文件名直接拼接目录
