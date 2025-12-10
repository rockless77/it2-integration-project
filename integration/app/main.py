import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("integration")

app = FastAPI()

INCOMING_API_KEY = os.getenv("INCOMING_API_KEY", "a_to_integration_key")
WEBSITE_B_URL = os.getenv("WEBSITE_B_URL", "http://website-b:8000/api/receive")
WEBSITE_B_API_KEY = os.getenv("WEBSITE_B_API_KEY", "b_secret_key")

class IncomingUser(BaseModel):
    id: int
    name: str
    phone: str
    joined_at: str

def _get_key(req: Request):
    return req.headers.get("api-key")

@app.post("/api/send")
def forward_to_b(data: IncomingUser, request: Request):
    key = _get_key(request)

    log.info(f"[INT] Received user from A: {data.dict()} (API-key={key})")

    if key != INCOMING_API_KEY:
        log.warning("[INT] Invalid API key rejected")
        return {"status": "error", "message": "invalid incoming api key"}

    payload = data.dict()
    headers = {"API-Key": WEBSITE_B_API_KEY}

    log.info(f"[INT] Forwarding to B: {WEBSITE_B_URL} with payload {payload}")

    try:
        resp = requests.post(WEBSITE_B_URL, json=payload, headers=headers)
        log.info(f"[INT] B responded: {resp.status_code} {resp.text}")
        return {"status": "OK", "forward_status": resp.status_code}
    except Exception as e:
        log.error(f"[INT] Failed to forward to B: {e}")
        return {"status": "error", "forward_status": None}
