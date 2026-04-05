"""
Seed Script — loads middle_class_expenses.json into Supabase.
Run from the SEBA/ directory:
    python seed.py

The JSON format is:
{
  "person": "...",
  "months": [
    {
      "month": "January",
      "days": [
        {
          "date": "2026-01-01",
          "expenses": [
            {"category": "Food", "description": "Milk", "amount": 28}
          ]
        }
      ]
    }
  ]
}
A fixed demo user_id is used (replace with a real Supabase Auth UUID if needed).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from app.categorizer import categorize, is_impulsive
from app.db import get_supabase

# ── Config ────────────────────────────────────────────────────────────────────
JSON_PATH = Path(__file__).parent.parent / "middle_class_expenses.json"

# Use a fixed demo UUID so the seed is idempotent and easily queryable.
# Replace with a real Supabase Auth user UUID for production.
DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"


def load_json(path: Path) -> dict:
    if not path.exists():
        print(f"[ERROR] JSON file not found: {path}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_rows(data: dict) -> list[dict]:
    rows: list[dict] = []

    for month_block in data.get("months", []):
        for day_block in month_block.get("days", []):
            txn_date: str = day_block["date"]

            for expense in day_block.get("expenses", []):
                description: str = expense["description"]
                amount: float   = float(expense["amount"])

                # Use the JSON's own category as the canonical category,
                # but also run our keyword engine to verify / enrich it.
                json_category: str = expense.get("category", "Misc")
                detected_category  = categorize(description)

                # Trust the JSON label; fall back to detected if it says Misc.
                category = json_category if json_category != "Misc" else detected_category

                from datetime import date
                flagged, reason = is_impulsive(
                    category=category,
                    amount=amount,
                    transaction_date=date.fromisoformat(txn_date),
                )

                rows.append({
                    "user_id":        DEMO_USER_ID,
                    "amount":         amount,
                    "date":           txn_date,
                    "merchant":       description,
                    "category":       category,
                    "is_impulsive":   flagged,
                    "impulse_reason": reason,
                    "source":         "json",
                    "raw_text":       f"{txn_date} | {description} | ₹{amount}",
                })

    return rows


def seed():
    print(f"[SEBA Seed] Loading: {JSON_PATH}")
    data = load_json(JSON_PATH)
    rows = build_rows(data)

    if not rows:
        print("[WARN] No rows to insert.")
        return

    print(f"[SEBA Seed] Inserting {len(rows)} transactions for demo user {DEMO_USER_ID}...")

    db = get_supabase()

    # Clear existing demo data first to keep seeding idempotent
    db.table("transactions").delete().eq("user_id", DEMO_USER_ID).execute()

    # Batch insert in chunks of 50
    BATCH = 50
    total_stored = 0
    for i in range(0, len(rows), BATCH):
        chunk = rows[i : i + BATCH]
        res = db.table("transactions").insert(chunk).execute()
        stored = len(res.data) if res.data else 0
        total_stored += stored
        print(f"  Batch {i // BATCH + 1}: inserted {stored} rows")

    print(f"\n[SEBA Seed] ✅ Done — {total_stored} transactions seeded.")
    print(f"            Demo user_id: {DEMO_USER_ID}")
    print(f"            Test: GET /analytics/dashboard/{DEMO_USER_ID}")


if __name__ == "__main__":
    seed()
