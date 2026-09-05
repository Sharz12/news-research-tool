class NewsAPIError(Exception):
    """Base exception for all NewsAPI-related errors."""


class NewsAPIAuthenticationError(NewsAPIError):
    """Raised when NewsAPI authentication fails."""


class NewsAPIRateLimitError(NewsAPIError):
    """Raised when NewsAPI rate limits the request."""


class NewsAPIRequestError(NewsAPIError):
    """Raised when a NewsAPI request fails."""


class NewsAPIResponseError(NewsAPIError):
    """Raised when NewsAPI returns an invalid response."""