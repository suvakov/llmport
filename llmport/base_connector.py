class BaseLLMConnector:
    """
    Base class for LLM connectors. Defines the interface for calling an LLM.
    """
    provider: str

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def call_llm(self, prompt: str) -> str:
        """
        Sends a prompt to the LLM and returns the raw text response.

        Returns:
            The raw text response from the LLM.
        """
        raise NotImplementedError("Connectors must implement the 'call_llm' method.")
