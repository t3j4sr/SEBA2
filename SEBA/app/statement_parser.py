"""
Statement Parser
----------------
Handles CSV, Excel (.xlsx/.xls), and PDF bank statements.
- CSV/Excel: auto-detects Amount / Date / Narration / Description columns via pandas.
- PDF: extracts text with pdfplumber and applies the same SMS regex pipeline.
"""
from __future__ import annotations

import io
import re
from datetime import date
from typing import Optional

import pandas as pd


# ── Column name normalisation ─────────────────────────────────────────────────
_COL_ALIASES = {
    "amount":       ["amount", "debit", "withdrawal", "dr", "txn amount", "transaction amount"],
    "date":         ["date", "txn date", "transaction date", "value date", "posting date"],
    "description":  ["description", "narration", "particulars", "details", "merchant", "remarks"],
    "credit":       ["credit", "cr", "deposit"],
}


def _normalise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename detected columns to canonical names."""
    mapping: dict[str, str] = {}
    lower_cols = {c.lower().strip(): c for c in df.columns}

    for canonical, aliases in _COL_ALIASES.items():
        for alias in aliases:
            if alias in lower_cols:
                mapping[lower_cols[alias]] = canonical
                break

    return df.rename(columns=mapping)


def _process_df(df: pd.DataFrame) -> list[dict]:
    """Shared logic: normalise columns and extract transactions from a DataFrame."""
    df = _normalise_columns(df)

    # Only amount is truly required; date and description fall back gracefully
    if "amount" not in df.columns:
        raise ValueError(
            f"Could not detect an amount/debit/withdrawal column. Found: {list(df.columns)}"
        )

    transactions: list[dict] = []
    for _, row in df.iterrows():
        amount_raw = row.get("amount")
        try:
            amount = float(str(amount_raw).replace(",", "").strip())
        except (ValueError, TypeError):
            continue

        if amount <= 0:
            continue  # Skip blank/credit rows

        # Date — fall back to today if column missing or unparseable
        txn_date: Optional[date] = None
        if "date" in df.columns:
            try:
                txn_date = pd.to_datetime(row["date"], dayfirst=True).date()
            except Exception:
                txn_date = date.today()
        else:
            txn_date = date.today()

        # Description — fall back to category, then to "Unknown"
        description = (
            str(row.get("description", "")).strip()
            or str(row.get("narration", "")).strip()
            or str(row.get("category", "")).strip()
            or "Unknown"
        )

        txn_type = "credit" if "credit" in df.columns and not pd.isna(row.get("credit")) else "debit"

        transactions.append({
            "amount": amount,
            "date": txn_date,
            "merchant": description[:120],
            "txn_type": txn_type,
            "raw_text": f"{txn_date} | {description} | ₹{amount}",
        })

    return transactions


def parse_csv(content: bytes) -> list[dict]:
    """
    Parse a CSV bank statement.
    Returns list of dicts: {amount, date, merchant, txn_type, raw_text}.
    """
    df = pd.read_csv(io.BytesIO(content), thousands=",", skipinitialspace=True)
    return _process_df(df)


def parse_excel(content: bytes) -> list[dict]:
    """
    Parse an Excel (.xlsx / .xls) bank statement.
    Tries each sheet in order and returns transactions from the first sheet that yields data.
    """
    xl = pd.ExcelFile(io.BytesIO(content))
    for sheet in xl.sheet_names:
        df = xl.parse(sheet, thousands=",", skipinitialspace=True)
        df = df.dropna(how="all").dropna(axis=1, how="all")
        if df.empty:
            continue
        try:
            results = _process_df(df)
            if results:
                return results
        except ValueError:
            continue  # Try next sheet if columns not found
    return []


def parse_pdf(content: bytes) -> list[dict]:
    """
    Parse a PDF bank statement using pdfplumber.
    Falls back to line-by-line SMS regex parsing.
    """
    try:
        import pdfplumber
    except ImportError:
        raise RuntimeError("pdfplumber is required for PDF parsing. Install it with: pip install pdfplumber")

    from app.sms_parser import parse_sms

    transactions: list[dict] = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    headers = [str(h).lower().strip() if h else "" for h in table[0]]
                    for row in table[1:]:
                        row_text = " | ".join(str(c) for c in row if c)
                        parsed = parse_sms(row_text)
                        if parsed:
                            transactions.append(parsed)
            else:
                # No tables — treat each line like an SMS
                text = page.extract_text() or ""
                for line in text.splitlines():
                    parsed = parse_sms(line)
                    if parsed:
                        transactions.append(parsed)

    return transactions
