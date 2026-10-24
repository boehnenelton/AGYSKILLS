---
name: gemini-tooling-manager
description: >-
  Declare, configure, and execute custom client functions and built-in tools (google_search,
  code_execution, url_context, file_search, mcp_server, computer_use) using the Gemini
  Interactions API (client.interactions.create). Governs JSON Schema function definitions,
  dispatching and parsing function_call steps, serializing function_result payloads with
  call_id matching, handling parallel tool invocations, multi-round iterative tool loops,
  tool choice policies (auto, any, none, validated, allowed_tools), and hybrid pipelines
  combining built-in web grounding with custom execution tools. Use when defining function
  tools, executing tool-calling loops, handling parallel or chained function steps, or
  configuring built-in tools in Gemini Interactions API workflows. Do NOT use for basic
  text generation, stateful previous_interaction_id sessions without tools, or streaming
  lifecycle management (use gemini-interactions-core).
---

# gemini-tooling-manager (Layer 3 Domain Service & Tool Orchestrator)

## Summary

`gemini-tooling-manager` governs tool configuration, function declaration schemas, dispatch execution loops, and result serialization for the Google Gemini **Interactions API** using `google-genai`. It handles both **Custom Client Functions** (arbitrary Python/local handlers with JSON Schema declarations) and **Built-in Grounding Tools** (`google_search`, `code_execution`, `url_context`, `file_search`, `mcp_server`, `computer_use`). It also formalizes tool choice routing policies (`auto`, `any`, `none`, `validated`, and targeted `allowed_tools`).

## When to Use

- Declaring custom client tool schemas using standard JSON Schema definitions (`type: "function"`).
- Detecting and parsing `function_call` steps (`id`, `name`, `arguments`) in model outputs.
- Constructing and returning `function_result` steps (`call_id`, `name`, `result`, `is_error`) to the model.
- Handling parallel tool execution (multiple `function_call` steps emitted in a single model turn).
- Running multi-round iterative tool chains (tool -> result -> tool -> result -> final answer).
- Configuring built-in tools (`google_search`, `code_execution`, `url_context`, `file_search`, `mcp_server`).
- Enforcing tool choice behavior using `generation_config["tool_choice"]` (`auto`, `any`, `none`, or `allowed_tools`).
- Building hybrid pipelines that combine built-in search grounding with client-side computation tools.

## When NOT to Use

- Do NOT use for conversational session IDs, basic text generation, streaming SSE mechanics, or background polling (use `gemini-interactions-core`).
- Do NOT use for legacy `GenerateContentConfig(tools=[...])` methods (use `cli-ai-standardizer`).
- Do NOT use for terminal menu presentation or TUI rendering (use `bejson-tui-menu-builder`).

---

## 1. Custom Function Calling Schemas

### 1.1 Tool Declaration Specification
Declare function tools as dictionaries passed in the `tools` list of `client.interactions.create`. Each function definition requires `type: "function"`, `name`, `description`, and a `parameters` object complying with JSON Schema:

```python
FUNCTION_GET_WEATHER = {
    "type": "function",
    "name": "get_weather",
    "description": "Retrieve current weather conditions for a target city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city, e.g. 'Tokyo' or 'Paris'",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit preference.",
            },
        },
        "required": ["city"],
    },
}

FUNCTION_CALCULATE = {
    "type": "function",
    "name": "calculate",
    "description": "Evaluate an arithmetic expression.",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression, e.g. '12.5 * 7'",
            },
        },
        "required": ["expression"],
    },
}
```

---

## 2. Tool Execution & Multi-Turn Loop

### 2.1 The Canonical Interactions Tool Loop
In the Interactions API, the model outputs `function_call` steps. The client executes each call locally and returns a `function_result` step referencing `call_id` and the `previous_interaction_id`:

