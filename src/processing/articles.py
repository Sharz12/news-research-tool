import re

from src.news.models import NewsArticle


DEFAULT_MAX_CHARS = 4000


def clean_text(text: str | None) -> str:
    """Normalize whitespace in article text."""

    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip()


def truncate_text(
    text: str,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> str:
    """Limit text length while preserving complete input when possible."""

    if max_chars < 1:
        raise ValueError("max_chars must be greater than 0.")

    text = clean_text(text)

    if len(text) <= max_chars:
        return text

    return text[:max_chars].rstrip() + "..."


def format_article(
    article: NewsArticle,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> str:
    """Convert a NewsArticle into clean LLM-ready text."""

    description = clean_text(article.description)
    content = clean_text(article.content)

    article_body = truncate_text(
        content or description or "No article content available.",
        max_chars,
    )

    return (
        f"Title: {clean_text(article.title)}\n"
        f"Source: {clean_text(article.source_name)}\n"
        f"Published: {article.published_at}\n"
        f"Description: {description or 'N/A'}\n"
        f"Article: {article_body}"
    )


def format_articles(
    articles: list[NewsArticle],
    max_chars: int = DEFAULT_MAX_CHARS,
) -> str:
    """Format multiple articles into a single LLM context."""

    if not articles:
        return ""

    return "\n\n---\n\n".join(
        format_article(article, max_chars=max_chars)
        for article in articles
    )