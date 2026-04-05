"""
Supabase client singleton – shared across all modules.
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

_SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
_SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY", os.environ.get("SUPABASE_SERVICE_ROLE_KEY", ""))

_client: Client | None = None


from fastapi import HTTPException

def get_supabase() -> Client:
    global _client
    if not _SUPABASE_URL or not _SUPABASE_KEY:
        raise HTTPException(
            status_code=500,
            detail="Supabase configuration is missing on the server. Add SUPABASE_URL and SUPABASE_KEY in Render."
        )
    if _client is None:
        _client = create_client(_SUPABASE_URL, _SUPABASE_KEY)
    return _client
