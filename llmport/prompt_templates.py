GENERATE_PROMPT_TEMPLATE = """
Generate a complete Python module based on the following prompt.
The code should be production-quality, well-documented, and follow PEP 8 standards.
Do not include any introductory text or explanations, only the raw Python code.
Do not use "```python ... ```" to format the code, just return the raw Python code. 

Prompt:
---
{prompt}
---
"""

UPDATE_PROMPT_TEMPLATE = """
Given the following existing Python module:
---
{existing_code}
---

Update the module based on this request: "{prompt}"
Return the complete, updated code for the entire file.
Do not include any introductory text or explanations, only the raw Python code.
Do not use "```python ... ```" to format the code, just return the raw Python code. 
"""
