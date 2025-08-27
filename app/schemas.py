
from __future__ import annotations
from typing import Optional, Literal, List
from pydantic import BaseModel, Field

Watched = Literal["yes","no"]

class MovieIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    year: Optional[int] = Field(None, ge=1888, le=2100)
    genre: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=10)

class Movie(BaseModel):
    id: int
    title: str
    year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = None
    watched: Watched = "no"

class AgentReply(BaseModel):
    message: str
    # message: Optional[str] = "Done."
    movies: Optional[List[Movie]] = None
    stats: Optional[dict] = None
