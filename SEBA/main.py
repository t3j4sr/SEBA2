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
    """Proxy endpoint for Groq API – translates seamlessly from frontend Gemini format."""
    body = await request.json()
    groq_key = os.environ.get("GROQ_API_KEY", "")
    if not groq_key:
        raise HTTPException(
            status_code=503,
            detail="Groq API key not configured. Add GROQ_API_KEY in Render."
        )
        
    messages = []
    
    if "system_instruction" in body:
        sys_text = body["system_instruction"]["parts"][0]["text"]
        messages.append({"role": "system", "content": sys_text})
        
    for msg in body.get("contents", []):
        role = "assistant" if msg.get("role") == "model" else "user"
        text = msg["parts"][0]["text"]
        messages.append({"role": role, "content": text})

    groq_body = {
        "model": "llama3-8b-8192",
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 1500
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {groq_key}"},
            json=groq_body
        )
    
    data = resp.json()
    if resp.status_code != 200:
        error_msg = data.get("error", {}).get("message", "Unknown Groq API Error")
        raise HTTPException(status_code=502, detail=f"Groq API Error: {error_msg}")
        
    groq_text = data["choices"][0]["message"]["content"]
    
    return {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": groq_text}]
                }
            }
        ]
    }

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": "S.E.B.A Backend v2.0.0"}
