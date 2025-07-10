# llmport: LLM-powered Module Generation

`llmport` is a Python library that uses Large Language Models (LLMs) to dynamically create and update single-file Python modules.
It's designed for prototyping and development, especially in environments like Python interpreter or Jupyter notebooks. It allows developers to stay within their Python environment to generate code, eliminating the need to switch to external LLM chat tools and then manually copy-paste the code back into their project.

On the first run, `llmport` generates a new Python file based on a natural language prompt. On subsequent runs, it directly imports the existing file, saving time and LLM calls.
Optionally, you can rewrite it or update it with a new prompt.

## Core Functionality

### `llmport()`

The `llmport()` function is the main entry point. It works like a standard import, but if the specified module doesn't exist, it generates it from your prompt. You can also force it to regenerate an existing module.

**Arguments:**
- `module_name` (str): The name of the module to import or generate (without the `.py` extension).
- `prompt` (str): The natural language prompt describing the module's functionality.
- `stdout` (bool, optional): If `True`, prints the full LLM interaction to the console. Defaults to `False`.
- `log` (bool, optional): If `True`, saves the LLM interaction to a `.log` file. Defaults to `True`.
- `overwrite` (bool, optional): If `True`, forces the regeneration of the module even if it already exists. Defaults to `False`.

**Example:**

```python
import llmport

# Prompt describing the desired module
math_utils_prompt = """
Create a Python module with the following capabilities:
- A function `primes_to(n)` that returns a list of all prime numbers up to n.
- A function `fibonacci(i)` that returns the i-th Fibonacci number.
"""

# On the first run, this generates 'math_utils.py'.
# On subsequent runs, it imports the existing file.
math_utils = llmport.llmport("math_utils", math_utils_prompt)

print(f"Primes up to 20: {math_utils.primes_to(20)}")
print(f"The 10th Fibonacci number is: {math_utils.fibonacci(10)}")
```

### Logging and Error Handling

`llmport` provides real-time logging and handles common import errors gracefully.

- **Real-time Logging**: The library logs the prompt before sending it to the LLM and logs the response as soon as it's received. This is useful for debugging and understanding the generation process.
- **Log Files**: By default, all interactions are saved to a `{module_name}.log` file.
- **ImportError Handling**: If a generated module requires a package that is not installed, `llmport` will catch the `ImportError`, print a user-friendly message to the console indicating which packages are missing, and log the error.

You can control logging behavior with the `stdout` and `log` arguments in both the `llmport()` and `update()` functions.

### `update()`

The `update()` function allows you to modify an existing module with a new prompt. It provides the full context of the existing code to the LLM and automatically reloads the module in your current session, making the changes immediately available.

**Example:**

```python
import llmport

# Assume 'math_utils.py' was already created.
update_prompt = "Please add a new function: `factorial(n)`."

# The 'update' function handles writing the new code and reloading the module.
math_utils = llmport.update("math_utils", update_prompt)

print(f"Factorial of 5 is: {math_utils.factorial(5)}")
```

## Configuration

`llmport` can be configured using environment variables or by calling the `configure()` function directly in your code.

### Environment Variables

This is the recommended way to set your API keys and default provider.

```bash
# For Gemini
export LLMPORT_PROVIDER="gemini"
export GEMINI_API_KEY="your-gemini-api-key" # Also checks for GOOGLE_API_KEY
export LLMPORT_GEMINI_MODEL="gemini-1.5-flash" # Optional

# For OpenRouter
export LLMPORT_PROVIDER="openrouter"
export OPENROUTER_API_KEY="your-openrouter-api-key"
export LLMPORT_OPENROUTER_MODEL="deepseek/deepseek-chat-v3-0324:free" # Optional
```

### `configure()` Function (alternative)

Use this to override settings for a specific script.

```python
import llmport

llmport.configure(
    provider="openrouter",
    api_key="YOUR_API_KEY",
    model="anthropic/claude-3-haiku"
)
```

## Supported LLM APIs

- **Gemini**: Google's family of models.
- **OpenRouter**: A platform that gives you access to a wide variety of LLMs.
