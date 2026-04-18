"""文件服务单元测试。"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi import HTTPException

from app.services.file_service import FileSavePolicy, FileService
from app.storage.rustfs import RustFsClient


def build_file_service(tmp_path: Path) -> FileService:
    """构造测试用文件服务。"""
    storage_client = RustFsClient(base_path=tmp_path)
    return FileService(storage_client=storage_client)


def test_save_bytes_returns_real_stored_filename_when_name_conflicts(tmp_path: Path) -> None:
    """同名文件冲突时应返回真实落盘文件名。"""
    file_service = build_file_service(tmp_path)

    first = file_service.save_bytes(
        user_id="user-1",
        filename="tender.pdf",
        body=b"first",
    )
    second = file_service.save_bytes(
        user_id="user-1",
        filename="tender.pdf",
        body=b"second",
    )

    assert first.stored_filename == "tender.pdf"
    assert second.stored_filename == "tender_1.pdf"
    assert second.path == "user-1/uploads/tender_1.pdf"


def test_save_bytes_sanitizes_traversal_filename(tmp_path: Path) -> None:
    """上传文件名中包含路径穿越片段时应被净化。"""
    file_service = build_file_service(tmp_path)

    saved = file_service.save_bytes(
        user_id="user-1",
        filename="../../secret.pdf",
        body=b"payload",
    )

    assert saved.stored_filename == "secret.pdf"
    assert saved.path == "user-1/uploads/secret.pdf"
    assert (tmp_path / "user-1" / "uploads" / "secret.pdf").exists()
    assert not (tmp_path / "secret.pdf").exists()


def test_save_bytes_rejects_empty_file(tmp_path: Path) -> None:
    """空文件应被拒绝。"""
    file_service = build_file_service(tmp_path)

    with pytest.raises(HTTPException) as exc_info:
        file_service.save_bytes(
            user_id="user-1",
            filename="empty.pdf",
            body=b"",
        )

    assert exc_info.value.status_code == 400


def test_save_bytes_rejects_oversized_file(tmp_path: Path) -> None:
    """超出大小限制的文件应被拒绝。"""
    file_service = build_file_service(tmp_path)
    policy = FileSavePolicy(max_file_size_bytes=4)

    with pytest.raises(HTTPException) as exc_info:
        file_service.save_bytes(
            user_id="user-1",
            filename="large.pdf",
            body=b"12345",
            policy=policy,
        )

    assert exc_info.value.status_code == 413


def test_save_bytes_rejects_unsupported_suffix(tmp_path: Path) -> None:
    """不支持的文件类型应被拒绝。"""
    file_service = build_file_service(tmp_path)

    with pytest.raises(HTTPException) as exc_info:
        file_service.save_bytes(
            user_id="user-1",
            filename="notes.txt",
            body=b"payload",
        )

    assert exc_info.value.status_code == 400
