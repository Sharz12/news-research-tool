from src.news.client import NewsClient

def main() -> None:
    client = NewsClient()

    articles = client.search(
        query= "technology",
        page_size= 5,
        days_back= 30,
    )

    print(f"Articles Retreived: {len(articles)}")

    for index, article in enumerate(articles, start=1):
        print()
        print(f"{index}, {article.title}")
        print(f" Source: {article.source_name}")
        print(f" Published: {article.published_at}")
        print(f" URL: {article.url}")

if __name__ == "__main__":
    main()