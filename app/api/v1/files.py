"""文件上传接口（最小实现）。

说明与假设：
- 为保证企业之间文件不混淆，上传请求必须包含 `X-Company-Id` HTTP 头（字符串）。
- 仅允许上传常见文档格式（pdf、docx）。
- 文件实际存储使用 `app.storage.rustfs` 的本地适配实现，真实环境可替换为真正的 rustfs 客户端。
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile, status, Depends

from app.common.responses import success_result
from app.common.security import get_current_user
from app.services.file_service import file_service

router = APIRouter(prefix="/api/files", tags=["files"])

ALLOWED_SUFFIXES = {".pdf", ".docx"}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
) -> Any:
    """接收单文件上传并保存到 rustfs（按登录用户 id 作为 company_id 隔离）。

    请求必须在 `Authorization: Bearer <token>` 中携带已登录用户的访问令牌，
    我们会解析 token 并取 `sub` 字段作为 company_id（用户即企业）。
    返回存储相对路径与原始文件名。
    """
    # current_user 是 decode_access_token 的 payload
    company_id = str(current_user.get("sub", ""))
    if not company_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token payload")

    filename = file.filename or "upload"
    suffix = "" if "." not in filename else filename[filename.rfind("."):].lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"unsupported file type: {suffix}, allowed: {', '.join(sorted(ALLOWED_SUFFIXES))}",
        )

    body = await file.read()
    saved = file_service.save_company_file(company_id=company_id, filename=filename, body=body)
    return success_result(saved)
