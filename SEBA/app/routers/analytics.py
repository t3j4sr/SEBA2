"""
Analytics Router
GET /analytics/dashboard/{user_id}   — Aggregated spend summary.
GET /analytics/impulsive/{user_id}   — Impulsive transactions list.
GET /analytics/patterns/{user_id}    — Behavioural patterns (risky hours, weekend risk).
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime

from fastapi import APIRouter, HTTPException

from app.db import get_supabase

router = APIRouter()


@router.get("/dashboard/{user_id}")
async def dashboard(user_id: str):
    db = get_supabase()
    res = db.table("transactions").select("*").eq("user_id", user_id).execute()

    if res.data is None:
        raise HTTPException(status_code=500, detail="Database error")

    txns = res.data
    if not txns:
        return {
            "user_id": user_id,
            "total_spent": 0,
            "transaction_count": 0,
            "by_category": {},
            "impulsive_count": 0,
            "impulsive_total": 0,
            "top_merchant": None,
            "monthly_breakdown": {},
        }

    total_spent = sum(float(t["amount"]) for t in txns)
    by_category: dict[str, float] = defaultdict(float)
    for t in txns:
        by_category[t["category"]] += float(t["amount"])

    impulsive_txns  = [t for t in txns if t.get("is_impulsive")]
    impulsive_total = sum(float(t["amount"]) for t in impulsive_txns)

    merchant_spend: dict[str, float] = defaultdict(float)
    for t in txns:
        merchant_spend[t["merchant"]] += float(t["amount"])
    top_merchant = max(merchant_spend, key=merchant_spend.get) if merchant_spend else None

    monthly: dict[str, float] = defaultdict(float)
    for t in txns:
        monthly[str(t["date"])[:7]] += float(t["amount"])

    return {
        "user_id":           user_id,
        "total_spent":       round(total_spent, 2),
        "transaction_count": len(txns),
        "by_category":       {k: round(v, 2) for k, v in sorted(by_category.items(), key=lambda x: -x[1])},
        "impulsive_count":   len(impulsive_txns),
        "impulsive_total":   round(impulsive_total, 2),
        "top_merchant":      top_merchant,
        "monthly_breakdown": {k: round(v, 2) for k, v in sorted(monthly.items())},
    }


@router.get("/impulsive/{user_id}")
async def impulsive(user_id: str):
    db = get_supabase()
    res = (
        db.table("transactions")
        .select("id, date, merchant, category, amount, impulse_reason")
        .eq("user_id", user_id)
        .eq("is_impulsive", True)
        .order("date", desc=True)
        .execute()
    )
    if res.data is None:
        raise HTTPException(status_code=500, detail="Database error")
    return {"user_id": user_id, "count": len(res.data), "transactions": res.data}


@router.get("/patterns/{user_id}")
async def patterns(user_id: str):
    """
    Analyses spending patterns to power the smart reminder system.
    Returns:
      - hourly_spend     : total spent per hour (0-23), derived from created_at
      - risky_hours      : hours where avg-per-tx is >1.5x overall average
      - day_of_week_spend: total by weekday (0=Mon … 6=Sun)
      - weekend_risk     : True if user spends ≥30% more per-tx on weekends
      - behavioral_insights: list of human-readable insight dicts
    """
    db = get_supabase()
    res = (
        db.table("transactions")
        .select("amount, date, created_at, category, is_impulsive, merchant")
        .eq("user_id", user_id)
        .execute()
    )
    txns = res.data or []

    if not txns:
        return {
            "user_id": user_id,
            "hourly_spend": {},
            "hourly_count": {},
            "risky_hours": [],
            "day_of_week_spend": {},
            "day_of_week_count": {},
            "weekend_avg_per_tx": 0,
            "weekday_avg_per_tx": 0,
            "weekend_risk": False,
            "top_impulsive_category": None,
            "behavioral_insights": [],
        }

    hourly_spend: dict[int, float] = defaultdict(float)
    hourly_count: dict[int, int]   = defaultdict(int)
    day_spend:    dict[int, float] = defaultdict(float)
    day_count:    dict[int, int]   = defaultdict(int)
    weekend_amts: list[float] = []
    weekday_amts: list[float] = []

    for t in txns:
        amt = float(t["amount"])

        # Hour from created_at timestamp
        raw_ts = t.get("created_at", "")
        if raw_ts:
            try:
                # Supabase returns ISO strings like "2026-04-04T10:23:00+00:00"
                dt   = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
                hour = dt.hour
                hourly_spend[hour] += amt
                hourly_count[hour] += 1
            except Exception:
                pass

        # Day-of-week from date field
        try:
            d   = date.fromisoformat(str(t["date"])[:10])
            dow = d.weekday()          # 0=Mon … 6=Sun
            day_spend[dow] += amt
            day_count[dow] += 1
            if dow >= 5:
                weekend_amts.append(amt)
            else:
                weekday_amts.append(amt)
        except Exception:
            pass

    # Risky hours: avg-per-tx at that hour > 1.5× overall avg
    overall_avg = sum(float(t["amount"]) for t in txns) / len(txns)
    risky_hours = [
        h for h, total in hourly_spend.items()
        if hourly_count[h] > 0 and (total / hourly_count[h]) > overall_avg * 1.5
    ]

    weekend_avg = sum(weekend_amts) / len(weekend_amts) if weekend_amts else 0
    weekday_avg = sum(weekday_amts) / len(weekday_amts) if weekday_amts else 0
    weekend_risk = (weekend_avg > weekday_avg * 1.3) and len(weekend_amts) >= 3

    # Top impulsive category
    imp_cats: dict[str, int] = defaultdict(int)
    for t in txns:
        if t.get("is_impulsive"):
            imp_cats[t["category"]] += 1
    top_imp_cat = max(imp_cats, key=imp_cats.get) if imp_cats else None

    # Build human-readable insights
    insights = []
    if weekend_risk:
        pct = round((weekend_avg / weekday_avg - 1) * 100) if weekday_avg else 0
        insights.append({
            "type": "weekend",
            "severity": "high",
            "title": "Weekend Splurge Pattern Detected",
            "body": (
                f"You spend ₹{weekend_avg:.0f} on average per transaction on weekends "
                f"vs ₹{weekday_avg:.0f} on weekdays — {pct}% more. "
                "Consider setting a weekend budget."
            ),
        })

    for h in sorted(risky_hours)[:3]:
        label = f"{'12' if h == 12 else h % 12 or 12}{'am' if h < 12 else 'pm'}"
        insights.append({
            "type":     "time",
            "severity": "medium",
            "title":    f"High-Spend Window: {label}",
            "hour":     h,
            "body": (
                f"Transactions made around {label} tend to be larger than your average. "
                "Pause and reflect before buying at this time."
            ),
        })

    if top_imp_cat:
        insights.append({
            "type":     "impulsive",
            "severity": "medium",
            "title":    f"Impulse Hotspot: {top_imp_cat}",
            "body": (
                f"Most of your flagged impulsive purchases fall under {top_imp_cat}. "
                "Try a 10-minute rule before spending in this category."
            ),
        })

    if not insights and len(txns) >= 10:
        insights.append({
            "type":     "positive",
            "severity": "low",
            "title":    "Spending Looks Healthy! 🎉",
            "body":     "No significant overspend patterns detected. Keep it up!",
        })

    return {
        "user_id":               user_id,
        "hourly_spend":          {str(h): round(v, 2) for h, v in sorted(hourly_spend.items())},
        "hourly_count":          {str(h): v           for h, v in sorted(hourly_count.items())},
        "risky_hours":           sorted(risky_hours),
        "day_of_week_spend":     {str(d): round(v, 2) for d, v in sorted(day_spend.items())},
        "day_of_week_count":     {str(d): v           for d, v in sorted(day_count.items())},
        "weekend_avg_per_tx":    round(weekend_avg, 2),
        "weekday_avg_per_tx":    round(weekday_avg, 2),
        "weekend_risk":          weekend_risk,
        "top_impulsive_category": top_imp_cat,
        "behavioral_insights":   insights,
    }
