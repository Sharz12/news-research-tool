import logging

from langchain_groq import ChatGroq

from config.settings import GROQ_API_KEY, GROQ_MODEL


logger = logging.getLogger(__name__)


class GroqClient:
    """Client responsible for interacting with the Groq LLM."""

    def __init__(
        self,
        api_key: str = GROQ_API_KEY,
        model: str = GROQ_MODEL,
    ):
        if not api_key:
            raise ValueError("GROQ_API_KEY is required.")

        if not model:
            raise ValueError("GROQ_MODEL is required.")

        self.model = model

        self.llm = ChatGroq(
            api_key=api_key,
            model=model,
            temperature=0,
        )

        logger.info(
            "Initialized Groq client with model=%s",
            model,
        )

    def invoke(self, prompt: str) -> str:
        """
        Send a prompt to Groq and return the generated response.
        """

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            response = self.llm.invoke(prompt)

            return response.content

        except Exception as exc:
            logger.exception("Groq request failed.")

            raise RuntimeError(
                "Failed to generate response from Groq."
            ) from exc