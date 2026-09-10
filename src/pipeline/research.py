import re
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
        self.news_client = (
            news_client or NewsClient()
        )

        self.llm_client = (
            llm_client or GroqClient()
        )

    def research(
        self,
        query: str,
        page_size: int = 10,
        days_back: int | None = None,
        max_articles: int = 50,
    ) -> ResearchResult:
        """
        Retrieve relevant news and generate an
        analyst-oriented research summary.
        """

        query = query.strip()

        if not query:
            raise ValueError(
                "Research query cannot be empty."
            )

        articles = self.news_client.search(
            query=query,
            page_size=page_size,
            days_back=days_back,
            max_articles=max_articles,
        )

        if not articles:
            return ResearchResult(
                query=query,
                articles=[],
                summary=(
                    "No relevant news articles were found."
                ),
            )

        prompt = self._build_prompt(
            query,
            articles,
        )

        raw_summary = self.llm_client.invoke(
            prompt
        )

        summary = self._clean_summary(
            raw_summary
        )

        return ResearchResult(
            query=query,
            articles=articles,
            summary=summary,
        )

    @staticmethod
    def _clean_summary(summary: str) -> str:
        """
        Convert an LLM response into safe, clean,
        presentation-neutral text.

        The LLM is not allowed to control the UI formatting.
        """

        if not summary:
            return ""

        cleaned = summary.strip()

        # -------------------------------------------------
        # Remove code fences.
        # -------------------------------------------------

        cleaned = re.sub(
            r"```(?:markdown|md|text|plain)?",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = cleaned.replace(
            "```",
            "",
        )

        # -------------------------------------------------
        # Remove inline code formatting.
        #
        # `12.9 billion`
        # ->
        # 12.9 billion
        # -------------------------------------------------

        cleaned = re.sub(
            r"`+([^`]+)`+",
            r"\1",
            cleaned,
        )

        # -------------------------------------------------
        # Remove Markdown links.
        #
        # [Nvidia](https://example.com)
        # ->
        # Nvidia
        # -------------------------------------------------

        cleaned = re.sub(
            r"\[([^\]]+)\]\([^)]+\)",
            r"\1",
            cleaned,
        )

        # -------------------------------------------------
        # Remove Markdown emphasis.
        #
        # **text**
        # *text*
        # __text__
        # _text_
        # ->
        # text
        # -------------------------------------------------

        cleaned = re.sub(
            r"\*\*(.*?)\*\*",
            r"\1",
            cleaned,
            flags=re.DOTALL,
        )

        cleaned = re.sub(
            r"__(.*?)__",
            r"\1",
            cleaned,
            flags=re.DOTALL,
        )

        cleaned = re.sub(
            r"\*(.*?)\*",
            r"\1",
            cleaned,
            flags=re.DOTALL,
        )

        cleaned = re.sub(
            r"_(.*?)_",
            r"\1",
            cleaned,
            flags=re.DOTALL,
        )

        # -------------------------------------------------
        # Remove remaining Markdown heading markers.
        # -------------------------------------------------

        cleaned_lines = []

        for line in cleaned.splitlines():

            line = re.sub(
                r"^\s*#{1,6}\s+",
                "",
                line,
            )

            cleaned_lines.append(
                line.rstrip()
            )

        cleaned = "\n".join(
            cleaned_lines
        )

        # -------------------------------------------------
        # Remove remaining formatting characters that
        # should never appear in our presentation-neutral
        # research output.
        # -------------------------------------------------

        cleaned = cleaned.replace(
            "`",
            "",
        )

        # -------------------------------------------------
        # Normalize excessive blank lines.
        # -------------------------------------------------

        cleaned = re.sub(
            r"\n{3,}",
            "\n\n",
            cleaned,
        )

        return cleaned.strip()

    @staticmethod
    def _build_prompt(
        query: str,
        articles: list[NewsArticle],
    ) -> str:
        """
        Build a structured research prompt for the LLM.
        """

        article_text = format_articles(
            articles
        )

        return f"""
You are an AI research assistant supporting an
equity research analyst.

Analyze the supplied news articles in relation to
the user's research query.

The application will handle all visual formatting.
Therefore, return clean plain text only.

USER RESEARCH QUERY:
{query}

SOURCE ARTICLES:
{article_text}

==================================================
ANALYSIS RULES
==================================================

1. Use ONLY information contained in the supplied
   source articles.

2. Do NOT invent facts, statistics, dates, financial
   figures, events, company statements, or market
   movements.

3. Clearly distinguish between reported facts and
   reasonable business or market implications.

4. When discussing implications, use cautious language
   such as "may", "could", "suggests", or "potentially".

5. If the sources disagree, explicitly identify the
   disagreement.

6. If there is insufficient evidence to support a
   conclusion, clearly state that.

7. Do not repeat the same information across sections.

8. Prioritize information that could matter to an
   equity research or business analyst.

9. Do not provide investment advice.

10. Do not recommend buying, selling, or holding
    any security.

==================================================
RESPONSE FORMAT
==================================================

Return EXACTLY these six section names:

Executive Summary

Key Developments

Companies / Markets Affected

Business & Market Implications

Risks / Contradictions

Research Takeaway

Do NOT use:

- Markdown headings
- Markdown bold
- Markdown italics
- Backticks
- Markdown links
- Code blocks

Do NOT place special formatting around numbers,
dates, financial figures, company names, or phrases.

==================================================
SECTION REQUIREMENTS
==================================================

Executive Summary

Write 2-4 concise sentences summarizing the most
important developments relevant to the research query.


Key Developments

Provide 3-6 numbered developments.

Each development should explain:
- What happened
- The company, organization, or market involved
- Why the development matters

Keep each point concise.


Companies / Markets Affected

List relevant companies, organizations, industries,
sectors, or markets.

Only include entities supported by the articles.


Business & Market Implications

Separate facts from interpretation.

Use:

Reported fact:
What the sources actually report.

Potential implication:
What this could reasonably mean for the business,
industry, or market.

Do not present speculation as fact.


Risks / Contradictions

Identify:
- Conflicting information
- Important uncertainties
- Risks mentioned by sources
- Missing information that limits the analysis

If no material contradiction is identified,
state that clearly.


Research Takeaway

Provide 2-3 concise sentences summarizing the
most important conclusion supported by the coverage.

The final takeaway must remain evidence-based and
must not provide investment advice.

==================================================
FINAL CHECK
==================================================

Before responding, verify that:

- All six sections are present.
- The response contains no Markdown formatting.
- There are no backticks.
- There are no Markdown headings.
- There are no Markdown links.
- There are no unsupported facts.
- There are no investment recommendations.
- The response is concise.
""".strip()