from src.news.models import NewsArticle
from src.processing.articles import (
    clean_text,
    format_article,
    format_articles,
    truncate_text,
)


def make_article(
    description="AI adoption continues to grow.",
    content="Businesses are increasing AI investments.",
):
    return NewsArticle(
        title="AI Market Growth",
        description=description,
        content=content,
        source_name="Example News",
        author="Test Author",
        url="https://example.com/ai",
        published_at="2026-08-30T10:00:00Z",
    )


def test_clean_text_normalizes_whitespace():
    result = clean_text("  AI   is\n growing\t rapidly.  ")

    assert result == "AI is growing rapidly."


def test_clean_text_handles_empty_input():
    assert clean_text(None) == ""
    assert clean_text("") == ""


def test_truncate_text_limits_length():
    result = truncate_text("A" * 100, max_chars=20)

    assert len(result) == 23
    assert result.endswith("...")


def test_truncate_text_rejects_invalid_limit():
    try:
        truncate_text("test", max_chars=0)
        assert False
    except ValueError:
        pass


def test_format_article_contains_key_information():
    article = make_article()

    result = format_article(article)

    assert "AI Market Growth" in result
    assert "Example News" in result
    assert "AI adoption continues to grow." in result
    assert "Businesses are increasing AI investments." in result


def test_format_article_falls_back_to_description():
    article = make_article(
        description="AI adoption continues to grow.",
        content=None,
    )

    result = format_article(article)

    assert "AI adoption continues to grow." in result


def test_format_articles_combines_multiple_articles():
    articles = [
        make_article(),
        make_article(
            description="Cloud spending is increasing.",
            content="Companies continue investing in cloud infrastructure.",
        ),
    ]

    result = format_articles(articles)

    assert "AI Market Growth" in result
    assert "Example News" in result
    assert "AI adoption continues to grow." in result
    assert "Businesses are increasing AI investments." in result


def test_format_articles_handles_empty_list():
    assert format_articles([]) == ""