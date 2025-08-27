
from __future__ import annotations
import json, os
from typing import List, Dict, Any, Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "movies.json")

def _load() -> Dict[str, Any]:
    if not os.path.exists(DATA_PATH):
        return {"movies": [], "next_id": 1}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_movie(title: str, year: int | None, genre: str | None, rating: float | None) -> Dict[str, Any]:
    data = _load()
    m = {
        "id": data.get("next_id", 1),
        "title": title,
        "year": year,
        "genre": genre,
        "rating": rating,
        "watched": "no",
    }
    data["movies"].append(m)
    data["next_id"] = m["id"] + 1
    _save(data)
    return m

def list_movies(watched: str | None = None, genre: str | None = None, year_after: int | None = None) -> List[Dict[str, Any]]:
    data = _load()
    res = data["movies"]
    if watched in {"yes","no"}:
        res = [m for m in res if m.get("watched") == watched]
    if genre:
        g = genre.strip().lower()
        res = [m for m in res if (m.get("genre") or "").lower() == g]
    if year_after is not None:
        res = [m for m in res if (m.get("year") or 0) > year_after]
    return sorted(res, key=lambda m: ((m.get("watched")=="no"), (m.get("rating") or 0), (m.get("year") or 0)), reverse=True)

def mark_watched(movie_id: int) -> Dict[str, Any]:
    data = _load()
    for m in data["movies"]:
        if m["id"] == int(movie_id):
            m["watched"] = "yes"
            _save(data)
            return m
    raise ValueError(f"No movie with id={movie_id}")

def compute_stats() -> Dict[str, Any]:
    data = _load()
    total = len(data["movies"])
    watched = sum(1 for m in data["movies"] if m.get("watched") == "yes")
    genres = {}
    for m in data["movies"]:
        g = (m.get("genre") or "unknown").lower()
        genres[g] = genres.get(g, 0) + 1
    return {"total": total, "watched": watched, "unwatched": total - watched, "by_genre": genres}

