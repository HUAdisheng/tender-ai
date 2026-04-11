"""统一成功响应结构。"""

from typing import Any

from app.common.result import Result


def success_result(data: Any) -> Result[Any]:
    """构造成功响应。"""
    return Result[Any](code=0, message="ok", data=data)
