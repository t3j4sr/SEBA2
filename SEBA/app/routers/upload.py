"""
Statement Upload Router
POST /upload/statement  — Accept CSV, Excel (.xlsx/.xls), or PDF bank statement and ingest.
"""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.categorizer import categorize, is_impulsive
from app.db import get_supabase
from app.statement_parser import parse_csv, parse_excel, parse_pdf

router = APIRouter()

_ALLOWED_TYPES = {
    "text/csv", "application/csv",
    "application/pdf",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    "application/octet-stream",   # generic fallback
}


@router.post("/statement", summary="Upload a CSV, Excel, or PDF bank statement")
async def upload_statement(
    user_id: str = Form(..., description="Supabase Auth user UUID"),
    file: UploadFile = File(..., description="CSV, Excel, or PDF bank statement"),
):
    filename = (file.filename or "").lower()
    content = await file.read()

    ct = (file.content_type or "").lower()
    
    if filename.endswith(".csv") or ct in ("text/csv", "application/csv", "text/plain", "text/comma-separated-values"):
        transactions = parse_csv(content)
    elif filename.endswith((".xlsx", ".xls")) or "excel" in ct or "spreadsheet" in ct or ct == "application/vnd.ms-excel":
        transactions = parse_excel(content)
    elif filename.endswith(".pdf") or "pdf" in ct:
        transactions = parse_pdf(content)
    elif ct in ("", "application/octet-stream", "binary/octet-stream"):
        # Unknown type — try to detect by magic bytes / fallback to CSV
        if content[:4] == b'%PDF':
            transactions = parse_pdf(content)
        elif content[:2] in (b'PK',):
            transactions = parse_excel(content)
        else:
            transactions = parse_csv(content)
    else:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type ({ct}). Upload a .csv, .xlsx, or .pdf bank statement.",
        )

    if not transactions:
        return {"status": "ok", "stored": 0, "message": "No transactions detected in file. Make sure columns include Date, Amount, and Description/Narration."}

    rows: list[dict] = []
    for t in transactions:
        cat = categorize(t["merchant"])
        flagged, reason = is_impulsive(
            category=cat,
            amount=t["amount"],
            transaction_date=t["date"],
        )
        rows.append({
            "user_id":      user_id,
            "amount":       t["amount"],
            "date":         str(t["date"]),
            "merchant":     t["merchant"],
            "category":     cat,
            "is_impulsive": flagged,
            "impulse_reason": reason,
            "source":       "statement",
            "raw_text":     t["raw_text"],
        })

    db = get_supabase()
    res = db.table("transactions").insert(rows).execute()
    stored = len(res.data) if res.data else 0

    return {
        "status":  "ok",
        "stored":  stored,
        "file":    file.filename,
    }
