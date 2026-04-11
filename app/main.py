from fastapi import FastAPI

from app.api.router import api_router
from app.common.logging import configure_logging
from app.common.middleware import register_middlewares
from app.common.settings import settings


def create_app() -> FastAPI:
    """创建应用实例。"""
    configure_logging()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        debug=settings.app_debug,
    )
    register_middlewares(app)
    app.include_router(api_router)

    return app


app = create_app()
