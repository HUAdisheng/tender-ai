"""rustfs 风格文件存储适配。

该模块负责最小化的文件落盘能力，不承载业务校验逻辑。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

from app.common.settings import settings

_INVALID_SEGMENT_CHARS = re.compile(r"[^A-Za-z0-9._-]+")
_INVALID_FILENAME_CHARS = re.compile(r"[^A-Za-z0-9._-]+")

try:
    from minio import Minio
    from minio.error import MinioException, S3Error
except ImportError:  # pragma: no cover - 依赖缺失时只在远端模式下报错
    Minio = None

    class MinioException(Exception):
        """MinIO 依赖缺失时的兜底异常类型。"""

    class S3Error(MinioException):
        """S3 兼容客户端异常兜底类型。"""


@dataclass(frozen=True, slots=True)
class StoredFile:
    """存储层返回的文件信息。"""

    filename: str
    path: str


class RustFsClient:
    """简单的本地文件存储适配器，模拟 object storage（rustfs）。"""

    def __init__(self, base_path: Path | None = None) -> None:
        """初始化存储根目录。"""
        rustfs_settings = settings.rustfs
        self._bucket_name = rustfs_settings.bucket or "tender-ai"
        self._endpoint = rustfs_settings.endpoint.strip()
        self._access_key = rustfs_settings.access_key.strip()
        self._secret_key = rustfs_settings.secret_key.strip()
        self._bucket_checked = False

        self._use_remote_storage = base_path is None and all(
            [
                self._endpoint,
                self._access_key,
                self._secret_key,
                rustfs_settings.bucket.strip(),
            ]
        )
        self._remote_client = self._build_remote_client() if self._use_remote_storage else None

        if self._use_remote_storage:
            self.base_path = None
            return

        bucket_path = rustfs_settings.bucket or "data/rustfs_bucket"
        self.base_path = base_path or Path(bucket_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_file(
        self,
        user_id: str,
        filename: str,
        body: bytes,
        namespace: str | None = None,
    ) -> StoredFile:
        """保存文件并返回最终落盘结果。"""
        safe_filename = self._sanitize_filename(filename)
        object_key = self._build_object_key(
            user_id=user_id,
            namespace=namespace,
            filename=safe_filename,
        )

        if self._use_remote_storage:
            return self._save_remote_file(
                object_key=object_key,
                filename=safe_filename,
                body=body,
            )

        return self._save_local_file(
            object_key=object_key,
            filename=safe_filename,
            body=body,
        )

    def get_file_path(self, relative_path: str) -> Path:
        """根据相对存储路径返回绝对路径。"""
        if self.base_path is None:
            raise RuntimeError("remote rustfs storage does not expose local file paths")
        return self.base_path / Path(relative_path)

    def _save_remote_file(self, object_key: str, filename: str, body: bytes) -> StoredFile:
        """保存文件到远端 rustfs。"""
        client = self._get_remote_client()
        self._ensure_remote_bucket()

        unique_object_key = self._allocate_remote_object_key(client=client, object_key=object_key)
        data_stream = BytesIO(body)

        try:
            client.put_object(
                bucket_name=self._bucket_name,
                object_name=unique_object_key,
                data=data_stream,
                length=len(body),
            )
        except MinioException as exc:
            raise RuntimeError(f"failed to upload file to rustfs bucket '{self._bucket_name}'") from exc

        return StoredFile(
            filename=Path(unique_object_key).name,
            path=unique_object_key,
        )

    def _save_local_file(self, object_key: str, filename: str, body: bytes) -> StoredFile:
        """保存文件到本地目录。"""
        if self.base_path is None:
            raise RuntimeError("local rustfs storage base path is not configured")

        target = self._allocate_local_target(object_key=object_key)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        return StoredFile(
            filename=filename if target.name == filename else target.name,
            path=str(target.relative_to(self.base_path)),
        )

    def _build_remote_client(self) -> Minio | None:
        """构造远端 S3 兼容客户端。"""
        if Minio is None:
            return None

        parsed = urlparse(self._endpoint)
        endpoint = parsed.netloc or parsed.path
        secure = parsed.scheme == "https"
        return Minio(
            endpoint,
            access_key=self._access_key,
            secret_key=self._secret_key,
            secure=secure,
        )

    def _get_remote_client(self) -> Minio:
        """获取远端存储客户端。"""
        if self._remote_client is None:
            raise RuntimeError(
                "minio dependency is required for remote rustfs storage; "
                "please install project dependencies first",
            )
        return self._remote_client

    def _ensure_remote_bucket(self) -> None:
        """确保远端 bucket 可用。"""
        if self._bucket_checked:
            return

        client = self._get_remote_client()
        try:
            exists = client.bucket_exists(self._bucket_name)
            if not exists:
                client.make_bucket(self._bucket_name)
        except MinioException as exc:
            raise RuntimeError(f"failed to access rustfs bucket '{self._bucket_name}'") from exc

        self._bucket_checked = True

    def _allocate_remote_object_key(self, client: Minio, object_key: str) -> str:
        """为远端对象生成不冲突的 key。"""
        if not self._remote_object_exists(client=client, object_key=object_key):
            return object_key

        object_path = Path(object_key)
        parent = object_path.parent
        stem = object_path.stem
        suffix = object_path.suffix
        index = 1

        while True:
            candidate_name = f"{stem}_{index}{suffix}"
            candidate_key = str(parent / candidate_name) if str(parent) != "." else candidate_name
            if not self._remote_object_exists(client=client, object_key=candidate_key):
                return candidate_key
            index += 1

    def _remote_object_exists(self, client: Minio, object_key: str) -> bool:
        """检查远端对象是否存在。"""
        try:
            client.stat_object(self._bucket_name, object_key)
            return True
        except S3Error as exc:
            if exc.code in {"NoSuchKey", "NoSuchObject", "NoSuchVersion", "NoSuchBucket"}:
                return False
            raise RuntimeError(f"failed to stat rustfs object '{object_key}'") from exc
        except MinioException as exc:
            raise RuntimeError(f"failed to stat rustfs object '{object_key}'") from exc

    def _allocate_local_target(self, object_key: str) -> Path:
        """为本地文件分配不冲突路径。"""
        if self.base_path is None:
            raise RuntimeError("local rustfs storage base path is not configured")

        target = self.base_path / Path(object_key)
        if not target.exists():
            return target

        parent = target.parent
        stem = target.stem
        suffix = target.suffix
        index = 1
        while True:
            candidate = parent / f"{stem}_{index}{suffix}"
            if not candidate.exists():
                return candidate
            index += 1

    def _build_object_key(self, user_id: str, namespace: str | None, filename: str) -> str:
        """构造相对存储 key。"""
        user_segment = self._sanitize_segment(user_id, fallback="unknown")
        namespace_path = self._build_namespace_path(namespace)
        path = Path(user_segment) / namespace_path / filename
        return str(path)

    @staticmethod
    def _build_namespace_path(namespace: str | None) -> Path:
        """将逻辑命名空间转换为安全路径。"""
        if not namespace:
            return Path()

        safe_segments = [
            RustFsClient._sanitize_segment(segment, fallback="")
            for segment in re.split(r"[\\/]+", namespace)
            if segment.strip()
        ]
        safe_segments = [segment for segment in safe_segments if segment]
        if not safe_segments:
            return Path()
        return Path(*safe_segments)

    @staticmethod
    def _sanitize_segment(value: str, fallback: str) -> str:
        """净化单个路径片段，避免路径穿越。"""
        cleaned = _INVALID_SEGMENT_CHARS.sub("_", value.strip())
        cleaned = cleaned.strip("._-")
        return cleaned or fallback

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """净化文件名，确保不会逃逸出目标目录。"""
        basename = filename.replace("\\", "/").split("/")[-1].strip()
        stem = Path(basename).stem or "upload"
        suffix = Path(basename).suffix.lower()

        safe_stem = _INVALID_FILENAME_CHARS.sub("_", stem).strip("._-") or "upload"
        safe_suffix = _INVALID_FILENAME_CHARS.sub("", suffix)
        if safe_suffix and not safe_suffix.startswith("."):
            safe_suffix = f".{safe_suffix}"
        return f"{safe_stem}{safe_suffix}"


@lru_cache(maxsize=1)
def get_rustfs_client() -> RustFsClient:
    """构造可复用的 rustfs 客户端依赖。"""
    return RustFsClient()
