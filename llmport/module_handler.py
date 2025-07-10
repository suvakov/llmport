from __future__ import annotations
from .base_connector import BaseLLMConnector
from .prompt_templates import GENERATE_PROMPT_TEMPLATE, UPDATE_PROMPT_TEMPLATE
import re

class ModuleHandler:
    """
    Handles the logic of generating and updating module files
    using a provided LLM connector.
    """
    def __init__(self, connector: BaseLLMConnector):
        self.connector = connector

    def _clean_response(self, response: str) -> str:
        """Removes markdown formatting from the LLM's response."""
        match = re.search(r"```(?:python)?\n(.*?)\n```", response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response.strip()

    def generate_module(self, prompt: str) -> tuple[str, str, str]:
        """Creates the full code for a new module."""
        final_prompt = GENERATE_PROMPT_TEMPLATE.format(prompt=prompt)
        raw_response = self.connector.call_llm(final_prompt)
        cleaned_code = self._clean_response(raw_response)
        
        return cleaned_code, final_prompt, raw_response

    def update_module(self, existing_code: str, prompt: str) -> tuple[str, str, str]:
        """Creates the full code for an updated module."""
        final_prompt = UPDATE_PROMPT_TEMPLATE.format(existing_code=existing_code, prompt=prompt)
        raw_response = self.connector.call_llm(final_prompt)
        cleaned_code = self._clean_response(raw_response)
        
        return cleaned_code, final_prompt, raw_response
