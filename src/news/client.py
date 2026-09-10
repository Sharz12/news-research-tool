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
        days_back: int | None = None,
        max_articles: int = 50,
    ) -> list[NewsArticle]:
        """
        Search NewsAPI and return validated, deduplicated articles.

        When days_back is None, no application-level date filter
        is applied. NewsAPI determines the available historical
        range according to the user's API plan.

        Pagination continues until either:
        - max_articles are collected, or
        - NewsAPI has no more results.
        """

        query = query.strip()

        if not query:
            raise ValueError(
                "Search query cannot be empty."
            )

        if not 1 <= page_size <= 100:
            raise ValueError(
                "page_size must be between 1 and 100."
            )

        if days_back is not None and days_back < 1:
            raise ValueError(
                "days_back must be at least 1 when provided."
            )

        if max_articles < 1:
            raise ValueError(
                "max_articles must be greater than 0."
            )

        logger.info(
            "Searching NewsAPI: query=%r page_size=%d "
            "days_back=%s max_articles=%d",
            query,
            page_size,
            days_back,
            max_articles,
        )

        request_params: dict[str, Any] = {
            "q": query,
            "language": "en",
            "sort_by": "relevancy",
            "page_size": page_size,
        }

        # Apply date filtering only when requested.
        if days_back is not None:
            to_date = datetime.now(timezone.utc)
            from_date = (
                to_date - timedelta(days=days_back)
            )

            request_params["from_param"] = (
                from_date.strftime("%Y-%m-%d")
            )

            request_params["to"] = (
                to_date.strftime("%Y-%m-%d")
            )

        collected_articles: list[NewsArticle] = []
        seen_urls: set[str] = set()

        page = 1

        while len(collected_articles) < max_articles:

            request_params["page"] = page

            logger.info(
                "Requesting NewsAPI page=%d",
                page,
            )

            try:
                response = self.client.get_everything(
                    **request_params
                )

            except NewsAPIException as exc:
                logger.error(
                    "NewsAPI request failed: %s",
                    exc,
                )

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
                logger.exception(
                    "Unexpected NewsAPI error."
                )

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
                    "NewsAPI response does not contain "
                    "a valid articles list."
                )

            total_results = response.get(
                "totalResults",
                0,
            )

            logger.info(
                "NewsAPI page=%d returned %d articles "
                "out of %s total results.",
                page,
                len(articles),
                total_results,
            )

            if not articles:
                break

            parsed_articles = self._parse_articles(
                articles
            )

            for article in parsed_articles:

                article_url = str(article.url)

                if article_url in seen_urls:
                    continue

                seen_urls.add(article_url)
                collected_articles.append(article)

                if len(collected_articles) >= max_articles:
                    break

            # Stop if NewsAPI has no additional pages.
            if len(articles) < page_size:
                break

            if isinstance(total_results, int):
                if page * page_size >= total_results:
                    break

            page += 1

        logger.info(
            "Collected %d unique articles.",
            len(collected_articles),
        )

        return collected_articles

    @staticmethod
    def _parse_articles(
        articles: list[dict[str, Any]],
    ) -> list[NewsArticle]:
        """Validate raw NewsAPI articles using Pydantic."""

        validated_articles: list[NewsArticle] = []

        for article in articles:

            try:
                source = article.get("source") or {}

                news_article = NewsArticle(
                    title=article.get("title") or "Untitled",
                    description=article.get("description"),
                    content=article.get("content"),
                    source_name=(
                        source.get("name")
                        or "Unknown"
                    ),
                    author=article.get("author"),
                    url=article.get("url"),
                    image_url=article.get("urlToImage"),
                    published_at=article.get("publishedAt"),
                )

                validated_articles.append(
                    news_article
                )

            except Exception as exc:
                logger.warning(
                    "Skipping invalid article: %s",
                    exc,
                )

        return validated_articles