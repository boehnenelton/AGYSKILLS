# Gemini Tools & Function Calling Reference

## 1. Built-in Tools Schema Table

| Tool Type (`type`) | Parameters / Config Options | Produced Step Types |
| :--- | :--- | :--- |
| `google_search` | `search_types`: list of search grounding types | `google_search_call`, `google_search_result` |
| `code_execution` | None (sandboxed Python execution) | `code_execution_call`, `code_execution_result` |
| `url_context` | Ingests URL targets mentioned in prompt | `url_context_call`, `url_context_result` |
| `file_search` | `file_search_store_names`: list of store URIs | `file_search_call`, `file_search_result` |
| `mcp_server` | `server_url`: remote MCP server SSE endpoint | `mcp_server_tool_call`, `mcp_server_tool_result` |
| `computer_use` | System environment automation capabilities | `processing_call`, `processing_result` |

---

## 2. Function Calling Step Schemas

### 2.1 Model Request (`function_call` Step)
```json
{
  "type": "function_call",
  "id": "call_abc123",
  "name": "lookup_inventory",
  "arguments": {
    "sku": "SKU-123"
  }
}
```

### 2.2 Client Response (`function_result` Step)
```json
{
  "type": "function_result",
  "call_id": "call_abc123",
  "name": "lookup_inventory",
  "result": "{\"sku\": \"SKU-123\", \"price\": 12.50, \"stock\": 40}",
  "is_error": false
}
```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
