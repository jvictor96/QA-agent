import random
from langchain_core.tools import tool


@tool
def roll_dice(sides: int = 6) -> str:
    """Roll a dice with the specified number of sides. Default is 6-sided dice."""
    if sides < 2:
        return "Error: Dice must have at least 2 sides."
    result = random.randint(1, sides)
    response = f"Rolled {result} on a d{sides}"
    return response
