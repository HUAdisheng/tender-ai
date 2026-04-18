"""文件上传接口。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile

from app.common.responses import success_result
from app.common.security import get_current_user
from app.schemas.file import FileUploadResult
from app.services.file_service import FileService
from app.storage.rustfs import RustFsClient, get_rustfs_client

router = APIRouter(prefix="/api/files", tags=["files"])


def get_file_service(
    storage_client: RustFsClient = Depends(get_rustfs_client),
) -> FileService:
    """构造文件服务依赖。"""
    return FileService(storage_client=storage_client)


@router.post("/upload", response_model=FileUploadResult)
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
) -> FileUploadResult:
    """接收单文件上传并保存到 rustfs。"""
    user_id = str(current_user.get("sub", ""))
    data = await file_service.save_upload_file(user_id=user_id, upload_file=file)
    return success_result(data)
