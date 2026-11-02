---
name: litert-lm-server
description: >-
  Scaffold, configure, and operate high-performance local LiteRT-LM inference servers
  and OpenAI/Gemini-compatible proxy architectures. Implements selectable tool-context
  modes (separate vs. merged KV caches), dual-engine fallback routing, context-window
  preflight checks, Gemma reasoning/thinking controls, native workspace tool execution,
  and SSE streaming keep-alives across Linux, macOS, Windows, and Android Termux.
  Use when deploying local LLM endpoints, building OpenAI-compatible LiteRT proxies,
  configuring on-device tool calling loops, or tuning edge inference budgets.
  Do NOT use for high-level multi-skill DAG orchestration (use skill-chain-coordinator),
  direct in-process C FFI execution without network transport (via native C API bindings),
  or cloud-only Gemini API pipelines without local runtimes (use gemini-interactions-core).
---

# litert-lm-server (Layer 3 Service & Server Orchestrator)

## Summary

`litert-lm-server` is the canonical Layer 3 service skill for engineering, scaffolding, and managing local HTTP inference servers and proxy middleware powered by Google AI Edge's **LiteRT-LM** engine. It establishes enterprise-grade server architectures that expose OpenAI-compatible (`/v1/chat/completions`, `/v1/models`) and Gemini-compatible (`/v1beta/models/{model}:generateContent`) endpoints backed by pre-converted FlatBuffer models (`.litertlm`, such as Gemma 4 E2B, E4B, and 12B).

The skill formalizes critical edge-inference operating modes:
- **Selectable Tool-Context Lifecycle:** Switching between isolated stateless tool turns (`separate`) and persistent in-memory KV-cache continuation (`merged`).
- **Dual-Model Fallback Delegation:** Routing complex client chat to a high-capacity primary model while delegating autonomous tool executions to a dedicated lightweight engine.
- **Defensive Edge Inference Guardrails:** Context-window preflight budgeting, incoming tool-result truncation, malformed tool argument validation/retries, and server-sent event (SSE) prefill keep-alives.

## When to Use

- Architecting, scaffolding, or deploying an OpenAI- or Gemini-compatible HTTP inference proxy server for local `.litertlm` models using FastAPI, Uvicorn, or the native `litert-lm serve` daemon.
- Configuring tool execution loops with selectable context lifecycle policies (`--tool-context-mode separate|merged`).
- Implementing dual-model routing where primary conversational inference runs on GPU/WebGPU and automatic tool loops run on a secondary CPU engine.
- Establishing context-window overflow preflight validation (`messages + tools + completion_reserve + safety_margin`).
- Configuring Gemma thinking/reasoning token budgets (`ThinkingConfig`) and separating thought channels from user-facing completion text.
- Integrating bounded native workspace filesystem tools (`find`, `grep`, `read`, `write`, `line_count`) with path traversal guards and command approval workflows.

## When NOT to Use

- Executing dependency-ordered multi-skill DAG workflows across separate project domains (use `skill-chain-coordinator`).
- Direct, in-process Python C FFI bindings without network or HTTP proxy overhead (use direct `litert_lm.Engine` and `litert_lm.Conversation` code).
- Authoring bare-bones static UI templates or layout components (use `template-literal-skeleton` or `behtml-layout-builder`).
- Interacting exclusively with Google Cloud remote Gemini endpoints without any local edge model runtime (use `gemini-interactions-core`).
- Auditing BEJSON relational schemas or field map caches (use `policy-bejson-auditor`).

---

## 1. Architectural Guardrails & Server Topologies

