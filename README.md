# SEBA- Smart Expense Behaviour Analyser 🧠💸

**SEBA- upload ur bank statement and get future predictions, personalized finance coach and much more.**

---

## 🏆 Competitive Analysis

*   **Behavioral Analysis**: Understands your spending patterns and identifies impulse buys based on time, day, and merchant.
*   **Future Prediction**: Forecasts upcoming fixed expenses (rent, bills, EMI) and potential variable splurge periods based on your unique history.
*   **Personalized AI Coach**: Chat with S.E.B.A., your AI finance assistant, for custom insights on your categories, savings potential, and habits.
*   **Credit Card Insights**: Visual tracking of credit card utilization.
*   **Tax Save Recs**: Get basic suggestions on tax-saving investments based on your current expense footprint.
*   **Zero Manual Entry**: Upload a bank statement (CSV/PDF) and the system completely auto-categorizes your transactions.

---

## 🛠 Tech Stack

*   **Hosting**: Render
*   **Database**: Supabase
*   **Backend**: FastAPI
*   **AI Engine**: Groq
*   **Parsing Engine**: pandas / pdfplumber

---

## 🚀 How to Use

**Web App Link:**  
**[https://seba2.onrender.com](https://seba2.onrender.com)**

*(Note: We also have the Android `.apk` file for mobile installations).*

**Dependencies (if running locally):**
```bash
pip install fastapi uvicorn pydantic python-multipart pdfplumber pandas supabase python-dotenv httpx
```

---

## 🗂 Project Folder Structure

```
SEBA/
├── main.py                  # FastAPI app entry point (Backend routing)
├── requirements.txt         # Dependencies
├── .env                     # Your credentials (Render & Supabase)
├── static/                  # Frontend Web App Folder
│   ├── index.html           # Main Dashboard (Upload & summary view)
│   ├── analytics.html       # Visual analytics & Behavioral insights
│   ├── predictions.html     # Future risk-day prediction calendar
│   ├── login.html           # Authentication UI
│   ├── crypto.html          # Crypto Space module
│   ├── health.html          # Financial health score module
│   └── chat-widget.js       # Floating AI chatbot logic
└── app/
    ├── db.py                # Supabase client singleton
    ├── models.py            # Data validation schemas
    ├── categorizer.py       # Auto-category + impulsive detection engine
    ├── statement_parser.py  # Bank statement (CSV/PDF) ingester
    └── routers/
        ├── auth.py          # Secure signup/login
        ├── upload.py        # Statement upload handling
        ├── transactions.py  # History retrieval
        └── analytics.py     # Aggregation & AI pattern generation
```
