"""
Deletes all seeded demo transactions for the hardcoded DEMO_USER_ID.
Run once: python clear_seed.py
"""
from dotenv import load_dotenv
load_dotenv()
from app.db import get_supabase

DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"

db = get_supabase()
result = db.table("transactions").delete().eq("user_id", DEMO_USER_ID).execute()
count = len(result.data) if result.data else 0
print(f"✅ Deleted {count} seeded rows for demo user {DEMO_USER_ID}")
print("Analytics will now show ₹0 until you upload a CSV or add expenses manually.")
