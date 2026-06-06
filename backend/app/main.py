# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import run_support_copilot
from database import init_db
from rag import ingest_policies
import os

app = FastAPI(title="AI Customer Support Agentic Backend", version="1.0")

# Input structural requirement configuration
class TicketPayload(BaseModel):
    customer_id: str
    ticket_text: str

@app.on_event("startup")
def startup_event():
    """Runs automated environmental initialization checks on launch."""
    print("Initializing databases and background indexers...")
    init_db()          # Rebuilds our SQLite mock data tables
    ingest_policies()  # Generates our local Chroma vector RAG matrix

@app.get("/")
def read_root():
    return {"status": "online", "message": "Agentic API Copilot engine is listening."}

@app.post("/api/tickets/process")
async def process_ticket(payload: TicketPayload):
    """Processes incoming support tickets using our unified agentic workflow."""
    try:
        if not payload.customer_id or not payload.ticket_text:
            raise HTTPException(status_code=400, detail="Missing customer_id or ticket_text parameters.")
            
        result = run_support_copilot(payload.customer_id, payload.ticket_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Fire up the server locally on port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)