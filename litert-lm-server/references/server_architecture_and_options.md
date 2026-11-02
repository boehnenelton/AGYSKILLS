# LiteRT-LM Server Architecture & Configuration Reference

This reference document details the runtime architecture, request lifecycles, and configuration options for building or hosting an OpenAI- and Gemini-compatible inference server using LiteRT-LM.

---

## 1. Request Lifecycle & Concurrency Protocol

```
Client Request (POST /v1/chat/completions)
       │
       ▼
[1] Concurrency Lock (asyncio.Lock) ──(Acquired? No)──> Return HTTP 429
       │ (Yes)
       ▼
[2] Context-Window Preflight Check
    Calculates: messages + tool schemas + max_tokens + safety_margin
    Is Demand > Engine Capacity? ──────────────────────> Return HTTP 413
       │ (Within budget)
       ▼
[3] Tool Context Mode Router
    ├── "separate": Instantiate new Conversation; re-prefill full history.
    └── "merged":   Reuse live Conversation; append delta turns into KV-cache.
       │
       ▼
[4] Hardware Execution (GPU/CPU)
    ├── Non-Streaming: Synchronous execution with timeout watchdog.
    └── Streaming (SSE): Emit token deltas + periodic keep-alive comments.
       │
       ▼
[5] Tool Call Detection & Interception
    ├── Model Emitted Tool Call: Return candidate to client (or execute if workspace tool).
    └── Final Text Generated: Format completion payload; release Concurrency Lock.
```

---

## 2. Environment Variables & Runtime Parameters

All environment variables can be declared in a local `.env` or exported in the host shell before starting the server.

### 2.1 Model & Delegate Configuration
- `LITERT_MODEL_PATH`: Path to the `.litertlm` FlatBuffer bundle (e.g. `~/.litert-lm/models/gemma-4-e2b/model.litertlm`).
- `LITERT_CACHE_DIR`: Directory where LiteRT stores compiled OpenGLES/Vulkan shader binaries or XNNPACK micro-kernels.
- `LITERT_HOST`: Listening interface (`127.0.0.1` for local-only, `0.0.0.0` for container/network binding). Default: `127.0.0.1`.
- `LITERT_PORT`: TCP port for the HTTP server. Default: `8000`.

### 2.2 Context & Memory Bounds
- `LITERT_MAX_NUM_TOKENS`: Maximum total sequence length allocated in the engine (e.g. `32768`).
- `LITERT_MAX_OUTPUT_TOKENS`: Maximum completion tokens if not specified in the client request. Default: `4096`.
- `LITERT_MAX_TOOL_RESPONSE_TOKENS`: Hard limit on the size of tool outputs inserted into conversation history. Default: `4096`.
- `LITERT_CONTEXT_SAFETY_MARGIN`: Token headroom buffer reserved for prompt templates and tokenizer estimation error. Default: `1024`.

### 2.3 Tool Context Strategy
- `LITERT_TOOL_CONTEXT_MODE`:
  - `separate`: Destroys the conversation after each tool turn and rebuilds on subsequent turns. Highly resilient against syntax errors.
  - `merged`: Retains conversation state and KV-cache across tool turns. Delivers lower latency but requires prompt monitoring.

### 2.4 Reasoning & Inference Safeguards
- `LITERT_REASONING_EFFORT`: Thinking depth (`none`, `minimal`, `low`, `medium`, `high`, `xhigh`).
- `LITERT_INFERENCE_TIMEOUT`: Maximum seconds before aborting a stalled inference pass. Default: `180`.
- `LITERT_MALFORMED_TOOL_RETRIES`: Number of automatic retries on detected tool-call JSON parsing failures. Default: `1`.
- `LITERT_CONSTRAINED_DECODING`: Enables grammar-constrained decoding via `LL_GUIDANCE` when tools are active. Default: `1`.

---

## 3. Wire API Endpoints

### 3.1 `GET /health`
Returns runtime status, GPU delegate state, memory allocation, and active conversation cache metrics:
```json
{
  "status": "healthy",
  "model": "gemma-4-e2b-it",
  "backend": "GPU",
  "context_capacity": 32768,
  "estimated_used_tokens": 1420,
  "tool_context_mode": "separate",
  "constrained_decoding": true
}
```

### 3.2 `POST /v1/chat/completions`
OpenAI-compatible chat completion endpoint supporting standard parameters (`model`, `messages`, `temperature`, `max_tokens`, `stream`, `tools`, `tool_choice`).

### 3.3 `POST /v1/conversation/cancel`
Interrupts active inference immediately via `conversation.cancel_process()`.
