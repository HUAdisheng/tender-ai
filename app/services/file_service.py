"""文件存储业务封装。

将上层调用与底层 storage 实现解耦。当前实现使用本地 rustfs 适配器（app.storage.rustfs）。
"""

from __future__ import annotations

from typing import Dict

from app.storage.rustfs import rustfs_client


class FileService:
    """提供文件保存相关业务方法。"""

    def __init__(self) -> None:
        self._client = rustfs_client

    def save_company_file(self, company_id: str, filename: str, body: bytes) -> Dict[str, str]:
        """保存文件并返回基本信息。

        Returns dict 包含字段：
        - filename: 最终存储的文件名（含可能的冲突后缀）
        - path: 相对于 storage 根的路径
        """
        path = self._client.save_file(company_id=company_id, filename=filename, body=body)
        return {"filename": filename, "path": path}


file_service = FileService()
