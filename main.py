from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

app = FastAPI(title="Quantum Terminal Engine", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BrokerConfig(BaseModel):
    api_key: str
    api_secret: str
    broker_name: str = "CoinDCX"

class EnginePayload(BaseModel):
    asset: str
    custom_logic: str
    market_structure: str

system_state = {
    "status": "Live",
    "mode": "Simulation",
    "broker_connected": False
}

@app.get("/", response_class=HTMLResponse)
def home():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Error: index.html not found in repository root.</h3>"

@app.post("/api/broker/connect")
def connect_broker(config: BrokerConfig):
    if len(config.api_key) < 10 or len(config.api_secret) < 10:
        raise HTTPException(status_code=400, detail="Invalid API Keys")
    system_state["broker_connected"] = True
    return {
        "status": "Success",
        "message": f"{config.broker_name} Connected Successfully.",
        "mode": system_state["mode"]
    }

@app.post("/api/engine/evaluate")
def evaluate_market(payload: EnginePayload):
    return {
        "asset": payload.asset,
        "action": "WAITING_FOR_TRIGGER",
        "analyzed_logic": payload.custom_logic,
        "ai_context": payload.market_structure,
        "system_message": "Logic parsed. Monitoring live data streams..."
    }

@app.get("/api/system/status")
def get_status():
    return system_state
  
