# Hybrid Approach - Both Worlds Example (Python)

## Overview
This demonstrates three ways to calculate: power(a,b) + add(a,b) using Python FastMCP

---

## 🌍 WORLD 1: AI Orchestrates (Flexible, Multi-Step)

### How to use:
1. User invokes the prompt or AI asks a question
2. AI calls multiple tools step-by-step
3. AI does reasoning and combines results

### Example Flow:
```
User: "Calculate power and addition for 5 and 3"

Option A - Using Prompt:
├─ Call hr_add_number_prompt(5, 3)
├─ Prompt returns instructions
└─ AI follows instructions:
    ├─ Step 1: Call power(5, 3) → Result: 125.0
    ├─ Step 2: Call add(5, 3) → Result: 8.0
    ├─ Step 3: AI calculates: 125.0 + 8.0 = 133.0
    └─ Step 4: AI formats: "The power result is 125.0, addition is 8.0, total is 133.0 😊"

Option B - Using Hybrid Tool in AI Mode:
├─ Call hr_add_numbers(5, 3, let_ai_orchestrate=True)
├─ Returns instructions dict
└─ AI follows the instructions (same as above)
```

### Tools/Prompts used:
- **`hr_add_number_prompt(a, b)`** - Returns instructions for AI
- **`power(base, exponent)`** - Returns raw float (a^b)
- **`add(a, b)`** - Returns raw float (a+b)
- AI combines the results

### When to use:
✅ Complex workflows with multiple steps
✅ Need flexibility (AI can adapt logic)
✅ Want AI reasoning visible
✅ Can chain with other prompts
✅ Educational/debugging purposes

---

## ⚡ WORLD 2: Tool Orchestrates (Fast, All-in-One)

### How to use:
1. Call single tool with parameters
2. Tool does everything internally
3. Get formatted result immediately

### Example Flow:
```
User/AI: Call hr_add_numbers_fast(5, 3)

Tool internally:
├─ Calls power(5, 3) → 125.0
├─ Calls add(5, 3) → 8.0
├─ Combines 125.0 + 8.0 → 133.0
└─ Returns formatted: "⚡ Fast Mode: power is 125.0, addition is 8.0, total is 133.0 😊"

Result: Instant answer in 1 tool call!
```

### Tools used:
- **`hr_add_numbers_fast(a, b)`** - Does everything, returns formatted string

### When to use:
✅ Need speed (1 tool call vs multiple)
✅ Want guaranteed accuracy
✅ Don't need AI reasoning
✅ Simple, repeatable calculations
✅ Production systems

---

## 🚀 HYBRID: Smart Mode (Best of Both)

### How to use:
Use `hr_add_numbers(a, b, let_ai_orchestrate)` with different parameters:
- **AI mode (default)**: `hr_add_numbers(5, 3)` or `hr_add_numbers(5, 3, True)`
- **Fast mode**: `hr_add_numbers(5, 3, False)`

### Example Flow - AI Mode (Default):
```python
# Call with AI orchestration (default)
result = await hr_add_numbers(5, 3)
# or explicitly
result = await hr_add_numbers(5, 3, let_ai_orchestrate=True)

# Returns:
{
  "mode": "ai_orchestration",
  "instructions": "You are given two numbers: 5 and 3...",
  "hint": "AI should call 'power' and 'add' tools, then combine results"
}

# Then AI follows instructions and makes multiple tool calls
```

### Example Flow - Fast Mode:
```python
# Call with tool orchestration
result = await hr_add_numbers(5, 3, let_ai_orchestrate=False)

# Returns:
"🚀 Smart Mode: The power result is 125.0 (5^3), the addition result is 8.0 (5 + 3), and the combined total is 133.0. 😊"
```

---

## 📊 Comparison

| Feature | World 1 (AI) | World 2 (Tool) | Hybrid (Smart) |
|---------|-------------|----------------|----------------|
| Speed | Slower (3+ calls) | Fast (1 call) | Configurable |
| Token Usage | High | Low | Configurable |
| Flexibility | High | Low | High |
| Accuracy | Depends on AI | Guaranteed | Both |
| AI Reasoning | Visible | Hidden | Configurable |
| Return Type | Instructions → AI acts | Formatted string | Both |
| Use Case | Complex workflows | Simple repeatable | Adaptive |

---

## 🎯 Real-World Examples

### Example 1: Simple Calculation (Use World 2)
```python
# Question: "What's 5^3 + 5+3?"
result = await hr_add_numbers_fast(5, 3)
# Why: Simple, fast, one call
# Returns: "⚡ Fast Mode: The power result is 125.0..."
```

### Example 2: Explain the Process (Use World 1)
```python
# Question: "Show me step-by-step how to calculate power and addition for 5 and 3"
# Option A: Use prompt
instructions = await hr_add_number_prompt(5, 3)
# Option B: Use hybrid in AI mode
instructions = await hr_add_numbers(5, 3, let_ai_orchestrate=True)
# Why: AI shows each step clearly
```

### Example 3: Conditional Logic (Use Hybrid)
```python
# Question: "Calculate for 5 and 3, but explain if result > 100"

# Start with fast mode
result = await hr_add_numbers(5, 3, let_ai_orchestrate=False)

# If AI needs to explain (result > 100), switch to AI mode
if needs_explanation:
    instructions = await hr_add_numbers(5, 3, let_ai_orchestrate=True)
    # AI follows instructions and explains each step

# Why: Fast first, flexible when needed
```

---

## 🔧 Available Tools Summary

### Basic Tools (Building Blocks) - WORLD 1 Helpers
- **`power(base, exponent)`** → float (raw number)
- **`add(a, b)`** → float (raw number)

### Orchestrator Tools
- **`hr_add_numbers_fast(a, b)`** → str (formatted result with ⚡ emoji)
- **`hr_add_numbers(a, b, let_ai_orchestrate=True)`** → dict|str (adaptive)

### Prompts
- **`hr_add_number_prompt(a, b)`** → list[dict] (instructions for AI)

---

## 💡 Best Practices

1. **Default to AI Mode for flexibility** - The hybrid tool defaults to `let_ai_orchestrate=True`
2. **Use Fast Mode for production** - When you know the exact workflow
3. **Use Hybrid** for adaptive scenarios - Start with AI mode, switch if needed
4. **Check logs** to see which mode was used:
   - `"Tool called: add (AI orchestration)"`
   - `"Tool orchestrator: hr_add_numbers_fast"`
   - `"AI orchestration mode activated"`
   - `"Tool orchestration mode (default)"`

---

## 🧪 Test Commands

### Start the Calculator Server
```bash
cd python_mcp
source env/bin/activate  # On Windows: env\Scripts\activate
python calculator_server.py
```

### Configure in Claude Desktop (macOS)
```json
{
  "mcpServers": {
    "calculator": {
      "command": "/absolute/path/to/python_mcp/env/bin/python",
      "args": ["/absolute/path/to/python_mcp/calculator_server.py"]
    }
  }
}
```

### Test with AI Client
Once configured, you can ask:
- **World 1**: "Use the hr_add_number_prompt to calculate 5 and 3"
- **World 2**: "Use hr_add_numbers_fast with 5 and 3"
- **Hybrid (AI)**: "Call hr_add_numbers with 5 and 3"
- **Hybrid (Fast)**: "Call hr_add_numbers with 5, 3, and let_ai_orchestrate=False"

---

## 🐍 Python-Specific Features

### Async/Await
All tools are async functions for efficient I/O:
```python
result = await hr_add_numbers_fast(5, 3)
```

### Type Hints
Clear return types for better IDE support:
```python
async def hr_add_numbers(...) -> dict | str:
    # Returns dict in AI mode, str in fast mode
```

### FastMCP Decorators
Clean, declarative tool registration:
```python
@app.tool(name="...", description="...")
async def my_tool(...):
    ...

@app.prompt(name="...", description="...")
async def my_prompt(...):
    ...
```

---

## 📝 Code Examples

### Creating a Custom Orchestrator
```python
@app.tool(
    name="my_custom_calculator",
    description="Custom calculation workflow",
)
async def my_custom_calculator(
    a: float,
    b: float,
    operation: str = "power_add",  # or "multiply_subtract"
) -> str:
    """Custom orchestrator with multiple workflows."""
    
    if operation == "power_add":
        result1 = await power(a, b)
        result2 = await add(a, b)
        total = result1 + result2
        return f"Power+Add: {result1} + {result2} = {total}"
    
    elif operation == "multiply_subtract":
        result1 = await multiply(a, b)
        result2 = await subtract(a, b)
        total = result1 - result2
        return f"Multiply-Subtract: {result1} - {result2} = {total}"
    
    return "Unknown operation"
```

---

## 🔍 Debugging Tips

### Enable Verbose Logging
```python
logging.basicConfig(level=logging.DEBUG)
```

### Check Which Mode Was Used
Look for these log messages:
- `"Tool called: add (AI orchestration)"` - AI is calling basic tools
- `"Tool orchestrator: hr_add_numbers_fast"` - Fast mode in use
- `"AI orchestration mode activated"` - Hybrid returned instructions
- `"Tool orchestration mode (default)"` - Hybrid executed directly

### Test Locally
```python
# Create a test file: test_hybrid.py
import asyncio
from calculator_server import hr_add_numbers, hr_add_numbers_fast

async def test():
    # Test fast mode
    result1 = await hr_add_numbers_fast(5, 3)
    print("Fast mode:", result1)
    
    # Test AI mode
    result2 = await hr_add_numbers(5, 3, let_ai_orchestrate=True)
    print("AI mode:", result2)
    
    # Test tool mode
    result3 = await hr_add_numbers(5, 3, let_ai_orchestrate=False)
    print("Tool mode:", result3)

asyncio.run(test())
```

---

## 🎓 Learning Path

1. **Start with World 2** - Understand how orchestrator tools work
2. **Explore World 1** - See how AI can follow instructions
3. **Master Hybrid** - Learn when to use each mode
4. **Create Custom Orchestrators** - Build your own workflows

---

## 🆚 PHP vs Python Comparison

| Feature | PHP Implementation | Python Implementation |
|---------|-------------------|----------------------|
| Framework | PhpMcp\Server | FastMCP |
| Async | Not used | async/await |
| Tool Decorator | `#[McpTool(...)]` | `@app.tool(...)` |
| Prompt Decorator | `#[McpPrompt(...)]` | `@app.prompt(...)` |
| Default Mode | `letAiOrchestrate=false` (fast) | `let_ai_orchestrate=True` (AI) |
| Return Types | `string\|array` | `dict \| str` |
| Logging | `LoggerInterface` | `logging` module |

**Note**: Python defaults to AI mode (`True`), while PHP defaults to fast mode (`false`). Adjust based on your use case!

---

## 📚 Additional Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)
