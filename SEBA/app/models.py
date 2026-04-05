"""
Pydantic models shared across the application.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Inbound / Request models ─────────────────────────────────────────────────

class SMSMessage(BaseModel):
    text: str = Field(..., description="Raw SMS text received from the bank")
    received_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the SMS was received (ISO 8601). "
                    "Defaults to now if omitted.",
    )


class SMSSyncRequest(BaseModel):
    user_id: str = Field(..., description="Supabase Auth user UUID")
    messages: list[SMSMessage]


# ── Internal / Processing models ──────────────────────────────────────────────

class ParsedTransaction(BaseModel):
    user_id: str
    amount: float
    date: date
    merchant: str
    category: str
    is_impulsive: bool
    source: Literal["sms", "statement", "json"]
    raw_text: str


# ── Response models ───────────────────────────────────────────────────────────

class Transaction(BaseModel):
    id: Optional[int] = None
    user_id: str
    amount: float
    date: date
    merchant: str
    category: str
    is_impulsive: bool
    source: str
    raw_text: str


class DashboardSummary(BaseModel):
    user_id: str
    total_spent: float
    transaction_count: int
    by_category: dict[str, float]
    impulsive_count: int
    impulsive_total: float
    top_merchant: Optional[str]


class ImpulsiveTransaction(BaseModel):
    id: Optional[int]
    date: date
    merchant: str
    category: str
    amount: float
    reason: str
