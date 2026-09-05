import pytest

from src.llm.client import GroqClient


def test_empty_prompt_is_rejected():
    client = GroqClient.__new__(GroqClient)

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        client.invoke("")


def test_whitespace_prompt_is_rejected():
    client = GroqClient.__new__(GroqClient)

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        client.invoke("   ")


def test_missing_api_key_is_rejected():
    with pytest.raises(ValueError, match="GROQ_API_KEY is required"):
        GroqClient(api_key="")


def test_missing_model_is_rejected():
    with pytest.raises(ValueError, match="GROQ_MODEL is required"):
        GroqClient(api_key="test-key", model="")


def test_successful_response(monkeypatch):
    client = GroqClient.__new__(GroqClient)

    class FakeResponse:
        content = "This is a test summary."

    class FakeLLM:
        def invoke(self, prompt):
            assert prompt == "Summarize this news."
            return FakeResponse()

    client.llm = FakeLLM()

    result = client.invoke("Summarize this news.")

    assert result == "This is a test summary."


def test_groq_failure_is_wrapped():
    client = GroqClient.__new__(GroqClient)

    class FakeLLM:
        def invoke(self, prompt):
            raise Exception("API failure")

    client.llm = FakeLLM()

    with pytest.raises(
        RuntimeError,
        match="Failed to generate response from Groq",
    ):
        client.invoke("Test prompt.")