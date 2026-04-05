"""
SMS Parser
----------
Extracts Amount, Merchant, Date, and Type (credit/debit) from
typical Indian bank SMS messages using targeted regular expressions.
"""
from __future__ import annotations

import re
from datetime import date, datetime
from typing import Optional


# ── Regex patterns ────────────────────────────────────────────────────────────

# Amount patterns: Rs.500, INR 1,234.56, ₹ 250
_AMOUNT_RE = re.compile(
    r"(?:rs\.?|inr|₹)\s*([\d,]+(?:\.\d{1,2})?)",
    re.IGNORECASE,
)

# Debit keywords
_DEBIT_RE = re.compile(
    r"\b(debited|debit|paid|spent|withdrawn|purchase|txn)\b",
    re.IGNORECASE,
)

# Credit keywords
_CREDIT_RE = re.compile(
    r"\b(credited|credit|received|refund|cashback)\b",
    re.IGNORECASE,
)

# Merchant: "at MERCHANT", "to MERCHANT", "for MERCHANT"
_MERCHANT_RE = re.compile(
    r"(?:at|to|for|with|from)\s+([A-Za-z0-9\s&\-\.]+?)(?:\s+on|\s+ref|\s+upi|\s+via|\s+using|\.|\Z)",
    re.IGNORECASE,
)

# Date patterns: 01/04/26, 01-04-2026, 01Apr26, 1 Apr 2026
_DATE_RES = [
    re.compile(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})"),
    re.compile(r"(\d{1,2})\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*(\d{2,4})", re.IGNORECASE),
]

_MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def _parse_amount(text: str) -> Optional[float]:
    m = _AMOUNT_RE.search(text)
    if m:
        return float(m.group(1).replace(",", ""))
    return None


def _parse_date(text: str) -> Optional[date]:
    # Numeric date
    m = _DATE_RES[0].search(text)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y = y + 2000 if y < 100 else y
        try:
            return date(y, mo, d)
        except ValueError:
            pass

    # Month-name date
    m = _DATE_RES[1].search(text)
    if m:
        d = int(m.group(1))
        mo = _MONTH_MAP[m.group(2).lower()[:3]]
        y = int(m.group(3))
        y = y + 2000 if y < 100 else y
        try:
            return date(y, mo, d)
        except ValueError:
            pass

    return None


def _parse_merchant(text: str) -> str:
    m = _MERCHANT_RE.search(text)
    if m:
        return m.group(1).strip().title()
    return "Unknown"


def _parse_type(text: str) -> str:
    if _DEBIT_RE.search(text):
        return "debit"
    if _CREDIT_RE.search(text):
        return "credit"
    return "debit"  # default assumption for expense tracker


def parse_sms(
    text: str,
    received_at: Optional[datetime] = None,
) -> Optional[dict]:
    """
    Parse a single SMS string.
    Returns a dict with keys: amount, date, merchant, txn_type, raw_text
    or None if amount cannot be parsed (not a transaction SMS).
    """
    amount = _parse_amount(text)
    if amount is None:
        return None

    txn_date = _parse_date(text) or (received_at.date() if received_at else date.today())
    merchant = _parse_merchant(text)
    txn_type = _parse_type(text)

    return {
        "amount": amount,
        "date": txn_date,
        "merchant": merchant,
        "txn_type": txn_type,
        "raw_text": text,
    }
