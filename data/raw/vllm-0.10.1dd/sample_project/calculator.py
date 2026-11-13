"""Small calculator module for testing Python chunking."""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference between two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


class Calculator:
    """Keep a history of arithmetic results."""

    def __init__(self) -> None:
        self.history: list[float] = []

    def calculate(self, operation: str, a: float, b: float) -> float:
        if operation == "add":
            result = add(a, b)
        elif operation == "subtract":
            result = subtract(a, b)
        elif operation == "multiply":
            result = multiply(a, b)
        else:
            raise ValueError(f"Unknown operation: {operation}")
        self.history.append(result)
        return result
