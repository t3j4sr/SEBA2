"""
Transactions Router
GET    /transactions/{user_id}  — Paginated transaction list with optional filters.
DELETE /transactions/{tx_id}    — Delete a single transaction by ID.
"""
from __future__ import annotations

from fastapi import APIRouter, Query

from app.db import get_supabase

router = APIRouter()


@router.get("/{user_id}")
async def list_transactions(
    user_id:       str,
    page:          int  = Query(default=1, ge=1),
    page_size:     int  = Query(default=50, ge=1, le=200),
    category:      str  = Query(default=None),
    impulsive_only: bool = Query(default=False),
):
    db     = get_supabase()
    offset = (page - 1) * page_size

    query = (
        db.table("transactions")
        .select("*")
        .eq("user_id", user_id)
        .order("date", desc=True)
        .order("created_at", desc=True)
        .range(offset, offset + page_size - 1)
    )
    if category:
        query = query.eq("category", category)
    if impulsive_only:
        query = query.eq("is_impulsive", True)

    res = query.execute()
    return {
        "page":         page,
        "page_size":    page_size,
        "transactions": res.data or [],
    }


@router.delete("/{tx_id}")
async def delete_transaction(
    tx_id:   int,
    user_id: str = Query(default="00000000-0000-0000-0000-000000000001"),
):
    db = get_supabase()
    db.table("transactions").delete().eq("id", tx_id).eq("user_id", user_id).execute()
    return {"status": "deleted", "id": tx_id}
