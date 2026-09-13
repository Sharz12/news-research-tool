from datetime import datetime, timezone

from src.export.reports import (
    build_articles_csv,
    build_research_report,
)
from src.news.models import NewsArticle


def create_test_articles():
    """Create test articles for export tests."""

    return [
        NewsArticle(
            title="Nvidia expands AI strategy",
            description=(
                "Nvidia announced a new AI initiative."
            ),
            content=(
                "Nvidia is expanding its AI capabilities."
            ),
            source_name="Example News",
            author="Test Reporter",
            url="https://example.com/article-1",
            image_url=None,
            published_at=datetime(
                2026,
                9,
                10,
                10,
                0,
                tzinfo=timezone.utc,
            ),
        ),
        NewsArticle(
            title="AI market continues to grow",
            description=(
                "The AI market continues to expand."
            ),
            content=(
                "Companies are investing in AI infrastructure."
            ),
            source_name="Tech News",
            author="Another Reporter",
            url="https://example.com/article-2",
            image_url=None,
            published_at=datetime(
                2026,
                9,
                11,
                12,
                30,
                tzinfo=timezone.utc,
            ),
        ),
    ]


def test_build_research_report_contains_metadata():

    articles = create_test_articles()

    report = build_research_report(
        query="Nvidia AI",
        language="English",
        period_label="Last 30 days",
        articles=articles,
        summary="Nvidia is expanding its AI strategy.",
    )

    assert "NEWS RESEARCH REPORT" in report
    assert "Research Query: Nvidia AI" in report
    assert "Output Language: English" in report
    assert "Research Period: Last 30 days" in report
    assert "Articles Analyzed: 2" in report
    assert "Sources: 2" in report


def test_build_research_report_contains_summary():

    articles = create_test_articles()

    report = build_research_report(
        query="Nvidia AI",
        language="Hindi",
        period_label="All available history",
        articles=articles,
        summary="Nvidia is expanding its AI strategy.",
    )

    assert "AI RESEARCH SUMMARY" in report
    assert (
        "Nvidia is expanding its AI strategy."
        in report
    )


def test_build_research_report_contains_articles():

    articles = create_test_articles()

    report = build_research_report(
        query="Nvidia AI",
        language="English",
        period_label="All available history",
        articles=articles,
        summary="Research summary.",
    )

    assert (
        "Nvidia expands AI strategy"
        in report
    )

    assert (
        "AI market continues to grow"
        in report
    )

    assert "Example News" in report
    assert "Tech News" in report

    assert (
        "https://example.com/article-1"
        in report
    )

    assert (
        "https://example.com/article-2"
        in report
    )


def test_build_articles_csv_contains_headers():

    articles = create_test_articles()

    csv_content = build_articles_csv(
        articles
    )

    first_line = csv_content.splitlines()[0]

    assert first_line == (
        "Title,Source,Published,Description,URL"
    )


def test_build_articles_csv_contains_articles():

    articles = create_test_articles()

    csv_content = build_articles_csv(
        articles
    )

    assert (
        "Nvidia expands AI strategy"
        in csv_content
    )

    assert "Example News" in csv_content

    assert (
        "https://example.com/article-1"
        in csv_content
    )

    assert (
        "AI market continues to grow"
        in csv_content
    )

    assert "Tech News" in csv_content