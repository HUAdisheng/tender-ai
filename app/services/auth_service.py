"""认证业务编排。"""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.common.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginResponseData, RegisterResponseData, UserSummary


class AuthService:
    """负责注册与登录流程。"""

    def __init__(self, session: Session, user_repository: UserRepository):
        """初始化认证服务。"""
        self._session = session
        self._user_repository = user_repository

    def register(self, username: str, password: str) -> RegisterResponseData:
        """执行注册流程。"""
        try:
            if self._user_repository.exists_by_username(username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="username already exists",
                )

            hashed_password = hash_password(password)
            user = self._user_repository.save_user(username=username, password=hashed_password)
            self._session.commit()
            return RegisterResponseData(
                id=str(user.id),
                username=user.username,
                status=user.status,
            )
        except HTTPException:
            self._session.rollback()
            raise
        except Exception:
            self._session.rollback()
            raise

    def login(self, username: str, password: str) -> LoginResponseData:
        """执行登录流程。"""
        try:
            user = self._user_repository.get_by_username(username)
            self._validate_login_user(user)

            if not verify_password(password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="username or password is invalid",
                )

            user = self._user_repository.update_last_login_at(user)
            access_token, expires_in = create_access_token(str(user.id), user.username)
            self._session.commit()
            return LoginResponseData(
                access_token=access_token,
                expires_in=expires_in,
                user=UserSummary(
                    id=str(user.id),
                    username=user.username,
                    status=user.status,
                ),
            )
        except HTTPException:
            self._session.rollback()
            raise
        except Exception:
            self._session.rollback()
            raise

    @staticmethod
    def _validate_login_user(user: User | None) -> None:
        """校验用户登录前置条件。"""
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="username or password is invalid",
            )

        if user.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user is disabled",
            )
