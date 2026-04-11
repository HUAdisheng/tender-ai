"""健康检查接口。"""

from fastapi import APIRouter

from app.common.settings import settings

router = APIRouter()


@router.get("/health")
def health() -> dict[str, object]:
    """返回服务基础状态。"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
    }