```
┌────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL CLIENT LAYER                           │
│  - OpenAI Python / Node.js SDK                                         │
│  - Google GenAI SDK (api_version="v1beta")                             │
│  - Web Browser / Chat UI / Local Autonomous Agent                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / SSE (Port 8000 / 9379)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   LITERT-LM PROXY / SERVER GATEWAY                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ Single-Inference Request Lock & Concurrency Arbiter (HTTP 429)   │  │
│  ├──────────────────────────────────────────────────────────────────┤  │
│  │ Context Preflight Evaluator:                                     │  │
│  │ Prompt + Tool Schemas + Output Budget + Margin <= Engine Ceiling │  │
│  ├──────────────────────────────────────────────────────────────────┤  │
│  │ Tool Context Arbiter:                                            │  │
│  │  ├── "separate" mode: Fresh LiteRT conversation per tool turn    │  │
│  │  └── "merged" mode: Persistent live KV cache across tool turns   │  │
│  ├──────────────────────────────────────────────────────────────────┤  │
│  │ Dual-Engine Router: Primary Model (GPU) vs Tool Model (CPU)      │  │
│  └────────────────────────────────┬─────────────────────────────────┘  │
└───────────────────────────────────┼────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     LITERT-LM INFERENCE RUNTIMES                       │
│  ┌─────────────────────────────────┐ ┌──────────────────────────────┐  │
│  │      PRIMARY MODEL RUNTIME      │ │    DEDICATED TOOL RUNTIME    │  │
│  │  - Model: Gemma 4 E2B / 12B     │ │  - Model: Gemma 4 E2B / E4B  │  │
│  │  - Delegate: GPU (OpenGLES/Drift│ │  - Delegate: CPU (XNNPACK)   │  │
│  │  - Mode: Chat / Client Functions│ │  - Mode: Auto Workspace Tools│  │
│  └─────────────────────────────────┘ └──────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Concurrency & Request Serialization
On edge devices, mobile GPUs, and unified-memory SOCs, running concurrent autoregressive inference passes causes memory bandwidth thrashing and out-of-memory (OOM) crashes. 
- The server enforces a **Strict Single-Request Lock** (`asyncio.Lock`).
- Any concurrent incoming request while inference is active immediately receives `HTTP 429 Too Many Requests`.

### 1.2 Context Overflow Preflight Guard
Before allocating tensor memory or launching inference, the server calculates total projected token demand:
$$\text{Demand} = \text{Tokens}_{\text{messages}} + \text{Tokens}_{\text{tools}} + \text{Tokens}_{\text{max\_output}} + \text{Margin}_{\text{safety}}$$
- If $\text{Demand} > \text{Capacity}_{\text{engine}}$, the server rejects the request immediately with `HTTP 413 Payload Too Large`, preventing unrecoverable C runtime segmentation faults.

### 1.3 Tool Context Lifecycle Modes
1. **Separate Mode (`--tool-context-mode separate`, Default):**
   - A fresh `litert_lm.Conversation` is instantiated for each tool turn.
   - History is re-prefilled from scratch.
   - Eliminates carrying contaminated tool-protocol syntax forward; guarantees session isolation.
2. **Merged Mode (`--tool-context-mode merged`):**
   - Keeps one live `litert_lm.Conversation` instance and retains the active KV cache in VRAM.
   - Yields fast incremental prefill and preserves chain-of-thought tokens across turns.
   - Requires malformed argument detection and emergency reset fallback if protocol tokens leak into arguments.

---

## 2. Server Configuration Reference

Comprehensive environment variables and CLI parameters are detailed in [`references/server_architecture_and_options.md`](./references/server_architecture_and_options.md).

### 2.1 Authoritative Environment Matrix

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `LITERT_MODEL_PATH` | `models/gemma-4-e2b.litertlm` | Filesystem path to the primary `.litertlm` model bundle. |
| `LITERT_CACHE_DIR` | Auto (`parent(MODEL_PATH)`) | Directory for compiled GPU shaders and delegate caches. |
| `LITERT_HOST` | `127.0.0.1` | Network interface to bind HTTP listener. |
| `LITERT_PORT` | `8000` | TCP port for incoming REST requests. |
| `LITERT_TOOL_CONTEXT_MODE` | `separate` | Tool context strategy: `separate` (safe) or `merged` (fast). |
| `LITERT_MAX_NUM_TOKENS` | `32768` | Global context capacity configured on the primary engine. |
| `LITERT_MAX_OUTPUT_TOKENS` | `4096` | Default output token limit when request omits `max_tokens`. |
| `LITERT_MAX_TOOL_RESPONSE_TOKENS`| `4096` | Hard truncation ceiling for incoming tool execution outputs. |
| `LITERT_CONTEXT_SAFETY_MARGIN` | `1024` | Reserved headroom buffer for prompt templating and overhead. |
| `LITERT_INFERENCE_TIMEOUT` | `180` | Maximum seconds allowed for synchronous tool turns before cancel. |
| `LITERT_REASONING_EFFORT` | `high` | Thinking level: `none` (0), `low` (512), `medium` (1024), `high` (2048). |
| `LITERT_CONSTRAINED_DECODING`| `1` | Enables `LL_GUIDANCE` grammar masking when tools are present. |
| `LITERT_TOOL_ROUTING_ENABLED`| `1` | Enables dedicated secondary model routing for workspace tools. |
| `LITERT_TOOL_MODEL_PATH` | `models/gemma-4-e2b.litertlm` | Model bundle path for the dedicated secondary tool worker. |
| `LITERT_TOOL_BACKEND` | `cpu` | Hardware delegate for the tool model (preserves GPU memory). |

---

## 3. Tool Execution Protocols & Defensive Boundaries

Full specifications of native filesystem tools and security sandboxing are detailed in [`references/workspace_tools_and_security.md`](./references/workspace_tools_and_security.md).

### 3.1 Two Disjoint Tool Tiers
The server distinguishes strictly between two tool models:
1. **Client Function Tools (OpenAI Style):**
   - Declared in the request's `tools` array.
   - LiteRT-LM returns function call candidates (`tool_calls`).
   - The API client executes the function on its own host and resubmits via `role: "tool"`.
2. **Native Workspace Tools (Server-Side Execution):**
   - Activated via `workspace_tools: true` with a specified `workspace_path`.
   - Executed automatically by the server inside the LiteRT loop using bounded Python primitives (`find`, `grep`, `read`, `write`, `line_count`).
   - The model iterates internally; SSE clients receive periodic keep-alives and the final answer.

### 3.2 Security Sandbox Rules for Workspace Tools
- **Path Resolution:** Every relative path is resolved against `workspace_path`. Traversals containing `..` or symbolic links resolving outside the root directory are aborted with permission errors.
- **Output Truncation:** If a tool returns a 100,000-line grep result, the server truncates the payload to `LITERT_MAX_TOOL_RESPONSE_TOKENS` before inserting into conversation history.
- **Protocol Leak Interception:** Tool arguments are scanned for hallucinated control sequences (`<start_of_turn>`, `user]`, `call:`). Detected leaks trigger automatic context pruning and retry.
- **Command Approvals:** Any mutating command or arbitrary shell execution requires an interactive client approval token (`workspace_shell_approval_id`).

---

## 4. Gemma Thinking & Reasoning Configuration

LiteRT-LM maps requested reasoning effort into token-budget allocations passed to `litert_lm.ThinkingConfig`:

| Reasoning Effort | Token Budget | Application Profile |
| :--- | :--- | :--- |
| `none` (`off`, `0`) | `0` (Disabled) | Fast classification, low-latency conversational QA, tool dispatch. |
| `minimal` | `256` | Minor sanity checks and simple parameter extractions. |
| `low` | `512` | Straightforward code edits and short logic derivations. |
| `medium` | `1024` | Multi-step mathematical calculations and architectural reasoning. |
| `high` | `2048` | Complex algorithmic problem-solving and deep adversarial analysis. |
| `xhigh` | `4096` | Maximum depth verification and exhaustive planning. |

Internal thinking tokens generated by Gemma are routed through the native `thought` channel and stripped from standard user completion text unless specifically requested via debug metadata.

---

## 5. Standard Scaffolding Workflow

When asked to scaffold or deploy a LiteRT-LM server:

1. **Verify Runtime & Model Assets:**
   Confirm Python 3.10+, `litert-lm-api` (or `litert-lm`), and valid `.litertlm` FlatBuffer files exist in the model cache.
2. **Select Context Strategy:**
   - Default to `separate` mode for autonomous coding agents with large file outputs.
   - Select `merged` mode for interactive low-latency chat sessions with minimal tool calls.
3. **Execute Server Scaffold:**
   Deploy [`scripts/litert_server_scaffold.py`](./scripts/litert_server_scaffold.py) or launch `litert-lm serve` with verified flags.
4. **Health Verification Gate:**
   Query `GET /health` to verify GPU memory allocation, KV-cache limits, and delegate readiness before routing user traffic.
