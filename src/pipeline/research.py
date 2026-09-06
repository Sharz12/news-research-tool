from dataclasses import dataclass

from src.llm.client import GroqClient
from src.news.client import NewsClient
from src.news.models import NewsArticle
from src.processing.articles import format_articles

@dataclass
class ResearchResult:
    """Result returned by the news research pipeline."""

    query: str
    articles: list[NewsArticle]
    summary: str


class ResearchPipeline:
    """Orchestrates news retrieval and LLM summarization."""

    def __init__(
        self,
        news_client: NewsClient | None = None,
        llm_client: GroqClient | None = None,
    ):
        self.news_client = news_client or NewsClient()
        self.llm_client = llm_client or GroqClient()

    def research(
        self,
        query: str,
        page_size: int = 10,
        days_back: int = 7,
    ) -> ResearchResult:
        """Retrieve relevant news and generate an overall summary."""

        query = query.strip()

        if not query:
            raise ValueError("Research query cannot be empty.")

        articles = self.news_client.search(
            query=query,
            page_size=page_size,
            days_back=days_back,
        )

        if not articles:
            return ResearchResult(
                query=query,
                articles=[],
                summary="No relevant news articles were found.",
            )

        prompt = self._build_prompt(query, articles)

        summary = self.llm_client.invoke(prompt)

        return ResearchResult(
            query=query,
            articles=articles,
            summary=summary,
        )

    @staticmethod
    def _build_prompt(
        query: str,
        articles: list[NewsArticle],
    ) -> str:
        """Build the research prompt sent to the LLM."""

        article_text = format_articles(articles)

        return f"""
You are an AI assistant helping an equity research analyst.

Given the user's research query and the provided news articles,
produce a concise, factual overall summary.

Focus on:
- The most important developments
- Companies, organizations, or markets affected
- Potential business or market implications
- Important differences or conflicting information between articles

Use only information supported by the provided articles.
Do not invent facts, numbers, events, or conclusions.

User Query:
{query}

News Articles:
{article_text}
""".strip()