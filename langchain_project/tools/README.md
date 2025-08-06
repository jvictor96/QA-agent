# Tools Module

This directory contains all the tool functions for the LangChain chatbot, organized by category.

## Adding New Tools

To add new tools:

1. Create a new file in the `tools/` directory (e.g., `new_category_tools.py`)
2. Import the `@tool` decorator from `langchain_core.tools`
3. Define your tool functions with the `@tool` decorator
4. Add the imports to `__init__.py`
5. Update the `__all__` list in `__init__.py`

Example:
```python
from langchain_core.tools import tool

@tool
def my_new_tool(param: str) -> str:
    """Description of what the tool does."""
    # Tool implementation
    return "Result"
```

## Usage

Import tools in your main application:
```python
from tools import roll_dice, calculate_square_root, calculate_power
...
tools = [roll_dice, calculate_square_root, calculate_power]
agent_executor = create_react_agent(model, tools, checkpointer=memory)
```
