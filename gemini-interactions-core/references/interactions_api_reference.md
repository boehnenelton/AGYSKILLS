# Gemini Interactions API Reference

## 1. Parameters for `client.interactions.create(...)`

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `model` | `str` | Yes | Target model ID (e.g. `"gemini-3-flash-preview"`, `"gemini-3.8-flash"`). |
| `input` | `str \| Content \| list[Step]` | Yes | User prompt, content object, or full historical step array. |
| `system_instruction`| `str` | No | System-level behavior guidance for the model. |
| `generation_config` | `dict` | No | Tuning dictionary: `temperature`, `max_output_tokens`, `stop_sequences`, `thinking_level`, `tool_choice`. |
| `previous_interaction_id` | `str` | No | ID of preceding turn to continue a stateful conversation thread. |
| `store` | `bool` | No | `True` (default) persists server-side; `False` enables stateless client-managed history. |
| `stream` | `bool` | No | When `True`, returns an iterable of SSE stream events (`InteractionSSEEvent`). |
| `background` | `bool` | No | When `True`, runs asynchronously; retrieve status via `client.interactions.get(id)`. |
| `response_format` | `dict` | No | JSON schema enforcing strict structured output structure. |
| `response_mime_type` | `str` | No | Required if `response_format` is provided (`"application/json"`). |
| `tools` | `list[dict]` | No | Declarations of client functions and built-in tools. |

---

## 2. Server Response Structure (`Interaction`)

```python
interaction.id                  # Unique string ID, e.g. "v1_..."
interaction.status              # "completed" | "in_progress" | "failed" | "cancelled"
interaction.output_text         # Concatenated final text response
interaction.steps               # List of Step objects (ordered sequence of execution)
interaction.usage               # Usage object with token consumption metrics
```

### Usage Breakdown
```python
interaction.usage.total_input_tokens
interaction.usage.total_output_tokens
interaction.usage.total_thought_tokens
interaction.usage.total_tokens
```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
