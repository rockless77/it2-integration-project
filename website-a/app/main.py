import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("website-a")

INTEGRATION_URL = os.getenv("INTEGRATION_URL", "http://integration:8000/api/send")
INTEGRATION_API_KEY = os.getenv("INTEGRATION_API_KEY", "a_to_integration_key")

app = FastAPI()

class IncomingUser(BaseModel):
    id: int
    name: str
    phone: str
    joined_at: str

@app.post("/api/send")
def send_to_integration(data: IncomingUser, request: Request):
    log.info(f"[A] Received user: {data.dict()} from host")

    payload = data.dict()
    headers = {"api-key": INTEGRATION_API_KEY}

    log.info(f"[A] Forwarding to integration: {INTEGRATION_URL}")

    resp = requests.post(INTEGRATION_URL, json=payload, headers=headers)

    log.info(f"[A] Integration responded: {resp.status_code} {resp.text}")

    return {"status": "OK", "forward_status": resp.status_code}


@app.get("/data")
def get_data():
    return "website-a OK"
