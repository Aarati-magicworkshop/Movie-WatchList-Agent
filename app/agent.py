
from __future__ import annotations
from httpx import AsyncClient
from typing import Optional, List
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from pydantic import BaseModel
from .schemas import Movie, AgentReply, MovieIn
from . import storage

GROQ_API_KEY="YOUR_GROQ_API_KEY"
MODEL="meta-llama/llama-4-scout-17b-16e-instruct"


class Deps(BaseModel):
    pass 

custom_http_client = AsyncClient(timeout=15)
model = GroqModel(
    MODEL,
    provider=GroqProvider(api_key=GROQ_API_KEY, http_client=custom_http_client),
)

agent = Agent[Deps, AgentReply](
    model,
    # api_key=GROQ_API_KEY,
    # provider=GroqProvider(api_key=GROQ_API_KEY),
    deps_type=Deps,
    output_type=AgentReply,
    system_prompt=(
        "You are intellegent movie watchlist assistant. "
        "You have access to the following tools: add_movie, list_movies, mark_watched, stats. "
        "⚠️ IMPORTANT: You must ALWAYS call one of these tools to take any action. "
        "For the tool `mark_watched`, always pass `movie_id` as a pure integer (e.g., 1), never a string."
        "Never just write the answer yourself. "
        "For example:\n"
        "- To add a movie, call add_movie(title=..., year=..., genre=..., rating=...)\n"
        "- To list movies, call list_movies(...)\n"
        "- To mark watched, call mark_watched(id=int)\n"
        "- To show stats, call stats()\n"

    )
)


@agent.tool
def add_movie(ctx: RunContext[Deps], movie: MovieIn) -> Movie:
    m = storage.add_movie(title=movie.title, year=movie.year, genre=movie.genre, rating=movie.rating)
    return Movie.model_validate(m)


@agent.tool
def list_movies(ctx: RunContext[Deps],watched: Optional[str] = None, genre: Optional[str] = None, year_after: Optional[int] = None) -> List[Movie]:
    rows = storage.list_movies(watched=watched, genre=genre, year_after=year_after)
    return [Movie.model_validate(r) for r in rows]


@agent.tool
def mark_watched(ctx: RunContext[Deps], movie_id: int | str) -> Movie:
    if isinstance(movie_id, str):
        try:
            movie_id = int(movie_id)
        except ValueError:
            raise ValueError(f"Invalid movie_id: {movie_id}")

    m = storage.mark_watched(movie_id)
    return Movie.model_validate(m)



@agent.tool
def stats(ctx: RunContext[Deps]) -> dict:
    stats_summary = storage.compute_stats()

    all_movies = storage.list_movies()  
    movies_data = [Movie.model_validate(m) for m in all_movies]

    return {
        "stats": stats_summary,
        "movies": movies_data,
        "message": (
            f"Your stats are: total movies = {stats_summary['total']}, "
            f"watched = {stats_summary['watched']}, "
            f"unwatched = {stats_summary['unwatched']}. "
            f"Genre distribution: " + ", ".join(f"{k} = {v}" for k, v in stats_summary['by_genre'].items())
        )
    }

async def run_agent(message: str) -> AgentReply:
    result = await agent.run(message, deps=Deps())
    return result.output


