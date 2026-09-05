from src.news.exceptions import (
    NewsAPIAuthenticationError,
    NewsAPIError,
    NewsAPIRequestError,
    NewsAPIResponseError,
    NewsAPIRateLimitError,
)


def test_exception_hierarchy():
    assert issubclass(NewsAPIAuthenticationError, NewsAPIError)
    assert issubclass(NewsAPIRateLimitError, NewsAPIError)
    assert issubclass(NewsAPIRequestError, NewsAPIError)
    assert issubclass(NewsAPIResponseError, NewsAPIError)


def test_exceptions_can_be_raised():
    try:
        raise NewsAPIRequestError("Test request failure")
    except NewsAPIError as exc:
        assert str(exc) == "Test request failure"
        