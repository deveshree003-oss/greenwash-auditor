"""News agent: fetch and parse news corroboration for claims."""

from backend.app.tools.news_tool import fetch_news


class NewsAgent:
    def run(self, company):
        return fetch_news(company)