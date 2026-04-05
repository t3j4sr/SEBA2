import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv("SEBA/.env")
gemini_key = os.environ.get("GEMINI_API_KEY", "")

async def test_gemini():
    print(f"Testing Gemini API config...")
    if not gemini_key:
        print("GEMINI_API_KEY is missing from environment.")
        return

    body = {
        "system_instruction": {
            "parts": [{"text": "You are a helpful assistant."}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": "Hello, are you there?"}]}
        ]
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
    
    async with httpx.AsyncClient(timeout=30) as client:
        print("Sending request...")
        resp = await client.post(url, json=body)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.text}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
