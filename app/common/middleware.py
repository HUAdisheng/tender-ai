"""应用中间件注册。"""

import time
import uuid

from fastapi import FastAPI, Request


def register_middlewares(app: FastAPI) -> None:
    """注册基础中间件。"""

    @app.middleware("http")
    async def add_request_context(request: Request, call_next):
        """补充请求链路上下文，便于后续排查。"""
        request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        started_at = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - started_at
        response.headers["X-Request-Id"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        return response
