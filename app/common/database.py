"""数据库基础设施。"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.common.settings import settings


engine = create_engine(settings.database.url) if settings.database.url else None

SessionLocal = (
    sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)
    if engine is not None
    else None
)


def get_db_session() -> Generator[Session, None, None]:
    """提供数据库会话依赖。"""
    if SessionLocal is None:
        raise RuntimeError("Database is not configured.")

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
