from datetime import datetime, timedelta, timezone
from typing import Any

from newsapi import NewsApiClient

from config.settings import NEWSAPI_KEY
from src.news.models import NewsArticle


class NewsClient:
    """Client responsible for retrieving and validating news articles."""

    def __init__(self, api_key: str = NEWSAPI_KEY):
        self.client = NewsApiClient(api_key=api_key)

    def search(
        self,
        query: str,
        page_size: int = 20,
        days_back: int = 7,
    ) -> list[NewsArticle]:
        """Search NewsAPI and return validated articles."""

        query = query.strip()

        if not query:
            raise ValueError("Search query cannot be empty.")

        if not 1 <= page_size <= 100:
            raise ValueError("page_size must be between 1 and 100.")

        if days_back < 1:
            raise ValueError("days_back must be at least 1.")

        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=days_back)

        response = self.client.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",
            page_size=page_size,
            from_param=from_date.strftime("%Y-%m-%d"),
            to=to_date.strftime("%Y-%m-%d"),
        )

        return self._parse_articles(
            response.get("articles", [])
        )

    @staticmethod
    def _parse_articles(
        articles: list[dict[str, Any]],
    ) -> list[NewsArticle]:
        """Convert raw NewsAPI articles into validated NewsArticle objects."""

        validated_articles: list[NewsArticle] = []

        for article in articles:
            try:
                source = article.get("source") or {}

                news_article = NewsArticle(
                    title=article.get("title") or "Untitled",
                    description=article.get("description"),
                    content=article.get("content"),
                    source_name=source.get("name") or "Unknown",
                    author=article.get("author"),
                    url=article.get("url"),
                    image_url=article.get("urlToImage"),
                    published_at=article.get("publishedAt"),
                )

                validated_articles.append(news_article)

            except Exception:
                continue

        return validated_articles