"""日志初始化。"""

import logging

from app.common.settings import settings


def configure_logging() -> None:
    """初始化基础日志配置。"""
    logging.basicConfig(
        level=logging.DEBUG if settings.app_debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
