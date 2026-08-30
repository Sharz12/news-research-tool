from src.news.client import NewsClient

def test_parse_valid_article():
    raw_articles = [
        {
            "title": "Nvidia expands AI Infrastructure",
            "description": "Nvidia reports continued AI demand.",
            "content": "Example article content.",
            "source": {
                "name": "Example News"
            },
            "author": "Test Author",
            "url": "https://example.com/nvidia.ai",
            "urlToImage": None,
            "publishedAt": "2026-08-29T10:00:00Z",
        }
    ]

    articles = NewsClient._parse_articles(raw_articles)

    assert len(articles) == 1
    assert articles[0].title == "Nvidia expands AI Infrastructure"
    assert articles[0].source_name == "Example News"

# Another Test

def test_parse_invalid_article():
    raw_articles = [
        {
            "title": "Invalid article",
            "description": "Missing Url",
            "source": {
                "name": "Example News",
            },
            "url": None,
            "publishedAt": "2026-08-29T10:00:00Z",
        }
    ]

    articles = NewsClient._parse_articles(raw_articles)

    assert len(articles) == 0
    