"""用户数据访问。"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """封装用户相关数据库访问。"""

    def __init__(self, session: Session):
        """初始化仓储。"""
        self._session = session

    def get_by_username(self, username: str) -> User | None:
        """按用户名查询未删除用户。"""
        statement = select(User).where(User.username == username, User.is_deleted.is_(False))
        return self._session.execute(statement).scalar_one_or_none()

    def exists_by_username(self, username: str) -> bool:
        """检查用户名是否已存在。"""
        return self.get_by_username(username) is not None

    def save_user(self, username: str, password: str) -> User:
        """保存用户。"""
        user = User(username=username, password=password, status="active", is_deleted=False)
        self._session.add(user)
        self._session.flush()
        self._session.refresh(user)
        return user

    def update_last_login_at(self, user: User) -> User:
        """更新最近登录时间字段。"""
        user.last_login_at = datetime.now(UTC)
        self._session.add(user)
        self._session.flush()
        self._session.refresh(user)
        return user
