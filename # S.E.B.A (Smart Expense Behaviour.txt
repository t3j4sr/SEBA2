# S.E.B.A (Smart Expense Behaviour Analyser) - Backend Implementation Plan

The objective is to build a robust, scalable backend for an automated expense tracker that requires **zero manual input** from the user. The system will passively track expenses using SMS data streams and bank statement parsing, categorizing transactions and deriving behavioral analytics (such as identifying impulsive purchases).

## User Review Required

> [!IMPORTANT]
> The backend will be designed to integrate with **Supabase** (PostgreSQL database and potentially Auth if the frontend uses it). We will use free, open-source models or free-tier APIs for NLP/Categorization. Please review the updated architecture below.

## Architecture & Tech Stack

- **Framework**: Python (FastAPI) - *Python is essential for efficient NLP, RegEx, and data processing required for parsing statements and SMS.*
- **Database Backend (BaaS)**: **Supabase** (PostgreSQL). The backend will interact with Supabase using the `supabase-py` client or direct async pg drivers.
- **AI/ML & NLP (Free)**: 
  - **Regex Engine**: Highly optimized custom regular expressions for standard bank SMS and statement formats.
  - **Categorization & Intelligence**: Hugging Face Inference API (free tier) for zero-shot classification (e.g., `facebook/bart-large-mnli`), or a local lightweight model like `distilbert` using `transformers`. For identifying "impulsive" purchases, we can use a combination of rule-based logic (time of day, category, frequency) and ML classification.
- **Hosting (Actionable for End Users)**: The FastAPI service can be dockerized and hosted on Render or Hugging Face Spaces (free tiers) for practical implementation.

## Proposed Features & Modules

### 1. Ingestion Engine
Handles incoming transaction data. Designed to accept dummy/Kaggle data for the demo, but structured for real-world API consumption.

- **Bank Statement Parser**: 
  - `POST /upload/statement` (accepts PDF/CSV).
  - Uses `pdfplumber` or `pandas` (for CSVs) to extract tabular data reliably.
- **SMS Sync API**: 
  - `POST /sync/sms` (accepts a list/JSON array of SMS text strings).

### 2. Processing & Categorization Layer
The core intelligence engine.

- **Extraction Logic**:
  - Uses precise Regex to pull **Amount**, **Merchant**, **Date**, and **Type** (Credit/Debit) from raw text.
- **Behavioral Categorization (Free AI)**:
  - Categorizes into standard buckets (Food, Rent, Travel, etc.).
  - **Impulsive Purchase Identifier**: Flags transactions as "Impulsive" based on heuristics:
    - *Timing*: Late night weekend purchases.
    - *Category*: Non-essentials (Gaming, Luxury, Food Delivery) exceeding normal averages.
    - *Pattern*: Multiple high-frequency purchases in a short span.

### 3. Analytics & Endpoints
Provides the data required by the frontend dashboard. (Since the frontend handles login, these endpoints will assume a `user_id` is passed via a secure header or JWT from Supabase).

- **Endpoints**:
  - `GET /analytics/dashboard/{user_id}` (Aggregated summary, total spend, budget vs actual).
  - `GET /analytics/impulsive/{user_id}` (List of flagged impulsive transactions and the rationale).
  - `GET /transactions/{user_id}` (Paginated list of all parsed and categorized transactions).

## Data Schema (Supabase / PostgreSQL)

- **Users**: Handled by frontend via Supabase Auth.
- **Transactions**: `id`, `user_id` (UUID from Supabase Auth), `amount`, `date`, `merchant`, `category`, `is_impulsive` (Boolean), `source` (SMS/Statement), `raw_text`

## Next Steps / Execution Phase

If this plan is approved:
1. I will set up the FastAPI project structure.
2. Develop the Regex-based SMS and CSV/PDF parsers.
3. Integrate a free Hugging Face model / Rule engine for categorization and impulsive behavior detection.
4. Set up the `supabase-py` client to write parsed data.
5. Create a script to ingest a dummy dataset (e.g., from Kaggle) to populate the database for the demo.

Do you approve this updated plan?
