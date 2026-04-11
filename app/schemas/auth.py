"""认证请求响应模型。"""

from pydantic import BaseModel, ConfigDict, Field

from app.common.result import Result


class RegisterRequest(BaseModel):
    """注册请求。"""

    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """登录请求。"""

    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)


class UserSummary(BaseModel):
    """用户摘要信息。"""

    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    status: str


class RegisterResponseData(BaseModel):
    """注册响应数据。"""

    id: str
    username: str
    status: str


class LoginResponseData(BaseModel):
    """登录响应数据。"""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserSummary


class RegisterResult(Result[RegisterResponseData]):
    """注册接口统一响应。"""


class LoginResult(Result[LoginResponseData]):
    """登录接口统一响应。"""
