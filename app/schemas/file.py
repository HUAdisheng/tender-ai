"""文件上传请求响应模型。"""

from pydantic import BaseModel

from app.common.result import Result


class FileUploadResponseData(BaseModel):
    """文件上传响应数据。"""

    original_filename: str
    stored_filename: str
    path: str
    size_bytes: int
    content_type: str | None = None


class FileUploadResult(Result[FileUploadResponseData]):
    """文件上传接口统一响应。"""
