"""
Transaction Categorizer & Impulsive Purchase Detector
------------------------------------------------------
Pure rule-based with brand alias expansion so short names like
'mcd', 'bk', 'kfc', 'hm' map correctly before keyword matching.
"""
from __future__ import annotations

import re
from datetime import date, datetime


# ── Brand alias map ───────────────────────────────────────────────────────────
# Short names / abbreviations → canonical keyword that appears in CATEGORY_RULES
BRAND_ALIASES: dict[str, str] = {
    # ── Food / QSR ──────────────────────────────────────────────────────────
    "mcd": "mcdonalds",
    "mc": "mcdonalds",
    "mcds": "mcdonalds",
    "mac donalds": "mcdonalds",
    "mac donald": "mcdonalds",
    "bk": "burger king",
    "burger king": "burger king",
    "burgerking": "burger king",
    "kfc": "kfc",
    "kentucky": "kfc",
    "pzh": "pizza hut",
    "pizza hut": "pizza hut",
    "pizzahut": "pizza hut",
    "dominos": "domino",
    "domino's": "domino",
    "subway": "subway restaurant",
    "starbucks": "starbucks cafe",
    "sbucks": "starbucks cafe",
    "ccd": "cafe coffee day",
    "costa": "costa cafe",
    "theobroma": "theobroma bakery",
    "wow momo": "wow momo restaurant",
    "wowmomo": "wow momo restaurant",
    "faasos": "faasos restaurant",
    "behrouz": "behrouz biryani",
    "box8": "box8 food",
    "freshmenu": "freshmenu food",
    "lunchbox": "lunchbox food",
    "biryani blues": "biryani restaurant",
    "oven story": "pizza restaurant",
    "instacart": "groceries",
    "big basket": "bigbasket groceries",
    "bigbasket": "bigbasket groceries",
    "bb daily": "bigbasket groceries",
    "milk basket": "milk groceries",
    "milkbasket": "milk groceries",
    "dunzo": "dunzo groceries",
    "blinkit": "blinkit groceries",
    "zepto": "zepto groceries",
    "swiggy instamart": "instamart groceries",
    "nature's basket": "groceries",
    "reliance fresh": "groceries",
    "more supermarket": "groceries",
    "dmart": "dmart groceries",
    "d-mart": "dmart groceries",
    "haldirams": "haldiram snack",
    "haldiram's": "haldiram snack",

    # ── Shopping / Fashion ───────────────────────────────────────────────────
    "hm": "h&m",
    "h & m": "h&m",
    "h and m": "h&m",
    "hennes": "h&m",
    "zara": "zara clothing",
    "mango": "mango clothing",
    "uniqlo": "uniqlo clothing",
    "gap": "gap clothing",
    "marks spencer": "marks and spencer clothing",
    "m&s": "marks and spencer clothing",
    "ms": "marks and spencer clothing",
    "forever 21": "forever21 clothing",
    "forever21": "forever21 clothing",
    "f21": "forever21 clothing",
    "levis": "levis clothing",
    "levi's": "levis clothing",
    "puma": "puma shoes",
    "nike": "nike shoes",
    "adidas": "adidas shoes",
    "reebok": "reebok shoes",
    "skechers": "skechers shoes",
    "bata": "bata shoes",
    "woodland": "woodland shoes",
    "superdry": "superdry clothing",
    "us polo": "us polo apparel",
    "uspa": "us polo apparel",
    "tommy": "tommy hilfiger clothing",
    "tommy hilfiger": "tommy hilfiger clothing",
    "th": "tommy hilfiger clothing",
    "ck": "calvin klein clothing",
    "calvin klein": "calvin klein clothing",
    "gucci": "gucci shopping",
    "louis vuitton": "louis vuitton shopping",
    "lv": "louis vuitton shopping",
    "chanel": "chanel shopping",
    "burberry": "burberry clothing",
    "westside": "westside clothing",
    "pantaloons": "pantaloons clothing",
    "max": "max fashion clothing",
    "max fashion": "max fashion clothing",
    "lifestyle": "lifestyle clothing",
    "shoppers stop": "shoppers stop clothing",
    "central": "central mall clothing",
    "myntra": "myntra clothing",
    "ajio": "ajio clothing",
    "nykaa": "nykaa shopping",
    "nykaa fashion": "nykaa shopping",
    "meesho": "meesho clothing",
    "snapdeal": "snapdeal shopping",
    "amazon": "amazon shopping",
    "flipkart": "flipkart shopping",

    # ── Transport ────────────────────────────────────────────────────────────
    "ola": "ola cab",
    "rapido": "rapido cab",
    "blu smart": "blusmart cab",
    "blusmart": "blusmart cab",
    "yulu": "yulu transport",
    "bounce": "bounce transport",
    "vogo": "vogo transport",
    "namma yatri": "namma yatri auto",
    "bmtc": "bmtc bus",
    "best bus": "best bus",
    "dtc": "dtc bus",
    "ksrtc": "ksrtc bus",
    "tsrtc": "tsrtc bus",
    "ap travels": "ap bus",

    # ── Bills / Utilities ────────────────────────────────────────────────────
    "act": "act broadband",
    "hathway": "hathway internet",
    "tata sky": "tata sky bill",
    "dish tv": "dish tv bill",
    "sun direct": "sun direct bill",
    "paytm bill": "bill payment",
    "phonepe bill": "bill payment",
    "gpay bill": "bill payment",
    "bescom": "electricity bill",
    "msedcl": "electricity bill",
    "bses": "electricity bill",
    "tpddl": "electricity bill",
    "igl": "gas bill",
    "mgl": "gas bill",
    "adani gas": "gas bill",

    # ── Entertainment ────────────────────────────────────────────────────────
    "netflix": "netflix entertainment",
    "disney+": "hotstar entertainment",
    "disney plus": "hotstar entertainment",
    "hotstar": "hotstar entertainment",
    "prime": "prime video entertainment",
    "amazon prime": "prime video entertainment",
    "apple tv": "apple tv entertainment",
    "zee5": "zee5 entertainment",
    "sony liv": "sonyliv entertainment",
    "sonyliv": "sonyliv entertainment",
    "jio cinema": "jiocinema entertainment",
    "jiocinema": "jiocinema entertainment",
    "mxplayer": "mxplayer entertainment",
    "voot": "voot entertainment",
    "alt balaji": "altbalaji entertainment",
    "spotify": "spotify music",
    "apple music": "apple music",
    "jiosaavn": "jiosaavn music",
    "gaana": "gaana music",
    "wynk": "wynk music",
    "pvr": "pvr cinema",
    "inox": "inox cinema",
    "cinepolis": "cinepolis cinema",
    "bms": "bookmyshow event",
    "book my show": "bookmyshow event",
    "bookmyshow": "bookmyshow event",
    "steam": "steam game",
    "ps": "playstation game",
    "ps5": "playstation game",
    "ps4": "playstation game",
    "xbox": "xbox game",
    "ea": "ea game",
    "epic": "epic games game",

    # ── Health ───────────────────────────────────────────────────────────────
    "apollo": "apollopharmacy medicine",
    "apolo": "apollopharmacy medicine",
    "medplus": "medplus pharmacy",
    "1mg": "1mg pharmacy",
    "netmeds": "netmeds pharmacy",
    "pharmeasy": "pharmeasy pharmacy",
    "practo": "practo doctor",
    "lybrate": "lybrate doctor",
    "cult fit": "cultfit health",
    "cultfit": "cultfit health",
    "curefit": "cultfit health",
    "cure fit": "cultfit health",
    "gold's gym": "gym health",
    "anytime fitness": "gym health",
    "fitpass": "gym health",

    # ── Travel ───────────────────────────────────────────────────────────────
    "oyo": "oyo hotel",
    "goibibo": "goibibo flight",
    "ixigo": "ixigo flight",
    "yatra": "yatra flight",
    "cleartrip": "cleartrip flight",
    "air india": "airindia flight",
    "airindia": "airindia flight",
    "indigo": "indigo flight",
    "spicejet": "spicejet flight",
    "go first": "goair flight",
    "akasa": "akasa air flight",
    "vistara": "vistara flight",
    "treebo": "treebo hotel",
    "fab hotel": "fabhotel hotel",
    "fabhotel": "fabhotel hotel",
    "zostel": "zostel hotel",
    "airbnb": "airbnb hotel",

    # ── Education ────────────────────────────────────────────────────────────
    "udemy": "udemy education",
    "coursera": "coursera education",
    "byju": "byju education",
    "byjus": "byju education",
    "byju's": "byju education",
    "unacademy": "unacademy education",
    "vedantu": "vedantu education",
    "toppr": "toppr education",
    "khan academy": "khan academy education",
    "duolingo": "duolingo education",
    "classplus": "classplus education",
    "great learning": "great learning education",
    "upgrad": "upgrad education",
    "simplilearn": "simplilearn education",
    "scaler": "scaler education",
}


