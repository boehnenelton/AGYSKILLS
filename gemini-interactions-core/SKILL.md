---
name: gemini-interactions-core
description: >-
  Build, manage, stream, and persist Gemini multi-turn conversations and sessions using
  the Google GenAI Interactions API (client.interactions.create, client.interactions.get,
  client.interactions.delete, client.interactions.cancel). Covers model selection,
  input payload structures, system instructions, generation config (thinking level,
  temperatures, stop sequences), stateful turns via previous_interaction_id, stateless
  step replay (store=False), streaming SSE event processing, background execution
  polling, and structured JSON output. Use when building or refactoring applications to
  use the Gemini Interactions API lifecycle, managing stateful session IDs, consuming
  streaming deltas, or executing background model tasks. Do NOT use for declaring custom
  function tools, managing tool dispatch loops, or configuring built-in search or code
  tools (use gemini-tooling-manager), or legacy GenerateContentConfig workflows
  (use cli-ai-standardizer).
---

# gemini-interactions-core (Layer 3 Domain Service & Lifecycle Manager)

## Summary

`gemini-interactions-core` provides canonical patterns, architecture, and runtime standards for building with the Google Gemini **Interactions API** using the unified `google-genai` SDK (`google.genai.Client`). It governs the full interaction lifecycle: synchronous generation, stateful conversational chaining via `previous_interaction_id`, stateless client-side history replay (`store=False`), real-time SSE streaming consumption (`stream=True`), asynchronous background execution (`background=True`), and resource persistence management (`get`, `cancel`, `delete`).

## When to Use

- Initializing and executing interactions via `client.interactions.create(...)`.
- Maintaining stateful multi-turn dialogs across turns using server-managed `previous_interaction_id`.
- Replaying explicit step histories (`user_input`, `thought`, `model_output`, etc.) in stateless environments when `store=False`.
- Consuming real-time streaming tokens and step lifecycle events (`step.start`, `step.delta`, `step.stop`, `interaction.completed`).
- Running long-running tasks in background mode (`background=True`) with deterministic polling via `client.interactions.get(id)`.
- Enforcing structured schema responses using `response_format` and `response_mime_type="application/json"`.
- Tuning reasoning depth via `thinking_level` (`"minimal"`, `"low"`, `"medium"`, `"high"`).

## When NOT to Use

- Do NOT use for declaring function calling schemas, dispatching tool execution, or returning `function_result` payloads (use `gemini-tooling-manager`).
- Do NOT use for configuring built-in tools like `google_search`, `code_execution`, `url_context`, or `mcp_server` (use `gemini-tooling-manager`).
- Do NOT use for legacy `client.models.generate_content` / `GenerateContentConfig` SDK methods (use `cli-ai-standardizer`).
- Do NOT use for multi-skill workflow coordination or turn gating (use `skill-chain-coordinator`).

---

## 1. Architectural Invariants & Client Setup

### 1.1 SDK Initialization & API Key Sourcing
Always initialize the client using the official `google-genai` package. Never hardcode API keys or host paths in business logic; source credentials from canonical BEJSON stores (e.g. `/storage/emulated/0/.env/secure/secureenv_file.json`) using O(1) Field Map Caching:

```python
from google import genai

# Standard Client Initialization
client = genai.Client(api_key=resolved_gemini_api_key)
```

### 1.2 Supported Models
- Primary production models: `gemini-3-flash-preview`, `gemini-3.8-flash`, `gemini-3.8-pro`.
- Always specify the model name explicitly in `client.interactions.create(model=...)`.

---

## 2. Core Interaction Lifecycle Patterns

### 2.1 Basic Synchronous Turn
The baseline call takes `model` and `input`. The input can be a raw string, a `Content` object, or a list of `Step` dictionaries.

```python
interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="Explain quantum entanglement in two sentences.",
    system_instruction="You are a theoretical physicist. Be rigorous but concise.",
    generation_config={
        "temperature": 0.3,
        "max_output_tokens": 500,
        "thinking_level": "medium",  # "minimal" | "low" | "medium" | "high"
    },
)

# Top-level interaction fields
interaction_id = interaction.id
interaction_status = interaction.status  # "completed" | "in_progress" | "failed"
text_output = interaction.output_text
token_usage = interaction.usage
# usage: total_input_tokens, total_output_tokens, total_thought_tokens, total_tokens
```

### 2.2 Stateful Multi-Turn Chaining (`previous_interaction_id`)
When `store=True` (the default), interactions are persisted server-side. Multi-turn conversations require passing only the new turn input and the previous interaction ID:

```python
# Turn 1
first_interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="My secret code is APEX-99. Acknowledge briefly.",
    store=True,
)

# Turn 2: Server automatically resolves previous conversational context
second_interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="What is my secret code?",
    previous_interaction_id=first_interaction.id,
    store=True,
)
print(second_interaction.output_text)  # "Your secret code is APEX-99."
```