```python
import json

# Local handler implementations
def handle_get_weather(city: str, unit: str = "celsius") -> dict:
    return {"city": city, "temperature": 23, "condition": "sunny", "unit": unit}

def handle_calculate(expression: str) -> dict:
    return {"expression": expression, "result": eval(expression)}  # Use safe AST in production

TOOL_DISPATCH = {
    "get_weather": handle_get_weather,
    "calculate": handle_calculate,
}

# Turn 1: Initial user query
tools_list = [FUNCTION_GET_WEATHER, FUNCTION_CALCULATE]
interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="What is the weather in Tokyo and what is 15% of 85?",
    tools=tools_list,
)

# Step 2: Tool Resolution Loop (handles single, parallel, and chained calls)
while True:
    # Identify all function calls in the interaction steps
    function_calls = [
        step for step in (interaction.steps or [])
        if getattr(step, "type", None) == "function_call"
    ]
    if not function_calls:
        break  # Model has completed execution and generated final text

    # Execute all calls (supports parallel execution in a single turn)
    results_payload = []
    for call in function_calls:
        handler = TOOL_DISPATCH.get(call.name)
        try:
            output = handler(**(call.arguments or {})) if handler else {"error": "Tool not found"}
            is_error = "error" in output
        except Exception as err:
            output, is_error = {"error": str(err)}, True

        results_payload.append({
            "type": "function_result",
            "call_id": call.id,           # Must match call.id exactly
            "name": call.name,
            "result": json.dumps(output), # Stringified JSON result
            "is_error": is_error,
        })

    # Send results back using previous_interaction_id
    interaction = client.interactions.create(
        model="gemini-3-flash-preview",
        input=results_payload,
        tools=tools_list,
        previous_interaction_id=interaction.id,
    )

print("Final response:", interaction.output_text)
```

---

## 3. Tool Choice Policies (`generation_config["tool_choice"]`)

Control when and how the model invokes tools via `tool_choice`:

### 3.1 Policy Modes

```python
# Mode 1: Auto (default) - Model decides whether to call a tool or reply directly
generation_config={"tool_choice": "auto"}

# Mode 2: Any / Required - Model is forced to call at least one available tool
generation_config={"tool_choice": "any"}

# Mode 3: None - Model is forbidden from calling any tools (treats tools as disabled)
generation_config={"tool_choice": "none"}

# Mode 4: Validated - Tool calls are strictly validated against declarations
generation_config={"tool_choice": "validated"}
```

### 3.2 Specific Tool Whitelisting (`allowed_tools`)
Restrict tool selection to a subset of declared tools:

```python
generation_config={
    "tool_choice": {
        "allowed_tools": {
            "mode": "any",                 # "any" forces a call from the subset; "auto" allows direct text
            "tools": ["calculate"],        # Only "calculate" may be invoked; others are ignored
        }
    }
}
```

---

## 4. Built-in Tools Specification

The Interactions API provides first-class native tools that require no client-side execution loop:

### 4.1 Google Search Grounding (`google_search`)
Enables real-time web search grounding. The model emits `google_search_call` and `google_search_result` steps automatically:

```python
interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="What were the top news headlines today?",
    tools=[{"type": "google_search"}],
)
# Output includes grounded citations and links
```

### 4.2 Code Execution (`code_execution`)
Enables server-side sandboxed Python execution for rigorous calculations and data processing. Emits `code_execution_call` and `code_execution_result` steps:

```python
interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="Calculate the 50th Fibonacci number using Python.",
    tools=[{"type": "code_execution"}],
)
# Output text contains the computed result, backed by sandbox execution steps
```

### 4.3 URL Context (`url_context`)
Instructs the model to inspect and ingest arbitrary live URL contents directly:

```python
interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="Summarize the core premise of https://example.com",
    tools=[{"type": "url_context"}],
)
```

### 4.4 File Search (`file_search`) & Remote MCP (`mcp_server`)

```python
# File search store integration
tools=[{"type": "file_search", "file_search_store_names": ["stores/my-store-123"]}]

# Remote Model Context Protocol (MCP) server integration
tools=[{"type": "mcp_server", "server_url": "https://mcp.internal.net/sse"}]
```

---

## 5. Hybrid Built-in + Custom Function Pipelines

Combine native web search grounding with custom local calculation tools in the same interaction turn:

```python
hybrid_tools = [
    {"type": "google_search"},
    FUNCTION_CALCULATE,
]

interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="Search for the population of Iceland, then use calculate to divide it by 1000.",
    tools=hybrid_tools,
)

# If the model emits a function_call (for calculate), resolve it using the standard tool loop:
for step in interaction.steps or []:
    if step.type == "function_call":
        result = handle_calculate(**step.arguments)
        # Return result with previous_interaction_id
```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
