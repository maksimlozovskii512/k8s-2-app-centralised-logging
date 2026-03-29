import os
import requests
from fastapi import FastAPI

app = FastAPI()

API_A_URL = os.getenv("API_A_URL", "http://api-a")

@app.get("/")
def root():
    r = requests.get(f"{API_A_URL}")
    return {
        "service": "B",
        "calls": API_A_URL,
        "response_from_a": r.json()
    }