"""
Manual Spending Entry Router
POST /add/spending  — User manually logs a spend via the web UI.
Auto-detects category and impulsive flag. Date defaults to today.
"""
from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.categorizer import categorize, is_impulsive
from app.db import get_supabase

router = APIRouter()


class SpendingEntry(BaseModel):
    description: str  = Field(..., description="What was spent on (e.g. 'Swiggy dinner')")
    amount:      float = Field(..., gt=0, description="Amount in INR")
    user_id:     str  = Field(default="00000000-0000-0000-0000-000000000001")
    date:        Optional[str] = Field(
        default=None,
        description="Date in YYYY-MM-DD format. Defaults to today if omitted.",
    )


@router.post("/spending", summary="Manually log a spending entry")
async def add_spending(entry: SpendingEntry):
    txn_date = entry.date or str(date.today())

    category = categorize(entry.description)
    flagged, reason = is_impulsive(
        category=category,
        amount=entry.amount,
        transaction_date=date.fromisoformat(txn_date),
    )

    row = {
        "user_id":        entry.user_id,
        "amount":         entry.amount,
        "date":           txn_date,
        "merchant":       entry.description,
        "category":       category,
        "is_impulsive":   flagged,
        "impulse_reason": reason,
        "source":         "manual",
        "raw_text":       f"{txn_date} | {entry.description} | ₹{entry.amount}",
    }

    db = get_supabase()
    res = db.table("transactions").insert(row).execute()

    stored = res.data[0] if res.data else row
    return {
        "status":         "ok",
        "id":             stored.get("id"),
        "category":       category,
        "is_impulsive":   flagged,
        "impulse_reason": reason,
        "date":           txn_date,
    }
