from langchain_core.tools import tool
import math


@tool
def calculate_square_root(number: float) -> str:
    """Calculate the square root of a number."""
    if number < 0:
        return "Error: Cannot calculate square root of a negative number."
    result = math.sqrt(number)
    return f"The square root of {number} is {result:.4f}"


@tool
def calculate_power(base: float, exponent: float) -> str:
    """Calculate a number raised to a power."""
    result = math.pow(base, exponent)
    return f"{base} raised to the power of {exponent} is {result:.4f}"
