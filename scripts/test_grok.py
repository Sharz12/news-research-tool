from src.llm.client import GroqClient


def main() -> None:
    client = GroqClient()

    response = client.invoke(
        "In one sentence, explain why artificial intelligence "
        "is important for modern businesses."
    )

    print("\nGROQ RESPONSE:")
    print(response)


if __name__ == "__main__":
    main()