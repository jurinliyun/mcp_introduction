#!/usr/bin/env python3
"""
Calculator MCP Server

An MCP server that provides calculator functionality for basic and advanced mathematical operations.
Refactored to use FastMCP for cleaner, more maintainable code.
"""

import logging
import math
from typing import Any

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("calculator-server")

# Initialize FastMCP server
app = FastMCP("calculator-server")


@app.tool(
    name="add",
    description="Add two or more numbers together.",
)
async def add(
    a: float = "First number",
    b: float = "Second number",
) -> str:
    """Add two numbers."""
    try:
        result = a + b
        return f"{a} + {b} = {result}"
    except Exception as e:
        logger.error(f"Addition error: {e}", exc_info=True)
        return f"Error: {str(e)}"


@app.tool(
    name="subtract",
    description="Subtract one number from another.",
)
async def subtract(
    a: float = "First number (minuend)",
    b: float = "Second number (subtrahend)",
) -> str:
    """Subtract b from a."""
    try:
        result = a - b
        return f"{a} - {b} = {result}"
    except Exception as e:
        logger.error(f"Subtraction error: {e}", exc_info=True)
        return f"Error: {str(e)}"


@app.tool(
    name="multiply",
    description="Multiply two or more numbers together.",
)
async def multiply(
    a: float = "First number",
    b: float = "Second number",
) -> str:
    """Multiply two numbers."""
    try:
        result = a * b
        return f"{a} × {b} = {result}"
    except Exception as e:
        logger.error(f"Multiplication error: {e}", exc_info=True)
        return f"Error: {str(e)}"


@app.tool(
    name="divide",
    description="Divide one number by another.",
)
async def divide(
    a: float = "Dividend (number to be divided)",
    b: float = "Divisor (number to divide by)",
) -> str:
    """Divide a by b."""
    try:
        if b == 0:
            return "Error: Division by zero is not allowed"
        result = a / b
        return f"{a} ÷ {b} = {result}"
    except Exception as e:
        logger.error(f"Division error: {e}", exc_info=True)
        return f"Error: {str(e)}"


@app.tool(
    name="power",
    description="Raise a number to a power (exponentiation).",
)
async def power(
    base: float = "Base number",
    exponent: float = "Exponent (power)",
) -> str:
    """Calculate base raised to the power of exponent."""
    try:
        result = math.pow(base, exponent)
        return f"{base} ^ {exponent} = {result}"
    except Exception as e:
        logger.error(f"Power calculation error: {e}", exc_info=True)
        return f"Error: {str(e)}"


@app.tool(
    name="square_root",
    description="Calculate the square root of a number.",
)
async def square_root(
    number: float = "Number to find the square root of",
) -> str:
    """Calculate the square root of a number."""
    try:
        if number < 0:
            return "Error: Cannot calculate square root of negative number"
        result = math.sqrt(number)
        return f"√{number} = {result}"
    except Exception as e:
        logger.error(f"Square root error: {e}", exc_info=True)
        return f"Error: {str(e)}"


@app.tool(
    name="calculate",
    description="Perform a basic arithmetic calculation with two numbers and an operator (+, -, *, /, ^).",
)
async def calculate(
    expression: str = "Mathematical expression (e.g., '5 + 3', '10 * 2', '8 / 4', '2 ^ 3')",
) -> str:
    """Calculate a simple mathematical expression."""
    try:
        # Remove whitespace
        expression = expression.strip()
        
        # Try to parse simple expressions
        operators = ['+', '-', '*', '/', '^', '×', '÷']
        operator = None
        for op in operators:
            if op in expression:
                operator = op
                break
        
        if not operator:
            return "Error: No valid operator found. Supported operators: +, -, *, /, ^"
        
        # Split by operator
        parts = expression.split(operator, 1)
        if len(parts) != 2:
            return "Error: Invalid expression format"
        
        try:
            a = float(parts[0].strip())
            b = float(parts[1].strip())
        except ValueError:
            return "Error: Invalid numbers in expression"
        
        # Perform calculation based on operator
        if operator in ['+', '-', '*', '/', '×', '÷']:
            if operator == '+' or operator == '-':
                if operator == '+':
                    result = a + b
                    return f"{a} + {b} = {result}"
                else:
                    result = a - b
                    return f"{a} - {b} = {result}"
            elif operator == '*' or operator == '×':
                result = a * b
                return f"{a} × {b} = {result}"
            elif operator == '/' or operator == '÷':
                if b == 0:
                    return "Error: Division by zero is not allowed"
                result = a / b
                return f"{a} ÷ {b} = {result}"
        elif operator == '^':
            result = math.pow(a, b)
            return f"{a} ^ {b} = {result}"
        
        return "Error: Unsupported operator"
        
    except Exception as e:
        logger.error(f"Calculation error: {e}", exc_info=True)
        return f"Error: {str(e)}"


if __name__ == "__main__":
    try:
        logger.info("Starting Calculator MCP Server with FastMCP...")
        app.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise

