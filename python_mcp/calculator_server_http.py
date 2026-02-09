#!/usr/bin/env python3
"""
Calculator MCP Server - HTTP Version

An MCP server that provides calculator functionality via HTTP/SSE transport.
Run with: python calculator_server_http.py
Access at: http://localhost:8000
"""

import logging
import math
from typing import Any

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("calculator-server-http")

# Initialize FastMCP server
app = FastMCP("calculator-server")


# ============================================================================
# CORE CALCULATION FUNCTIONS (Internal use)
# ============================================================================

async def _add_internal(a: float, b: float) -> float:
    """Internal add function. Returns raw number."""
    return a + b


async def _power_internal(base: float, exponent: float) -> float:
    """Internal power function. Returns raw number."""
    return math.pow(base, exponent)


# ============================================================================
# MCP TOOL REGISTRATIONS
# ============================================================================

@app.tool(
    name="add",
    description="Add two numbers together (basic addition) - for AI orchestration.",
)
async def add(
    a: float = "First number",
    b: float = "Second number",
) -> float:
    """Add two numbers. Returns raw number for AI to use in calculations."""
    try:
        logger.info(f"Tool called: add (AI orchestration) - a={a}, b={b}")
        result = await _add_internal(a, b)
        return result
    except Exception as e:
        logger.error(f"Addition error: {e}", exc_info=True)
        raise


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
    description="Raise a number to a power (exponentiation) - for AI orchestration.",
)
async def power(
    base: float = "Base number",
    exponent: float = "Exponent (power)",
) -> float:
    """Calculate base raised to the power of exponent. Returns raw number."""
    try:
        logger.info(f"Tool called: power (AI orchestration) - base={base}, exponent={exponent}")
        result = await _power_internal(base, exponent)
        return result
    except Exception as e:
        logger.error(f"Power calculation error: {e}", exc_info=True)
        raise


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

@app.tool(
    name="get_employee_details",
    description="to search employee details",
)
def get_employee_details(
    employee_id: str = "Employee ID",
) -> str:
    return {
        "employee_id": employee_id,
        "name": "John Doe",
        "department": "HR",
        "salary": 100000,
    }


# ============================================================================
# HYBRID ORCHESTRATION TOOLS
# ============================================================================

@app.tool(
    name="hr_add_numbers_fast",
    description="⚡ WORLD 2 - Fast combined calculation (AUTO-TRIGGERS prompt logic).",
)
async def hr_add_numbers_fast(
    a: float = "First number (base for power, first addend)",
    b: float = "Second number (exponent for power, second addend)",
) -> str:
    """
    WORLD 2 - TOOL ORCHESTRATES: Fast all-in-one calculation.
    ⚡ AUTO-TRIGGERS the hr_add_number_prompt logic internally.
    
    This tool automatically executes:
    1. power(a, b) to get a^b
    2. Addition a + b
    3. Combines both results
    4. Returns formatted answer
    
    The prompt logic is ALWAYS executed - no AI orchestration needed!
    """
    try:
        # 🔔 PROMPT AUTO-TRIGGER: Execute the workflow from hr_add_number_prompt
        logger.info(f"🔔 AUTO-TRIGGERING PROMPT: hr_add_number_prompt logic for a={a}, b={b}")
        
        # Step 1 from prompt: Calculate power (use internal function)
        logger.info(f"  Step 1: Calling power({a}, {b})")
        power_result = await _power_internal(a, b)
        logger.info(f"  Step 1 result: {power_result}")
        
        # Step 2 from prompt: Calculate addition (use internal function)
        logger.info(f"  Step 2: Calling add({a}, {b})")
        addition_result = await _add_internal(a, b)
        logger.info(f"  Step 2 result: {addition_result}")
        
        # Step 3 from prompt: Combine results
        logger.info(f"  Step 3: Combining {power_result} + {addition_result}")
        combined_total = power_result + addition_result
        logger.info(f"  Step 3 result: {combined_total}")
        
        # Step 4 from prompt: Format result
        logger.info(f"  Step 4: Formatting result with emoji style")
        result = f"⚡ Fast Mode (Prompt Auto-Executed): The power result is {power_result} ({a}^{b}), the addition result is {addition_result} ({a} + {b}), and the combined total is {combined_total}. 😊"
        
        logger.info(f"✅ PROMPT AUTO-TRIGGER COMPLETE")
        return result
    except Exception as e:
        logger.error(f"hr_add_numbers_fast error: {e}", exc_info=True)
        return f"Error: {str(e)}"


@app.tool(
    name="hr_add_numbers",
    description="🚀 Get instructions from hr_add_number_prompt for complex calculations.",
)
async def hr_add_numbers(
    a: float = "First number (base for power, first addend)",
    b: float = "Second number (exponent for power, second addend)",
) -> dict:
    """
    This tool directs AI to use the hr_add_number_prompt.
    It returns a reference to the prompt so AI can call it.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Message directing AI to use the prompt
    """
    try:
        # Direct AI to use the prompt instead of duplicating logic
        logger.info(f"🔔 Directing AI to use hr_add_number_prompt - a={a}, b={b}")
        
        return {
            "mode": "use_prompt",
            "message": f"Please call the 'hr_add_number_prompt' prompt with a={a} and b={b} to get the instructions for this calculation.",
            "prompt_name": "hr_add_number_prompt",
            "parameters": {"a": a, "b": b}
        }
    except Exception as e:
        logger.error(f"hr_add_numbers error: {e}", exc_info=True)
        return {"error": str(e)}


@app.prompt(
    name="hr_add_number_prompt",
    description="Prompt template for complex calculations with power and addition",
)
async def hr_add_number_prompt(
    a: float = "First number",
    b: float = "Second number",
) -> list[dict]:
    """
    AI ORCHESTRATES: Returns prompt instructions for AI to follow.
    The AI will call multiple tools step-by-step based on these instructions.
    """
    logger.info(f"🔔 Prompt triggered: hr_add_number_prompt - a={a}, b={b}")
    
    text = f"""You are given two numbers: {a} and {b}.

Step 1: Call the MCP tool 'power' with base={a} and exponent={b} to calculate {a}^{b}.
Step 2: Call the MCP tool 'add' with a={a} and b={b} to calculate {a} + {b}.
Step 3: Add the results from Step 1 and Step 2 together.
Step 4: Multiply the results from Step 1 and Step 2 together.
Step 5: Present the final result in words with emoji style.

Example format: 'The power result is X ({a}^{b}), the addition result is Y ({a} + {b}), the combined total is Z, and the multiplied result is W. 😊'"""
    
    return [{"role": "user", "content": text}]


if __name__ == "__main__":
    try:
        logger.info("Starting Calculator MCP Server with HTTP/SSE transport...")
        logger.info("Server will be available at: http://localhost:8000")
        logger.info("SSE endpoint: http://localhost:8000/sse")
        
        # Run with HTTP transport instead of stdio
        app.run(transport="sse", port=8000, host="127.0.0.1")
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise
