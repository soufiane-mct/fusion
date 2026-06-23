from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory storage (acts like a DLQ database)
DLQ_STORAGE = []


class DLQMessage(BaseModel):
    original_prompt: str
    status: str


# =========================
# POST endpoint (receive DLQ messages)
# =========================
@app.post("/dlq/messages")
def receive_dlq_message(message: DLQMessage):
    DLQ_STORAGE.append(message.model_dump())
    return {
        "message": "stored in DLQ successfully",
        "data": message
    }


# =========================
# GET endpoint (view DLQ messages)
# =========================
@app.get("/dlq/messages")
def get_dlq_messages():
    return DLQ_STORAGE