"""通用文件服务。

该服务统一处理文件上传校验与存储编排，供多个业务服务复用。
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import FrozenSet

from fastapi import HTTPException, UploadFile, status

from app.schemas.file import FileUploadResponseData
from app.storage.rustfs import RustFsClient

DEFAULT_ALLOWED_SUFFIXES: FrozenSet[str] = frozenset({".pdf", ".docx"})
DEFAULT_MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class FileSavePolicy:
    """文件保存策略。

    `namespace` 用于给不同业务场景做逻辑隔离，例如 `tenders/source`
    或 `knowledge_base/raw_documents`。
    """

    allowed_suffixes: FrozenSet[str] = DEFAULT_ALLOWED_SUFFIXES
    max_file_size_bytes: int = DEFAULT_MAX_FILE_SIZE_BYTES
    namespace: str = "uploads"


class FileService:
    """负责文件校验、命名与存储编排。"""

    def __init__(
        self,
        storage_client: RustFsClient,
        default_policy: FileSavePolicy | None = None,
    ) -> None:
        """初始化文件服务。"""
        self._storage_client = storage_client
        self._default_policy = default_policy or FileSavePolicy()

    async def save_upload_file(
        self,
        user_id: str,
        upload_file: UploadFile,
        policy: FileSavePolicy | None = None,
    ) -> FileUploadResponseData:
        """保存 FastAPI 上传文件。"""
        resolved_policy = policy or self._default_policy
        original_filename = upload_file.filename or "upload"
        body = await self._read_upload_body(upload_file=upload_file, policy=resolved_policy)
        return self.save_bytes(
            user_id=user_id,
            filename=original_filename,
            body=body,
            content_type=upload_file.content_type,
            policy=resolved_policy,
        )

    def save_bytes(
        self,
        user_id: str,
        filename: str,
        body: bytes,
        content_type: str | None = None,
        policy: FileSavePolicy | None = None,
    ) -> FileUploadResponseData:
        """保存二进制文件内容。

        该方法适合后续被其他业务服务复用，不依赖 FastAPI 的 `UploadFile`。
        """
        resolved_policy = policy or self._default_policy
        self._validate_user_id(user_id)
        original_filename = filename.strip() or "upload"
        suffix = self._extract_suffix(original_filename)
        self._validate_suffix(suffix=suffix, policy=resolved_policy)
        self._validate_body(body=body, policy=resolved_policy)

        stored_file = self._storage_client.save_file(
            user_id=user_id,
            filename=original_filename,
            body=body,
            namespace=resolved_policy.namespace,
        )
        return FileUploadResponseData(
            original_filename=original_filename,
            stored_filename=stored_file.filename,
            path=stored_file.path,
            size_bytes=len(body),
            content_type=content_type,
        )

    def with_namespace(self, namespace: str) -> "FileService":
        """基于当前服务生成一个新的命名空间视图。"""
        return FileService(
            storage_client=self._storage_client,
            default_policy=replace(self._default_policy, namespace=namespace),
        )

    @staticmethod
    def _validate_user_id(user_id: str) -> None:
        """校验用户标识。"""
        if not str(user_id).strip():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token payload",
            )

    @staticmethod
    def _extract_suffix(filename: str) -> str:
        """提取并标准化文件后缀。"""
        dot_index = filename.rfind(".")
        if dot_index < 0:
            return ""
        return filename[dot_index:].lower()

    @staticmethod
    def _validate_suffix(suffix: str, policy: FileSavePolicy) -> None:
        """校验文件后缀。"""
        if suffix not in policy.allowed_suffixes:
            allowed_text = ", ".join(sorted(policy.allowed_suffixes))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"unsupported file type: {suffix}, allowed: {allowed_text}",
            )

    @staticmethod
    def _validate_body(body: bytes, policy: FileSavePolicy) -> None:
        """校验文件内容大小。"""
        if not body:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="empty file is not allowed",
            )

        if len(body) > policy.max_file_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"file size exceeds limit: {policy.max_file_size_bytes} bytes",
            )

    @staticmethod
    async def _read_upload_body(upload_file: UploadFile, policy: FileSavePolicy) -> bytes:
        """分块读取上传内容，避免一次性吞入过大文件。"""
        chunks: list[bytes] = []
        total_size = 0
        chunk_size = 1024 * 1024

        while True:
            chunk = await upload_file.read(chunk_size)
            if not chunk:
                break

            total_size += len(chunk)
            if total_size > policy.max_file_size_bytes:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"file size exceeds limit: {policy.max_file_size_bytes} bytes",
                )
            chunks.append(chunk)

        return b"".join(chunks)
