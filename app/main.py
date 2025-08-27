
from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from .agent import run_agent

app = FastAPI(title="Movie Watchlist — Agent")

class ChatIn(BaseModel):
    message: str

@app.post("/chat")
async def chat(in_: ChatIn):
    reply = await run_agent(in_.message)
    return reply
