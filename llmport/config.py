import os

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

_config = {
    "provider": os.environ.get("LLMPORT_PROVIDER", "gemini"),
    "api_key": None,
    "model": None,
}

PROVIDER_CONFIG = {
    "gemini": {
        "api_key_vars": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
        "model_env_var": "LLMPORT_GEMINI_MODEL",
        "default_model": "gemini-1.5-flash",
    },
    "openrouter": {
        "api_key_vars": ["OPENROUTER_API_KEY"],
        "model_env_var": "LLMPORT_OPENROUTER_MODEL",
        "default_model": "deepseek/deepseek-chat-v3-0324:free",
    },
}

def configure(provider: str = None, api_key: str = None, model: str = None):
    """
    Sets configuration for the llmport library.
    """
    if provider:
        _config["provider"] = provider
    if api_key:
        _config["api_key"] = api_key
    if model:
        _config["model"] = model

def get_config():
    """
    Gets the current configuration, falling back to environment variables.
    """
    provider = _config["provider"]
    if provider not in PROVIDER_CONFIG:
        raise ConfigError(f"Unsupported provider: {provider}")

    provider_config = PROVIDER_CONFIG[provider]

    if _config["api_key"] is None:
        for env_var in provider_config["api_key_vars"]:
            api_key = os.environ.get(env_var)
            if api_key:
                _config["api_key"] = api_key
                break

    if _config["model"] is None:
        _config["model"] = os.environ.get(
            provider_config["model_env_var"],
            provider_config["default_model"]
        )

    return _config
