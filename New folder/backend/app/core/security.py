"""JWT token management, password hashing, and Fernet field encryption.

Usage::

    hashed = hash_password("my-secret")
    assert verify_password("my-secret", hashed)

    token = create_access_token({"sub": str(user_id)})
    payload = decode_token(token)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from cryptography.fernet import Fernet, InvalidToken
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings
from app.core.exceptions import UnauthorizedException

settings = get_settings()

# ─── Password hashing ───────────────────────────────────────────────────────

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """Return a bcrypt hash of *plain*."""
    return _pwd_ctx.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Return ``True`` if *plain* matches the bcrypt *hashed* value."""
    return _pwd_ctx.verify(plain, hashed)


# ─── JWT helpers ─────────────────────────────────────────────────────────────

def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token.

    Parameters
    ----------
    data:
        Payload claims.  Must include ``"sub"`` (subject / user id).
    expires_delta:
        Custom lifetime.  Defaults to ``ACCESS_TOKEN_EXPIRE_MINUTES``.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc), "jti": str(uuid.uuid4())})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict[str, Any]) -> str:
    """Create a long-lived refresh token.

    Refresh tokens have the claim ``"type": "refresh"`` so they cannot
    be confused with access tokens.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid.uuid4()),
        "type": "refresh",
    })
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT, raising on expiry or tampering."""
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("sub") is None:
            raise UnauthorizedException("Token is missing subject claim.")
        return payload
    except JWTError as exc:
        raise UnauthorizedException(f"Token validation failed: {exc}") from exc


# ─── Fernet field encryption ────────────────────────────────────────────────

def _get_fernet() -> Fernet:
    """Lazy singleton for the Fernet cipher."""
    return Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_value(plain: str) -> str:
    """Encrypt a string and return the Base-64 encoded ciphertext."""
    return _get_fernet().encrypt(plain.encode()).decode()


def decrypt_value(cipher: str) -> str:
    """Decrypt a Fernet token back to plain text."""
    try:
        return _get_fernet().decrypt(cipher.encode()).decode()
    except InvalidToken as exc:
        raise ValueError("Failed to decrypt value — key mismatch or corrupted data.") from exc
