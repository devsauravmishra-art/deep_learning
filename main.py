# main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Heartbeat Service", version="0.1.0")


@app.get("/heartbeat", response_class=JSONResponse, tags=["Health"])
async def heartbeat() -> dict:
    """
    Simple health‑check endpoint.
    Returns a JSON object confirming that the service is alive.
    """
    return {"status": "ok", "message": "Service is up and running"}
