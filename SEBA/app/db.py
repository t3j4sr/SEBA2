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


def get_supabase() -> Client:
    global _client
    if _client is None:
        _client = create_client(_SUPABASE_URL, _SUPABASE_KEY)
    return _client
