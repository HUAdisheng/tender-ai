"""认证接口。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.database import get_db_session
from app.common.responses import success_result
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResult, RegisterRequest, RegisterResult
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_service(session: Session = Depends(get_db_session)) -> AuthService:
    """构造认证服务依赖。"""
    return AuthService(session=session, user_repository=UserRepository(session))


@router.post("/register", response_model=RegisterResult)
def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> RegisterResult:
    """处理用户注册。"""
    data = auth_service.register(username=request.username, password=request.password)
    return success_result(data.model_dump())


@router.post("/login", response_model=LoginResult)
def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResult:
    """处理用户登录。"""
    data = auth_service.login(username=request.username, password=request.password)
    return success_result(data.model_dump())
