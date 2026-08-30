from datetime import datetime

from pydantic import BaseModel, HttpUrl

class NewsArticle(BaseModel):
    """ Validated representation of News Article."""

    title: str
    description: str | None = None
    content: str | None = None

    source_name: str
    author: str | None = None

    url: HttpUrl
    image_url: HttpUrl | None = None

    published_at: datetime


