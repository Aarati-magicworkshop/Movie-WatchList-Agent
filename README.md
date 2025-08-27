
# Movie Watchlist —  Agent (PydanticAI + FastAPI)

A *simple* agentic API that manages a movie watchlist stored in a **JSON file**.

## How to run ?

```python
python -m venv movie
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\movie\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# run API
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs and try `/chat`.

## Try prompts
- "Add 'Inception' (2010) sci-fi rated 9/10."
- "List unwatched sci-fi movies after 2005."
- "Mark movie 1 as watched."
- "What are my stats?"


