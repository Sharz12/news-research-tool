import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

from config.settings import NEWSAPI_KEY
from src.news.exceptions import (
    NewsAPIAuthenticationError,
    NewsAPIRequestError,
    NewsAPIResponseError,
)
from src.news.models import NewsArticle

logger = logging.getLogger(__name__)


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

        try:
            logger.info(
                "Searching NewsAPI: query=%r page_size=%d days_back=%d",
                query,
                page_size,
                days_back,
            )

            response = self.client.get_everything(
                q=query,
                language="en",
                sort_by="relevancy",
                page_size=page_size,
                from_param=from_date.strftime("%Y-%m-%d"),
                to=to_date.strftime("%Y-%m-%d"),
            )

        except NewsAPIException as exc:
            logger.error("NewsAPI request failed: %s", exc)

            message = str(exc).lower()

            if any(
                keyword in message
                for keyword in (
                    "apikey",
                    "api key",
                    "unauthorized",
                    "authentication",
                )
            ):
                raise NewsAPIAuthenticationError(
                    "NewsAPI authentication failed."
                ) from exc

            raise NewsAPIRequestError(
                "NewsAPI request failed."
            ) from exc

        except Exception as exc:
            logger.exception("Unexpected NewsAPI error")

            raise NewsAPIRequestError(
                "Unexpected error while contacting NewsAPI."
            ) from exc

        if not isinstance(response, dict):
            raise NewsAPIResponseError(
                "NewsAPI returned an invalid response."
            )

        articles = response.get("articles")

        if not isinstance(articles, list):
            raise NewsAPIResponseError(
                "NewsAPI response does not contain a valid articles list."
            )

        logger.info(
            "NewsAPI returned %d raw articles.",
            len(articles),
        )

        return self._parse_articles(articles)

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

            except Exception as exc:
                logger.warning(
                    "Skipping invalid article: %s",
                    exc,
                )

        return validated_articles
    