"""
Auth Router
POST /auth/signup  — Register a new user with username + password.
POST /auth/login   — Verify credentials, return user_id and username.

Uses Python stdlib hashlib (PBKDF2-HMAC-SHA256) — no external dependencies needed.
"""
from __future__ import annotations

import hashlib, hmac, os, uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db import get_supabase

router = APIRouter()


# ── Password helpers (PBKDF2-HMAC-SHA256, 260k iterations) ────────────────────
def _hash_password(password: str) -> str:
    salt = os.urandom(32)
    key  = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 260_000)
    return salt.hex() + ":" + key.hex()


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, key_hex = stored.split(":", 1)
        salt    = bytes.fromhex(salt_hex)
        stored_key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 260_000)
        return hmac.compare_digest(new_key, stored_key)
    except Exception:
        return False


class AuthBody(BaseModel):
    username: str
    password: str


# ── Signup ────────────────────────────────────────────────────────────────────
@router.post("/signup")
async def signup(body: AuthBody):
    username = body.username.strip().lower()
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters.")
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    db = get_supabase()

    try:
        existing = db.table("seba_users").select("id").eq("username", username).execute()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error (have you created the seba_users table?): {str(e)[:200]}"
        )

    if existing.data:
        raise HTTPException(status_code=409, detail="Username already taken.")

    user_id = str(uuid.uuid4())
    hashed  = _hash_password(body.password)

    try:
        db.table("seba_users").insert({
            "id":            user_id,
            "username":      username,
            "password_hash": hashed,
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not create user: {str(e)[:200]}")

    return {"user_id": user_id, "username": username}


# ── Login ─────────────────────────────────────────────────────────────────────
@router.post("/login")
async def login(body: AuthBody):
    username = body.username.strip().lower()
    db = get_supabase()

    try:
        res = db.table("seba_users").select("id, password_hash").eq("username", username).execute()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error (have you created the seba_users table?): {str(e)[:200]}"
        )

    if not res.data:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    row = res.data[0]
    if not _verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    return {"user_id": row["id"], "username": username}
