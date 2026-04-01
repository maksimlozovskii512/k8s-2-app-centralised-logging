from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()

REQUESTS = Counter("api_a_requests_total", "Requests to API A")

@app.get("/")
def root():
    REQUESTS.inc()
    return {"service": "A", "message": "hello from A"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")