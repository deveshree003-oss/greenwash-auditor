import requests
from backend.core.config import NEWS_API_KEY

def fetch_news(company):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company,
        "apiKey": NEWS_API_KEY,
        "pageSize": 5
    }

    res = requests.get(url, params=params).json()

    articles = []
    for a in res.get("articles", []):
        articles.append({
            "title": a["title"],
            "description": a["description"]
        })

    return articles