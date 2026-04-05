# S.E.B.A — Smart Expense Behaviour Analyser 🧠💸

A zero-manual-input expense tracking backend that passively ingests bank SMS messages and statements, categorizes transactions, and surfaces behavioural analytics including **impulsive purchase detection**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Python 3.11 + FastAPI |
| Database | Supabase (PostgreSQL) via `supabase-py` |
| Parsing | Custom Regex engine + pandas + pdfplumber |
| Categorization | Rule-based keyword engine (extendable to HuggingFace) |
| Hosting | Uvicorn (local) / Render / HuggingFace Spaces |

---

## Project Structure

```
SEBA/
├── main.py                  # FastAPI app entry point
├── seed.py                  # Demo data loader (reads middle_class_expenses.json)
├── schema.sql               # Run this in Supabase SQL Editor first!
├── requirements.txt
├── .env                     # Your credentials (never commit this)
├── .env.example             # Template
└── app/
    ├── db.py                # Supabase client singleton
    ├── models.py            # Pydantic request/response models
    ├── categorizer.py       # Category + impulsive detection engine
    ├── sms_parser.py        # Regex SMS parser
    ├── statement_parser.py  # CSV / PDF parser
    └── routers/
        ├── sync.py          # POST /sync/sms
        ├── upload.py        # POST /upload/statement
        ├── transactions.py  # GET  /transactions/{user_id}
        └── analytics.py     # GET  /analytics/dashboard|impulsive/{user_id}
```

---

## Setup

### 1. Create the Supabase table

Open **Supabase Dashboard → SQL Editor** and run the entire contents of `schema.sql`.

### 2. Configure environment

```bash
# The .env is already configured with your credentials.
# To check: cat .env
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Seed demo data

```bash
python seed.py
```

This reads `../middle_class_expenses.json` and inserts all transactions under the fixed demo user ID `00000000-0000-0000-0000-000000000001`.

### 5. Run the server

```bash
uvicorn main:app --reload
```

Server runs at: **http://127.0.0.1:8000**  
Interactive docs: **http://127.0.0.1:8000/docs**

---

## API Endpoints

### Ingestion

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/sync/sms` | Ingest a batch of raw SMS strings |
| `POST` | `/upload/statement` | Upload a CSV or PDF bank statement |

### Retrieval

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/transactions/{user_id}` | Paginated transaction list (supports `?category=Food&impulsive_only=true`) |
| `GET` | `/analytics/dashboard/{user_id}` | Total spend, per-category breakdown, monthly trend, top merchant |
| `GET` | `/analytics/impulsive/{user_id}` | All flagged impulsive transactions with reasoning |

### Quick test with demo data

```
GET http://127.0.0.1:8000/analytics/dashboard/00000000-0000-0000-0000-000000000001
GET http://127.0.0.1:8000/analytics/impulsive/00000000-0000-0000-0000-000000000001
GET http://127.0.0.1:8000/transactions/00000000-0000-0000-0000-000000000001
```

---

## Impulsive Purchase Detection Rules

A transaction is flagged as **impulsive** (is_impulsive = true) when **any** of the following are true:

| Rule | Condition |
|---|---|
| High Spend | Non-essential category (Entertainment/Shopping/Travel) exceeds category threshold |
| Late Night | Purchase in a non-essential category between 10 PM – 5 AM |
| Weekend Splurge | Non-essential weekend purchase above ₹1,000 |

The `impulse_reason` column stores a human-readable explanation for each flag.