# ── Category keyword map ──────────────────────────────────────────────────────
CATEGORY_RULES: dict[str, list[str]] = {
    "Food": [
        # Self-referential
        "food", "foods", "eating", "eatery", "eat out",
        # Quick service
        "swiggy", "zomato", "mcdonalds", "kfc", "domino", "pizza hut",
        "burger king", "subway restaurant", "starbucks cafe", "cafe coffee day",
        "costa cafe", "theobroma", "wow momo", "faasos", "behrouz", "box8",
        "freshmenu", "lunchbox", "biryani restaurant", "pizza restaurant",
        # Grocery / delivery
        "bigbasket groceries", "instamart groceries", "blinkit groceries",
        "zepto groceries", "milk groceries", "dunzo groceries",
        "dmart groceries", "reliance fresh", "more supermarket",
        # Generic food words
        "restaurant", "cafe", "chai", "tea", "snack", "idli", "dosa", "milk",
        "vegetables", "fruits", "groceries", "grocery", "breakfast", "lunch", "dinner",
        "rice", "dal", "sabzi", "haldiram snack", "pizza", "burger",
        "bakery", "confectionery", "sweet shop", "mithai",
    ],
    "Transport": [
        # Self-referential
        "transport", "transportation", "commute", "commuting", "travel expense",
        # Apps & operators
        "uber", "ola cab", "rapido cab", "blusmart cab", "yulu transport",
        "bounce transport", "vogo transport", "namma yatri auto",
        "bmtc bus", "best bus", "dtc bus", "ksrtc bus", "tsrtc bus",
        "redbus", "irctc", "metro", "train", "makemytrip",
        # Generic
        "petrol", "diesel", "fuel", "toll", "parking", "cab", "fare", "pass",
        "auto", "bus", "taxi",
    ],
    "Bills": [
        # Self-referential
        "bill", "bills", "utility", "utilities", "payment", "recharge",
        # Providers
        "electricity bill", "water", "gas bill", "internet", "broadband",
        "airtel", "jio", "bsnl", "vodafone", "rent", "maintenance",
        "society", "housekeeping", "act broadband", "hathway internet",
        "tata sky bill", "dish tv bill", "bill payment",
        "bescom", "msedcl", "bses", "tpddl", "igl", "mgl", "adani gas",
        # Bank narration patterns
        "neft", "rtgs", "imps", "emi", "loan emi", "insurance premium",
    ],
    "Entertainment": [
        # Self-referential
        "entertainment", "fun", "leisure",
        # Streaming
        "netflix entertainment", "hotstar entertainment", "prime video entertainment",
        "apple tv entertainment", "zee5 entertainment", "sonyliv entertainment",
        "jiocinema entertainment", "mxplayer entertainment", "voot entertainment",
        "altbalaji entertainment", "spotify music", "apple music",
        "jiosaavn music", "gaana music", "wynk music",
        # Cinemas & events
        "pvr cinema", "inox cinema", "cinepolis cinema",
        "bookmyshow event", "steam game", "playstation game", "xbox game",
        "ea game", "epic games game",
        "movie", "cinema", "concert", "event", "game", "gaming",
    ],
    "Health": [
        # Self-referential
        "health", "medical", "wellness", "fitness",
        # Pharmacies & doctors
        "apollopharmacy medicine", "medplus pharmacy", "1mg pharmacy",
        "netmeds pharmacy", "pharmeasy pharmacy", "practo doctor",
        "lybrate doctor", "cultfit health", "gym health",
        "pharmacy", "medicine", "hospital", "clinic", "doctor",
        "lab", "diagnostics", "healthians", "gym",
    ],
    "Shopping": [
        # Self-referential
        "shopping", "purchase", "retail", "store", "mart", "mall",
        # Online & offline
        "amazon shopping", "flipkart shopping", "myntra clothing",
        "ajio clothing", "nykaa shopping", "meesho clothing",
        "snapdeal shopping", "westside clothing", "pantaloons clothing",
        "max fashion clothing", "lifestyle clothing", "shoppers stop clothing",
        "zara clothing", "h&m", "mango clothing", "uniqlo clothing",
        "gap clothing", "marks and spencer clothing",
        "forever21 clothing", "levis clothing", "puma shoes",
        "nike shoes", "adidas shoes", "reebok shoes", "skechers shoes",
        "bata shoes", "woodland shoes", "superdry clothing",
        "us polo apparel", "tommy hilfiger clothing", "calvin klein clothing",
        "gucci shopping", "louis vuitton shopping", "chanel shopping",
        "burberry clothing", "central mall clothing",
        "clothing", "shoes", "apparel", "dmart",
        # Bank narration
        "pos debit", "pos purchase", "card purchase", "online purchase",
    ],
    "Travel": [
        # Self-referential
        "travel", "vacation", "holiday trip", "trip expense",
        # Platforms & airlines
        "oyo hotel", "treebo hotel", "fabhotel hotel", "zostel hotel",
        "airbnb hotel", "goibibo flight", "ixigo flight", "yatra flight",
        "cleartrip flight", "airindia flight", "indigo flight",
        "spicejet flight", "goair flight", "akasa air flight",
        "vistara flight",
        "hotel", "flight", "holiday", "tourism", "visa", "resort",
    ],
    "Education": [
        # Self-referential
        "education", "learning", "course", "training",
        # Platforms
        "udemy education", "coursera education", "byju education",
        "unacademy education", "vedantu education", "toppr education",
        "khan academy education", "duolingo education", "classplus education",
        "great learning education", "upgrad education", "simplilearn education",
        "scaler education",
        "books", "stationery", "school", "college", "tuition", "fees", "exam",
    ],
    "Misc": [],
}


