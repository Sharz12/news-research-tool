from datetime import datetime, timezone

from src.news.models import NewsArticle
from src.pipeline.research import ResearchPipeline


def create_test_article():
    """Create a valid NewsArticle for pipeline tests."""

    return NewsArticle(
        title="Nvidia expands AI strategy",
        description=(
            "Nvidia announced a new AI initiative."
        ),
        content=(
            "Nvidia is expanding its AI capabilities "
            "and ecosystem."
        ),
        source_name="Example News",
        author="Test Reporter",
        url="https://example.com/article",
        image_url=None,
        published_at=datetime(
            2026,
            9,
            10,
            10,
            0,
            tzinfo=timezone.utc,
        ),
    )


class FakeNewsClient:
    """Fake NewsClient used for pipeline tests."""

    def search(
        self,
        query,
        page_size,
        days_back,
        max_articles,
    ):
        assert query == "Nvidia AI"
        assert page_size == 10
        assert days_back is None
        assert max_articles == 50

        return [
            create_test_article()
        ]


class FakeLLMClient:
    """Fake LLM client used for pipeline tests."""

    def invoke(self, prompt):
        assert "Nvidia AI" in prompt
        assert "Nvidia expands AI strategy" in prompt
        assert "Example News" in prompt

        return (
            "Executive Summary\n\n"
            "Nvidia is expanding its AI strategy.\n\n"
            "Key Developments\n\n"
            "1. Nvidia expanded its AI strategy.\n\n"
            "Companies / Markets Affected\n\n"
            "- Nvidia\n"
            "- AI infrastructure\n\n"
            "Business & Market Implications\n\n"
            "Reported fact:\n"
            "Nvidia expanded its AI strategy.\n\n"
            "Potential implication:\n"
            "The strategy could strengthen Nvidia's AI ecosystem.\n\n"
            "Risks / Contradictions\n\n"
            "No material contradiction was identified.\n\n"
            "Research Takeaway\n\n"
            "The available coverage indicates continued "
            "expansion of Nvidia's AI strategy."
        )


def test_research_pipeline_returns_result():

    pipeline = ResearchPipeline(
        news_client=FakeNewsClient(),
        llm_client=FakeLLMClient(),
    )

    result = pipeline.research(
        "Nvidia AI"
    )

    assert result.query == "Nvidia AI"

    assert len(
        result.articles
    ) == 1

    assert (
        result.articles[0].title
        == "Nvidia expands AI strategy"
    )

    assert (
        result.articles[0].source_name
        == "Example News"
    )

    assert (
        "Executive Summary"
        in result.summary
    )


class EmptyNewsClient:
    """Fake NewsClient that returns no articles."""

    def search(
        self,
        query,
        page_size,
        days_back,
        max_articles,
    ):
        return []


class UnexpectedLLMClient:
    """LLM client that should never be called."""

    def invoke(self, prompt):
        raise AssertionError(
            "LLM should not be called when no articles exist."
        )


def test_research_pipeline_rejects_empty_query():

    pipeline = ResearchPipeline(
        news_client=EmptyNewsClient(),
        llm_client=UnexpectedLLMClient(),
    )

    try:

        pipeline.research("")

        assert False, (
            "Expected ValueError for empty query."
        )

    except ValueError as exc:

        assert str(exc) == (
            "Research query cannot be empty."
        )


def test_no_articles_returns_safe_result():

    pipeline = ResearchPipeline(
        news_client=EmptyNewsClient(),
        llm_client=UnexpectedLLMClient(),
    )

    result = pipeline.research(
        "Unknown company"
    )

    assert result.query == "Unknown company"

    assert result.articles == []

    assert result.summary == (
        "No relevant news articles were found."
    )


def test_research_pipeline_builds_prompt():

    articles = [
        create_test_article()
    ]

    prompt = ResearchPipeline._build_prompt(
        "Nvidia AI",
        articles,
    )

    assert "Nvidia AI" in prompt

    assert (
        "Nvidia expands AI strategy"
        in prompt
    )

    assert "Example News" in prompt

    assert "Executive Summary" in prompt

    assert "Key Developments" in prompt

    assert (
        "Companies / Markets Affected"
        in prompt
    )

    assert (
        "Business & Market Implications"
        in prompt
    )

    assert (
        "Risks / Contradictions"
        in prompt
    )

    assert (
        "Research Takeaway"
        in prompt
    )


def test_clean_summary_removes_markdown_formatting():

    raw_summary = """
## Executive Summary

Nvidia announced a **12.9 billion** acquisition of
`Hugging Face`.

The company also launched *Personal AI Router*.

[The Verge](https://example.com)

### Key Developments

1. **Nvidia expanded its AI strategy.**
2. `Revenue increased significantly.`
"""

    cleaned = ResearchPipeline._clean_summary(
        raw_summary
    )

    assert "##" not in cleaned

    assert "###" not in cleaned

    assert "`" not in cleaned

    assert "**" not in cleaned

    assert "*" not in cleaned

    assert "[The Verge]" not in cleaned

    assert "12.9 billion" in cleaned

    assert "Hugging Face" in cleaned

    assert "Personal AI Router" in cleaned

    assert "The Verge" in cleaned


def test_clean_summary_preserves_research_structure():

    raw_summary = """
Executive Summary

Nvidia announced a major acquisition.

Key Developments

1. Nvidia announced the acquisition.

Companies / Markets Affected

- Nvidia
- AI infrastructure

Business & Market Implications

Reported fact:
Nvidia announced the transaction.

Potential implication:
The transaction could expand Nvidia's AI ecosystem.

Risks / Contradictions

No material contradiction was identified.

Research Takeaway

The available coverage indicates continued
expansion of Nvidia's AI strategy.
"""

    cleaned = ResearchPipeline._clean_summary(
        raw_summary
    )

    assert (
        "Executive Summary"
        in cleaned
    )

    assert (
        "Key Developments"
        in cleaned
    )

    assert (
        "Companies / Markets Affected"
        in cleaned
    )

    assert (
        "Business & Market Implications"
        in cleaned
    )

    assert (
        "Risks / Contradictions"
        in cleaned
    )

    assert (
        "Research Takeaway"
        in cleaned
    )