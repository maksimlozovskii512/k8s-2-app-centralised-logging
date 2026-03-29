from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"service": "A", "message": "hello from A"}

@app.get("/health")
def health():
    return {"status": "ok"}