# Non-essential categories that trigger impulsive flag consideration
NON_ESSENTIAL: set[str] = {
    "Entertainment", "Shopping", "Travel",
}

HIGH_SPEND_THRESHOLD: dict[str, float] = {
    "Entertainment": 500,
    "Shopping": 2000,
    "Food": 800,
    "Travel": 5000,
}

LATE_NIGHT_START = 22
LATE_NIGHT_END = 5


def _expand_aliases(text: str) -> str:
    """Replace known brand abbreviations with their canonical names."""
    # Try longest alias first to avoid partial replacements
    for alias in sorted(BRAND_ALIASES, key=len, reverse=True):
        # Match as a whole word or at start/end of string
        pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            return re.sub(pattern, BRAND_ALIASES[alias], text, count=1)
    return text


def categorize(description: str) -> str:
    """Return the best matching category for a merchant/description string."""
    text = description.lower().strip()
    text = _expand_aliases(text)          # expand aliases first

    for category, keywords in CATEGORY_RULES.items():
        if category == "Misc":
            continue
        for kw in keywords:
            if kw in text:
                return category
    return "Misc"


def is_impulsive(
    category: str,
    amount: float,
    transaction_date: date,
    received_at: datetime | None = None,
) -> tuple[bool, str]:
    """
    Returns (flag: bool, reason: str).

    Rules (any one match → impulsive):
    1. Non-essential category AND amount exceeds per-category threshold.
    2. Late night purchase (10 PM – 5 AM) of a non-essential item.
    3. Weekend non-essential purchase above ₹1 000.
    """
    if category not in NON_ESSENTIAL:
        return False, ""

    reasons: list[str] = []

    threshold = HIGH_SPEND_THRESHOLD.get(category, 1500)
    if amount >= threshold:
        reasons.append(
            f"High spend of ₹{amount:.0f} in non-essential category '{category}' "
            f"(threshold ₹{threshold:.0f})"
        )

    if received_at:
        hour = received_at.hour
        if hour >= LATE_NIGHT_START or hour < LATE_NIGHT_END:
            reasons.append(f"Late-night purchase at {received_at.strftime('%H:%M')}")

    weekday = transaction_date.weekday()
    if weekday >= 5 and amount >= 1000:
        reasons.append(f"Weekend non-essential purchase of ₹{amount:.0f}")

    if reasons:
        return True, "; ".join(reasons)
    return False, ""
