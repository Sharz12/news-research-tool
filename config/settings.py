import os
from pathlib import Path

from dotenv import load_dotenv


# Project root:
# news-research-tool/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Explicitly locate the .env file in the project root.
ENV_FILE = PROJECT_ROOT / ".env"

# Load environment variables.
load_dotenv(dotenv_path=ENV_FILE, override=True)


GROK_API_KEY = os.getenv("GROK_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


if not GROK_API_KEY:
    raise ValueError(
        "GROK_API_KEY is missing. "
        "Add it to the .env file."
    )


if not NEWSAPI_KEY:
    raise ValueError(
        "NEWSAPI_KEY is missing. "
        "Add it to the .env file."
    )