import pytest

from src.pipeline.research import ResearchPipeline
from src.news.models import NewsArticle


class FakeNewsClient:
    def search(self, query, page_size, days_back):
        assert query == "Nvidia AI"
        assert page_size == 10
        assert days_back == 7

        return [
            NewsArticle(
                title="Nvidia expands AI infrastructure",
                description="Nvidia reports strong demand for AI infrastructure.",
                content="Nvidia announced additional AI infrastructure investments.",
                source_name="Example News",
                author="Test Author",
                url="https://example.com/nvidia",
                published_at="2026-08-30T10:00:00Z",
            )
        ]


class FakeLLMClient:
    def invoke(self, prompt):
        assert "Nvidia AI" in prompt
        assert "Nvidia expands AI infrastructure" in prompt
        assert "strong demand for AI infrastructure" in prompt

        return "Nvidia continues to benefit from strong AI infrastructure demand."


def test_research_pipeline_returns_result():
    pipeline = ResearchPipeline(
        news_client=FakeNewsClient(),
        llm_client=FakeLLMClient(),
    )

    result = pipeline.research("Nvidia AI")

    assert result.query == "Nvidia AI"
    assert len(result.articles) == 1
    assert result.articles[0].title == "Nvidia expands AI infrastructure"
    assert (
        result.summary
        == "Nvidia continues to benefit from strong AI infrastructure demand."
    )


def test_empty_query_is_rejected():
    pipeline = ResearchPipeline(
        news_client=FakeNewsClient(),
        llm_client=FakeLLMClient(),
    )

    with pytest.raises(ValueError, match="Research query cannot be empty"):
        pipeline.research("   ")


def test_no_articles_returns_safe_result():
    class EmptyNewsClient:
        def search(self, query, page_size, days_back):
            return []

    pipeline = ResearchPipeline(
        news_client=EmptyNewsClient(),
        llm_client=FakeLLMClient(),
    )

    result = pipeline.research("Unknown company")

    assert result.query == "Unknown company"
    assert result.articles == []
    assert result.summary == "No relevant news articles were found."


def test_build_prompt_contains_article_information():
    article = NewsArticle(
        title="AI market growth",
        description="AI adoption continues to grow.",
        content="Businesses are increasing AI investments.",
        source_name="Example News",
        author="Test Author",
        url="https://example.com/ai",
        published_at="2026-08-30T10:00:00Z",
    )

    prompt = ResearchPipeline._build_prompt(
        "AI market",
        [article],
    )

    assert "AI market" in prompt
    assert "AI market growth" in prompt
    assert "AI adoption continues to grow." in prompt
    assert "Businesses are increasing AI investments." in prompt
    assert "Example News" in prompt