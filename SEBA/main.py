from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os, httpx

from app.routers import transactions, analytics, upload, add, auth

app = FastAPI(
    title="S.E.B.A – Smart Expense Behaviour Analyser",
    description="Backend for manual expense tracking with behavioural analytics.",
    version="2.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

def _page(name: str):
    return FileResponse(os.path.join(static_dir, name))

@app.get("/", include_in_schema=False)
async def serve_landing(): return _page("landing.html")

@app.get("/home", include_in_schema=False)
async def serve_frontend(): return _page("index.html")

@app.get("/analytics", include_in_schema=False)
async def serve_analytics(): return _page("analytics.html")

@app.get("/predictions", include_in_schema=False)
async def serve_predictions(): return _page("predictions.html")


@app.get("/tax", include_in_schema=False)
async def serve_tax(): return _page("tax.html")

@app.get("/cards", include_in_schema=False)
async def serve_cards(): return _page("cards.html")

@app.get("/loans", include_in_schema=False)
async def serve_loans(): return _page("loans.html")

@app.get("/invest", include_in_schema=False)
async def serve_invest(): return _page("invest.html")

@app.get("/login", include_in_schema=False)
async def serve_login(): return _page("login.html")

@app.get("/welcome", include_in_schema=False)
async def serve_welcome(): return _page("welcome.html")

@app.get("/chat", include_in_schema=False)
async def serve_chat(): return _page("chat.html")

@app.get("/coach", include_in_schema=False)
async def serve_coach(): return _page("coach.html")

@app.get("/crypto", include_in_schema=False)
async def serve_crypto(): return _page("crypto.html")

app.include_router(add.router,          prefix="/add",          tags=["Add Spending"])
app.include_router(transactions.router, prefix="/transactions",  tags=["Transactions"])
app.include_router(analytics.router,    prefix="/analytics",     tags=["Analytics"])
app.include_router(upload.router,       prefix="/upload",        tags=["Import Statement"])
app.include_router(auth.router,         prefix="/auth",          tags=["Auth"])

@app.post("/chat/ai", tags=["AI Chat"])
async def ai_chat(request: Request):
    """Proxy endpoint for Gemini API – keeps the API key server-side."""
    body = await request.json()
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_key:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key not configured. Add GEMINI_API_KEY=your_key to the .env file."
        )
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}",
            json=body
        )
    
    data = resp.json()
    if resp.status_code != 200:
        error_msg = data.get("error", {}).get("message", "Unknown Google API Error")
        raise HTTPException(status_code=502, detail=f"Gemini API Error: {error_msg}")
        
    return data

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": "S.E.B.A Backend v2.0.0"}
