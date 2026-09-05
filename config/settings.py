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


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")



if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to the .env file."
    )


if not NEWSAPI_KEY:
    raise ValueError(
        "NEWSAPI_KEY is missing. "
        "Add it to the .env file."
    )
