from .base_connector import BaseLLMConnector
from google import genai

class GeminiConnector(BaseLLMConnector):
    """LLM connector for Google's Gemini models."""
    provider = "gemini"
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = genai.Client(api_key=self.api_key)

    def call_llm(self, prompt: str) -> str:
        """
        Sends a prompt to the Gemini API and returns the text response.
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text
