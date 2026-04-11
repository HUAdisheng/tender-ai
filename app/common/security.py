"""认证安全能力。"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime, timedelta

from app.common.settings import settings

PBKDF2_ITERATIONS = 100_000
PBKDF2_ALGORITHM = "sha256"


def _b64encode(raw: bytes) -> str:
    """使用 URL 安全方式编码字节串。"""
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")


def hash_password(password: str) -> str:
    """生成密码哈希。"""
    salt = secrets.token_hex(16)
    derived_key = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PBKDF2_ITERATIONS,
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${derived_key.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    """校验密码是否匹配。"""
    try:
        algorithm, iterations_text, salt, digest = hashed_password.split("$", maxsplit=3)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    derived_key = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        salt.encode("utf-8"),
        int(iterations_text),
    )
    return hmac.compare_digest(derived_key.hex(), digest)


def create_access_token(user_id: str, username: str) -> tuple[str, int]:
    """签发访问令牌。"""
    expires_in = settings.auth_access_token_expire_seconds
    expires_at = datetime.now(UTC) + timedelta(seconds=expires_in)
    payload = {
        "sub": user_id,
        "username": username,
        "exp": int(expires_at.timestamp()),
    }
    payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_encoded = _b64encode(payload_bytes)
    signature = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        payload_encoded.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    token = f"{payload_encoded}.{_b64encode(signature)}"
    return token, expires_in


def decode_access_token(token: str) -> dict:
    """解析并校验访问令牌，返回载荷字典。

    这是一个最小实现，跟 create_access_token 对称。若校验失败则抛出 ValueError。
    """
    try:
        payload_encoded, signature_encoded = token.split(".", maxsplit=1)
    except ValueError:
        raise ValueError("invalid token format")

    # 校验签名
    expected_sig = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        payload_encoded.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(_b64encode(expected_sig), signature_encoded):
        raise ValueError("invalid token signature")

    # 解码载荷
    # 补齐 base64 padding
    pad = "=" * (-len(payload_encoded) % 4)
    try:
        payload_bytes = base64.urlsafe_b64decode(payload_encoded + pad)
        payload = json.loads(payload_bytes.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - 抛给上层处理
        raise ValueError("invalid token payload") from exc

    # 校验过期
    now_ts = int(datetime.now(UTC).timestamp())
    exp = int(payload.get("exp", 0))
    if exp and now_ts > exp:
        raise ValueError("token expired")

    return payload


from fastapi import Header, HTTPException, status


async def get_current_user(authorization: str | None = Header(None, alias="Authorization")) -> dict:
    """FastAPI 依赖：从 Authorization header 中解析 token 并返回 payload。

    返回值为 token 的 payload（包含 sub, username, exp 等字段）。若 token 无效或缺失，将抛出 HTTPException。
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid Authorization header")

    token = authorization[len("Bearer ") :].strip()
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token")

    return payload
