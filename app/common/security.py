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
