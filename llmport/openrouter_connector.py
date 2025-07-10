from .base_connector import BaseLLMConnector
import requests

class OpenRouterConnector(BaseLLMConnector):
    """LLM connector for the OpenRouter API."""
    provider = "openrouter"
    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)

    def call_llm(self, prompt: str) -> str:
        """
        Sends a prompt to the OpenRouter API and returns the text response.
        """
        response = requests.post(
            url=self.API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
            },
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
            }
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
