"""统一响应模型。"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class Result(BaseModel, Generic[DataT]):
    """统一成功响应模型。"""

    code: int | str
    message: str
    data: DataT | None = None
