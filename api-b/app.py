import os
import requests
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest

app = FastAPI()

API_A_URL = os.getenv("API_A_URL", "http://api-a")

REQUESTS = Counter("api_b_requests_total", "Requests to API B")
UPSTREAM_ERRORS = Counter("api_b_upstream_errors_total", "Errors calling API A")

@app.get("/")
def root():
    REQUESTS.inc()

    try:
        r = requests.get(API_A_URL, timeout=2)
        r.raise_for_status()
        data = r.json()
    except Exception:
        UPSTREAM_ERRORS.inc()
        data = {"error": "failed to reach api-a"}

    return {
        "service": "B",
        "calls": API_A_URL,
        "response_from_a": data
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")