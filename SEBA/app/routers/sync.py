"""
SMS Sync Router
POST /sync/sms  — Accept a batch of raw SMS strings, parse, categorize, and store.
"""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.categorizer import categorize, is_impulsive
from app.db import get_supabase
from app.models import SMSSyncRequest
from app.sms_parser import parse_sms

router = APIRouter()


@router.post("/sms", summary="Ingest a batch of SMS messages")
async def sync_sms(payload: SMSSyncRequest):
    """
    Accepts a list of raw bank SMS strings, parses them, categorizes each
    transaction, flags impulsive purchases, and inserts into Supabase.
    """
    stored, skipped = 0, 0
    rows: list[dict] = []

    for msg in payload.messages:
        received_at: datetime | None = msg.received_at
        parsed = parse_sms(msg.text, received_at)
        if parsed is None:
            skipped += 1
            continue

        category = categorize(parsed["merchant"])
        flagged, reason = is_impulsive(
            category=category,
            amount=parsed["amount"],
            transaction_date=parsed["date"],
            received_at=received_at,
        )

        rows.append({
            "user_id":     payload.user_id,
            "amount":      parsed["amount"],
            "date":        str(parsed["date"]),
            "merchant":    parsed["merchant"],
            "category":    category,
            "is_impulsive": flagged,
            "impulse_reason": reason,
            "source":      "sms",
            "raw_text":    parsed["raw_text"],
        })

    if rows:
        db = get_supabase()
        res = db.table("transactions").insert(rows).execute()
        stored = len(res.data) if res.data else 0

    return {
        "status":  "ok",
        "stored":  stored,
        "skipped": skipped,
        "total":   len(payload.messages),
    }
