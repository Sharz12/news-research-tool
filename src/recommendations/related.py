import json
import re
from dataclasses import dataclass

from src.llm.client import GroqClient


# =========================================================
# DATA MODEL
# =========================================================


@dataclass
class RelatedNewsRecommendations:
    """Structured related-news recommendations."""

    within_topic: list[str]
    broader_context: list[str]


# =========================================================
# RECOMMENDATION GENERATOR
# =========================================================


class RelatedNewsGenerator:
    """
    Generates context-aware news search recommendations
    using the configured LLM.
    """

    def __init__(
        self,
        llm_client: GroqClient | None = None,
    ):
        self.llm_client = (
            llm_client or GroqClient()
        )

    def generate(
        self,
        query: str,
        max_recommendations: int = 4,
    ) -> RelatedNewsRecommendations:
        """
        Generate related news searches for a query.

        The recommendations are divided into:

        1. Within-topic recommendations
        2. Broader-context recommendations
        """

        query = query.strip()

        if not query:
            raise ValueError(
                "Recommendation query cannot be empty."
            )

        if max_recommendations < 1:
            raise ValueError(
                "max_recommendations must be greater than 0."
            )

        prompt = self._build_prompt(
            query=query,
            max_recommendations=max_recommendations,
        )

        raw_response = self.llm_client.invoke(
            prompt
        )

        return self._parse_response(
            raw_response,
            max_recommendations=max_recommendations,
        )

    # =====================================================
    # PROMPT
    # =====================================================

    @staticmethod
    def _build_prompt(
        query: str,
        max_recommendations: int,
    ) -> str:
        """
        Build a controlled prompt for recommendation
        generation.
        """

        return f"""
You are a news research recommendation assistant.

The user searched for:

{query}

Generate useful follow-up news searches that help
the user explore the topic more deeply.

Return ONLY valid JSON.

Use exactly this structure:

{{
  "within_topic": [
    "search query 1",
    "search query 2",
    "search query 3",
    "search query 4"
  ],
  "broader_context": [
    "search query 1",
    "search query 2",
    "search query 3",
    "search query 4"
  ]
}}

RECOMMENDATION RULES:

1. Generate no more than {max_recommendations}
   recommendations in each category.

2. "within_topic" should explore the original query
   through closely related entities, locations, subtopics,
   industries, companies, events, or developments.

3. If the query has a geographic component, prioritize
   relevant locations within that geography.

4. For example, if the user searches for:
   "weather in USA"

   useful within-topic recommendations could include:
   "California weather"
   "Texas weather"
   "Florida weather"
   "New York weather"

5. "broader_context" should expand beyond the original
   query into useful related regions, markets, countries,
   industries, competitors, or global developments.

6. If the original query concerns a country, include
   relevant international comparisons where useful.

7. If the original query concerns a company, include
   relevant competitors, industry developments, or
   adjacent business areas where useful.

8. If the original query concerns a topic rather than
   a company, identify closely related subtopics.

9. Recommendations must be realistic news-search queries.

10. Keep each recommendation concise.

11. Do not create recommendations that are unrelated
    to the user's original query.

12. Do not provide explanations.

13. Do not include numbering.

14. Do not include Markdown.

15. Do not include URLs.

16. Do not invent specific events, statistics, or claims.
    The recommendations are search queries, not factual
    statements.

17. Avoid duplicate or nearly identical recommendations.

18. Return valid JSON only.

19. If there are fewer useful recommendations than
    requested, return fewer rather than inventing
    unrelated suggestions.
""".strip()

    # =====================================================
    # RESPONSE PARSING
    # =====================================================

    @staticmethod
    def _parse_response(
        response: str,
        max_recommendations: int,
    ) -> RelatedNewsRecommendations:
        """
        Parse and validate the LLM recommendation response.
        """

        if not response or not response.strip():
            raise ValueError(
                "Recommendation model returned an empty response."
            )

        cleaned = response.strip()

        # -------------------------------------------------
        # Remove accidental Markdown code fences
        # -------------------------------------------------

        cleaned = re.sub(
            r"```(?:json)?",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = cleaned.replace(
            "```",
            "",
        ).strip()

        # -------------------------------------------------
        # Extract JSON object if the model added text
        # around the JSON.
        # -------------------------------------------------

        json_match = re.search(
            r"\{.*\}",
            cleaned,
            flags=re.DOTALL,
        )

        if not json_match:
            raise ValueError(
                "Recommendation model returned invalid JSON."
            )

        json_text = json_match.group(0)

        try:
            data = json.loads(
                json_text
            )

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Recommendation model returned invalid JSON."
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                "Recommendation response must be a JSON object."
            )

        within_topic = RelatedNewsGenerator._clean_list(
            data.get("within_topic")
        )

        broader_context = RelatedNewsGenerator._clean_list(
            data.get("broader_context")
        )

        within_topic = RelatedNewsGenerator._limit_unique(
            within_topic,
            max_recommendations,
        )

        broader_context = RelatedNewsGenerator._limit_unique(
            broader_context,
            max_recommendations,
        )

        return RelatedNewsRecommendations(
            within_topic=within_topic,
            broader_context=broader_context,
        )

    # =====================================================
    # LIST CLEANING
    # =====================================================

    @staticmethod
    def _clean_list(
        values,
    ) -> list[str]:
        """
        Clean a recommendation list and discard invalid
        values.
        """

        if not isinstance(values, list):
            return []

        cleaned = []

        for value in values:

            if not isinstance(value, str):
                continue

            value = re.sub(
                r"\s+",
                " ",
                value,
            ).strip()

            value = re.sub(
                r"^[\-\*\d\.\)\s]+",
                "",
                value,
            ).strip()

            if not value:
                continue

            cleaned.append(
                value
            )

        return cleaned

    # =====================================================
    # DEDUPLICATION
    # =====================================================

    @staticmethod
    def _limit_unique(
        values: list[str],
        limit: int,
    ) -> list[str]:
        """
        Remove duplicate recommendations while preserving
        their original order.
        """

        unique = []
        seen = set()

        for value in values:

            normalized = value.casefold()

            if normalized in seen:
                continue

            seen.add(
                normalized
            )

            unique.append(
                value
            )

            if len(unique) >= limit:
                break

        return unique