### 2.3 Stateless History Replay (`store=False`)
In ephemeral or privacy-sensitive environments where server-side storage is prohibited, set `store=False`. The client manages history by accumulating steps and replaying the full step array on subsequent calls:

```python
# Turn 1: Stateless
turn1_input = [{"type": "user_input", "content": [{"type": "text", "text": "Remember 42."}]}]
turn1_result = client.interactions.create(
    model="gemini-3-flash-preview",
    input=turn1_input,
    store=False,
)

# Accumulate steps client-side: user_input -> generated steps -> next user_input
full_history = [
    *turn1_input,
    *[step.model_dump(mode="json", exclude_none=True, by_alias=True) for step in turn1_result.steps],
    {"type": "user_input", "content": [{"type": "text", "text": "What number did I say?"}]},
]

# Turn 2: Replay full history without previous_interaction_id
turn2_result = client.interactions.create(
    model="gemini-3-flash-preview",
    input=full_history,
    store=False,
)
```

---

## 3. Streaming & Background Execution

### 3.1 Server-Sent Events (SSE) Streaming (`stream=True`)
When `stream=True`, `client.interactions.create` returns an iterable of SSE stream events. Consume deltas in real-time:

```python
stream_iterator = client.interactions.create(
    model="gemini-3-flash-preview",
    input="Stream a countdown from 5 to 1.",
    stream=True,
)

for event in stream_iterator:
    # event.event_type: "step.start" | "step.delta" | "step.stop" | "interaction.completed"
    if event.event_type == "step.delta":
        delta_payload = getattr(event, "delta", None)
        # Inspect content text chunk if present
        if delta_payload and hasattr(delta_payload, "content") and delta_payload.content:
            for content_chunk in delta_payload.content:
                if hasattr(content_chunk, "text") and content_chunk.text:
                    print(content_chunk.text, end="", flush=True)
    elif event.event_type == "interaction.completed":
        final_interaction = event.interaction
```

### 3.2 Asynchronous Background Execution (`background=True`)
For intensive queries or batch operations, delegate execution to the background and poll status until completion:

```python
import time

background_job = client.interactions.create(
    model="gemini-3-flash-preview",
    input="Conduct a deep comparative analysis of modern consensus algorithms.",
    background=True,
    store=True,  # Mandatory for background retrieval
)

job_id = background_job.id
terminal_statuses = {"completed", "failed", "cancelled", "incomplete"}

# Polling loop
current_job = background_job
while current_job.status not in terminal_statuses:
    time.sleep(2.0)
    current_job = client.interactions.get(job_id)

if current_job.status == "completed":
    print(current_job.output_text)
else:
    print(f"Job failed with status: {current_job.status}, errors: {current_job.errors}")
```

### 3.3 Resource Management: Get, Cancel, and Delete
Manage stored interactions explicitly:

```python
# Fetch an existing interaction by ID
interaction_record = client.interactions.get(interaction_id)

# Cancel an active in-progress or background interaction
client.interactions.cancel(interaction_id)

# Delete an interaction from server storage
client.interactions.delete(interaction_id)
```

---

## 4. Structured Output Enforcement

Enforce strict JSON schemas without conversational wrappers using `response_format` and `response_mime_type`:

```python
schema_definition = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["ok", "degraded", "error"]},
        "metric_score": {"type": "number"},
        "summary": {"type": "string"},
    },
    "required": ["status", "metric_score", "summary"],
}

interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="Provide current telemetry status.",
    response_format=schema_definition,
    response_mime_type="application/json",
)

# Output text is guaranteed valid JSON complying with schema_definition
import json
payload = json.loads(interaction.output_text)
```

---

## 5. Step Taxonomy in Interaction Responses

Every `interaction.steps` list contains ordered execution steps:

| Step Type (`step.type`) | Class Name | Description | Key Attributes |
| :--- | :--- | :--- | :--- |
| `user_input` | `UserInputStep` | The user's input prompt | `content` |
| `thought` | `ThoughtStep` | Internal model reasoning chain | `summary`, `content` |
| `model_output` | `ModelOutputStep` | Generated response text or media | `content`, `error` |
| `function_call` | `FunctionCallStep` | Model request to invoke a client tool | `id`, `name`, `arguments` |
| `function_result` | `FunctionResultStep` | Client tool execution response | `call_id`, `name`, `result`, `is_error` |
| `google_search_call` | `GoogleSearchCallStep` | Triggered Google Search query | `queries` |
| `google_search_result` | `GoogleSearchResultStep` | Search grounding results and citations | `results` |
| `code_execution_call` | `CodeExecutionCallStep` | Generated Python code to execute | `code` |
| `code_execution_result` | `CodeExecutionResultStep` | Sandbox execution outcome | `outcome`, `output` |
| `url_context_call` | `URLContextCallStep` | Target URL to fetch context from | `url` |
| `url_context_result` | `URLContextResultStep` | Content extracted from URL | `content` |

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
