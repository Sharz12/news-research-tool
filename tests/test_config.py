from config.settings import GROK_API_KEY, NEWSAPI_KEY

def test_grok_api_key_exists():
    assert GROK_API_KEY

def test_newsapi_key_exists():
    assert NEWSAPI_KEY

