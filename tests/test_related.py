from src.recommendations.related import (
    RelatedNewsGenerator,
    RelatedNewsRecommendations,
)


class FakeLLMClient:
    """Fake LLM client for recommendation tests."""

    def invoke(self, prompt):
        assert "Weather in USA" in prompt
        assert "within_topic" in prompt
        assert "broader_context" in prompt

        return (
            '{"within_topic": ['
            '"California weather", '
            '"Texas weather", '
            '"Florida weather", '
            '"New York weather"'
            '], "broader_context": ['
            '"Weather in India", '
            '"Weather in UK", '
            '"Weather in Japan", '
            '"Weather in Australia"'
            ']}'
        )


def test_generate_returns_recommendations():

    generator = RelatedNewsGenerator(
        llm_client=FakeLLMClient()
    )

    result = generator.generate(
        "Weather in USA"
    )

    assert isinstance(
        result,
        RelatedNewsRecommendations,
    )

    assert result.within_topic == [
        "California weather",
        "Texas weather",
        "Florida weather",
        "New York weather",
    ]

    assert result.broader_context == [
        "Weather in India",
        "Weather in UK",
        "Weather in Japan",
        "Weather in Australia",
    ]


def test_generate_rejects_empty_query():

    generator = RelatedNewsGenerator(
        llm_client=FakeLLMClient()
    )

    try:
        generator.generate("")

        assert False, (
            "Expected ValueError for empty query."
        )

    except ValueError as exc:
        assert str(exc) == (
            "Recommendation query cannot be empty."
        )


def test_generate_rejects_invalid_limit():

    generator = RelatedNewsGenerator(
        llm_client=FakeLLMClient()
    )

    try:
        generator.generate(
            "Weather in USA",
            max_recommendations=0,
        )

        assert False, (
            "Expected ValueError for invalid limit."
        )

    except ValueError as exc:
        assert str(exc) == (
            "max_recommendations must be greater than 0."
        )


def test_parser_removes_markdown_code_fences():

    response = (
        '```json\n'
        '{\n'
        '    "within_topic": [\n'
        '        "California weather"\n'
        '    ],\n'
        '    "broader_context": [\n'
        '        "Weather in India"\n'
        '    ]\n'
        '}\n'
        '```'
    )

    result = RelatedNewsGenerator._parse_response(
        response,
        max_recommendations=4,
    )

    assert result.within_topic == [
        "California weather"
    ]

    assert result.broader_context == [
        "Weather in India"
    ]


def test_parser_removes_duplicates():

    response = (
        '{'
        '"within_topic": ['
        '"California weather", '
        '"California weather", '
        '"Texas weather", '
        '"texas weather"'
        '], '
        '"broader_context": ['
        '"Weather in India", '
        '"Weather in India"'
        ']'
        '}'
    )

    result = RelatedNewsGenerator._parse_response(
        response,
        max_recommendations=4,
    )

    assert result.within_topic == [
        "California weather",
        "Texas weather",
    ]

    assert result.broader_context == [
        "Weather in India",
    ]


def test_parser_respects_recommendation_limit():

    response = (
        '{'
        '"within_topic": ['
        '"California weather", '
        '"Texas weather", '
        '"Florida weather", '
        '"New York weather"'
        '], '
        '"broader_context": ['
        '"Weather in India", '
        '"Weather in UK", '
        '"Weather in Japan", '
        '"Weather in Australia"'
        ']'
        '}'
    )

    result = RelatedNewsGenerator._parse_response(
        response,
        max_recommendations=2,
    )

    assert result.within_topic == [
        "California weather",
        "Texas weather",
    ]

    assert result.broader_context == [
        "Weather in India",
        "Weather in UK",
    ]


def test_parser_handles_invalid_json():

    response = "This is not valid JSON."

    try:
        RelatedNewsGenerator._parse_response(
            response,
            max_recommendations=4,
        )

        assert False, (
            "Expected ValueError for invalid JSON."
        )

    except ValueError as exc:
        assert str(exc) == (
            "Recommendation model returned invalid JSON."
        )


def test_parser_handles_missing_categories():

    response = (
        '{'
        '"within_topic": ['
        '"California weather"'
        ']'
        '}'
    )

    result = RelatedNewsGenerator._parse_response(
        response,
        max_recommendations=4,
    )

    assert result.within_topic == [
        "California weather"
    ]

    assert result.broader_context == []