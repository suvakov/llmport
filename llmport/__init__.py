"""
llmport: Smart, LLM-powered module generation.
"""
import warnings

# Suppress the specific Pydantic UserWarning from google-genai
warnings.filterwarnings("ignore", message="<built-in function any> is not a Python type")


__version__ = "0.1.0"

from .module_handler import ModuleHandler
from .gemini_connector import GeminiConnector
from .openrouter_connector import OpenRouterConnector
from .config import (
    configure,
    get_config,
    ConfigError
)
import importlib.util
import os
import sys
from datetime import datetime, timezone

_handler = None

def _get_handler():
    """Initializes and returns the singleton ModuleHandler."""
    global _handler
    if _handler is None:
        config = get_config()
        api_key = config.get("api_key")
        provider = config.get("provider")
        model = config.get("model")

        if not api_key:
            raise ConfigError("API key not configured. Please call llmport.configure() or set the appropriate environment variable.")

        connector_map = {
            "gemini": GeminiConnector,
            "openrouter": OpenRouterConnector,
        }
        connector_class = connector_map.get(provider)
        
        if not connector_class:
            raise ConfigError(f"LLM provider '{provider}' is not supported.")
        
        connector = connector_class(api_key=api_key, model=model)
        _handler = ModuleHandler(connector)
    return _handler

def _log_event(module_name: str, event: str, content: str, stdout: bool, log: bool):
    """Logs an event to the console and/or a log file."""
    log_message = f"--- {event} ---\n{content}\n"
    if stdout:
        print(log_message)
    if log:
        log_file_path = f"{module_name}.log"
        with open(log_file_path, "a") as f:
            f.write(log_message)

def _load_module(module_name: str, stdout: bool, log: bool):
    """Loads a module from a file path, handling ImportError."""
    file_path = f"{module_name}.py"
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec:
            raise ImportError(f"Could not load spec for module at {file_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except ImportError as e:
        error_message = f"Failed to import module '{module_name}'. Please ensure all required packages are installed. Details: {e}"
        _log_event(module_name, "IMPORT ERROR", error_message, stdout, log)
        print(error_message)
        return None


def llmport(module_name: str, prompt: str, stdout: bool = False, log: bool = True, overwrite: bool = False):
    """
    Imports a Python module, generating it from a prompt if it doesn't exist.
    """
    file_path = f"{module_name}.py"
    if os.path.exists(file_path) and not overwrite:
        return _load_module(module_name, stdout, log)

    handler = _get_handler()
    
    from .prompt_templates import GENERATE_PROMPT_TEMPLATE
    final_prompt = GENERATE_PROMPT_TEMPLATE.format(prompt=prompt)
    
    _log_event(module_name, "PROMPT", final_prompt, stdout, log)
    
    raw_response = handler.connector.call_llm(final_prompt)
    
    _log_event(module_name, "RESPONSE", raw_response, stdout, log)
    
    cleaned_code = handler._clean_response(raw_response)

    with open(file_path, "w") as f:
        f.write(cleaned_code)

    return _load_module(module_name, stdout, log)

def update(module_name: str, prompt: str, stdout: bool = False, log: bool = True):
    """
    Updates an existing LLM-generated module with a new prompt.
    """
    file_path = f"{module_name}.py"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist and cannot be updated.")

    with open(file_path, "r") as f:
        existing_code = f.read()

    handler = _get_handler()

    from .prompt_templates import UPDATE_PROMPT_TEMPLATE
    final_prompt = UPDATE_PROMPT_TEMPLATE.format(existing_code=existing_code, prompt=prompt)

    _log_event(module_name, "PROMPT", final_prompt, stdout, log)

    raw_response = handler.connector.call_llm(final_prompt)

    _log_event(module_name, "RESPONSE", raw_response, stdout, log)

    cleaned_code = handler._clean_response(raw_response)

    with open(file_path, "w") as f:
        f.write(cleaned_code)

    if module_name in sys.modules:
        try:
            importlib.reload(sys.modules[module_name])
            return sys.modules[module_name]
        except ImportError as e:
            error_message = f"Failed to reload module '{module_name}'. Please ensure all required packages are installed. Details: {e}"
            _log_event(module_name, "IMPORT ERROR", error_message, stdout, log)
            print(error_message)
            return None
    
    return _load_module(module_name, stdout, log)
