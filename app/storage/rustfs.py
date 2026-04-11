```python
"""最小化的 rustfs 风格本地适配实现（用于文件存储）。

该实现遵循项目约束：提供按企业隔离的文件存储接口。真实环境下可替换为真正的 rustfs 客户端。
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from app.common.settings import settings


class RustFsClient:
    """简单的本地文件存储适配器，模拟 object storage（rustfs）。

    存储目录由 `settings.rustfs.bucket` 指定（如果为空，则使用 ./data/rustfs_bucket）。
    文件按 company_id 子目录隔离，保证不同企业文件不会混淆。
    """

    def __init__(self) -> None:
        bucket = settings.rustfs.bucket or "data/rustfs_bucket"
        self.base_path = Path(bucket)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_file(self, company_id: str, filename: str, body: bytes) -> str:
        """保存文件并返回相对于存储根的路径字符串。

        Args:
            company_id: 企业标识，用于隔离目录。
            filename: 原始文件名（不做信任前缀）
            body: 文件二进制内容。

        Returns:
            存储路径（str），例如 "<company_id>/uploaded_name.pdf"。
        """
        safe_company = str(company_id).strip() or "unknown"
        company_dir = self.base_path / safe_company
        company_dir.mkdir(parents=True, exist_ok=True)

        # 为避免同名冲突，直接按原文件名存储；调用方可扩展为加 UUID 前缀或日期目录
        target = company_dir / filename
        # 若存在同名文件，追加计数后缀
        if target.exists():
            stem = target.stem
            suffix = target.suffix
            i = 1
            while True:
                new_name = f"{stem}_{i}{suffix}"
                new_target = company_dir / new_name
                if not new_target.exists():
                    target = new_target
                    break
                i += 1

        target.write_bytes(body)
        # 返回相对于 base_path 的路径
        return str(target.relative_to(self.base_path))

    def get_file_path(self, company_id: str, relative_path: str) -> Path:
        """返回文件在本地文件系统中的绝对路径。

        不负责文件存在性校验；调用方可自行检查。
        """
        return self.base_path / str(company_id) / relative_path


# 模块级单例，方便被服务或路由引用
rustfs_client = RustFsClient()

```