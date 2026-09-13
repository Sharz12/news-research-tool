import csv
import io

from src.news.models import NewsArticle


def build_research_report(
    query: str,
    language: str,
    period_label: str,
    articles: list[NewsArticle],
    summary: str,
) -> str:
    """
    Build a plain-text research report for download.
    """

    unique_sources = len(
        {
            article.source_name
            for article in articles
        }
    )

    lines = [
        "NEWS RESEARCH REPORT",
        "====================",
        "",
        f"Research Query: {query}",
        f"Output Language: {language}",
        f"Research Period: {period_label}",
        f"Articles Analyzed: {len(articles)}",
        f"Sources: {unique_sources}",
        "",
        "----------------------------------------",
        "AI RESEARCH SUMMARY",
        "----------------------------------------",
        "",
        summary.strip(),
        "",
        "----------------------------------------",
        "SOURCE ARTICLES",
        "----------------------------------------",
        "",
    ]

    for index, article in enumerate(
        articles,
        start=1,
    ):
        lines.extend(
            [
                f"{index}. {article.title}",
                f"Source: {article.source_name}",
                (
                    "Published: "
                    f"{article.published_at.strftime('%d %b %Y, %H:%M')}"
                ),
                f"URL: {article.url}",
                (
                    "Description: "
                    f"{article.description or 'N/A'}"
                ),
                "",
            ]
        )

    return "\n".join(lines).strip()


def build_articles_csv(
    articles: list[NewsArticle],
) -> str:
    """
    Build CSV content containing the retrieved articles.
    """

    output = io.StringIO(
        newline="",
    )

    writer = csv.writer(
        output,
    )

    writer.writerow(
        [
            "Title",
            "Source",
            "Published",
            "Description",
            "URL",
        ]
    )

    for article in articles:
        writer.writerow(
            [
                article.title,
                article.source_name,
                article.published_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                article.description or "",
                str(article.url),
            ]
        )

    return output.getvalue()