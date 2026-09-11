# auth.py
# ---------------------------------------------------------
# Password hashing and JWT (JSON Web Token) session handling.
#
# Passwords: we use Python's built-in hashlib (PBKDF2-HMAC-SHA256,
# 260,000 iterations — the current OWASP-recommended minimum). This
# needs zero extra packages and is the same algorithm family Django
# uses by default. We NEVER store the plain password — only this
# salted hash.
#
# Sessions: after a correct login, we hand back a JWT — a signed
# string that encodes "this is user #42" plus an expiry time. The
# frontend stores it and sends it back on every request in an
# Authorization header. Because it's signed with SECRET_KEY, nobody
# can forge or edit one without the key.
# ---------------------------------------------------------
import hashlib
import hmac
import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import JWT_SECRET_KEY

PBKDF2_ITERATIONS = 260_000
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7   # tokens stay valid for 7 days

# Tells FastAPI where the frontend gets a token from (used only for
# the auto-generated /docs page — the frontend calls /auth/login directly)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def hash_password(password: str) -> str:
    """
    Hashes a password with a random 16-byte salt. The salt is stored
    alongside the hash (both hex-encoded, joined with ':') so we can
    re-derive the same hash later to check a login attempt.
    """
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"{salt.hex()}:{derived.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Re-derives the hash using the SAME salt that was stored, and
    compares it to what's stored. hmac.compare_digest is used instead
    of == to avoid leaking timing information about how much of the
    hash matched (a "timing attack").
    """
    salt_hex, hash_hex = stored_hash.split(":")
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(hash_hex)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return hmac.compare_digest(derived, expected)


def create_access_token(user_id: int) -> str:
    """Creates a signed JWT string encoding which user this session belongs to."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    A FastAPI dependency: any route that adds `user_id: int =
    Depends(get_current_user_id)` to its parameters automatically
    requires a valid token, and gets the signed-in user's id back —
    without ever trusting a user_id the frontend might send in the
    request body itself.
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to sign in to do that.",
        )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Your session has expired. Please sign in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session. Please sign in again.")

    return payload["user_id"]
