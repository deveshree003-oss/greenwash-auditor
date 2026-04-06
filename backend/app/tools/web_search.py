"""Web / news search helper (placeholder implementation).

If `NEWS_API_KEY` is present in the environment this will attempt to
call NewsAPI.org; otherwise it returns an empty list. Swap in your
preferred search provider or connector as needed.
"""
import os
from typing import Any, Dict, List


def search(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Return a list of news hit dicts for `query`.

    Each hit is a dict with keys like `title`, `url`, `source`, and
    `publishedAt`. This is intentionally minimal and resilient.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return []

    try:
        import requests

        url = "https://newsapi.org/v2/everything"
        params = {"q": query, "pageSize": limit, "apiKey": api_key}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        hits: List[Dict[str, Any]] = []
        for a in data.get("articles", []):
            hits.append({
                "title": a.get("title"),
                "url": a.get("url"),
                "source": (a.get("source") or {}).get("name"),
                "publishedAt": a.get("publishedAt"),
                "summary": a.get("description"),
            })
        return hits
    except Exception:
        return []


def summarize_hits(hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return a compact summary for each hit (placeholder).

    Replace with an NLP summarizer or extractor as needed.
    """
    return [{"title": h.get("title"), "url": h.get("url")} for h in hits]
