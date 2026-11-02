#!/usr/bin/env python3
"""
Production-grade LiteRT-LM HTTP Server & Proxy.
Exposes OpenAI-compatible endpoints with selectable tool-context lifecycle modes.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional

try:
    from fastapi import FastAPI, HTTPException, Request, Response
    from fastapi.responses import JSONResponse, StreamingResponse
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print("[ERROR] FastAPI, Uvicorn, and Pydantic are required to run this server.", file=sys.stderr)
    print("Install via: pip install fastapi uvicorn pydantic", file=sys.stderr)
    sys.exit(1)

try:
    import litert_lm
except ImportError:
    print("[ERROR] litert_lm runtime not found. Install via: pip install litert-lm-api", file=sys.stderr)
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("litert_server")

# Configuration Constants
DEFAULT_MODEL_PATH = os.getenv("LITERT_MODEL_PATH", "models/gemma-4-e2b.litertlm")
DEFAULT_CACHE_DIR = os.getenv("LITERT_CACHE_DIR", str(Path(DEFAULT_MODEL_PATH).parent))
DEFAULT_HOST = os.getenv("LITERT_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.getenv("LITERT_PORT", "8000"))
DEFAULT_TOOL_MODE = os.getenv("LITERT_TOOL_CONTEXT_MODE", "separate")
DEFAULT_MAX_TOKENS = int(os.getenv("LITERT_MAX_NUM_TOKENS", "32768"))
DEFAULT_OUTPUT_TOKENS = int(os.getenv("LITERT_MAX_OUTPUT_TOKENS", "4096"))
DEFAULT_MAX_TOOL_TOKENS = int(os.getenv("LITERT_MAX_TOOL_RESPONSE_TOKENS", "4096"))
DEFAULT_SAFETY_MARGIN = int(os.getenv("LITERT_CONTEXT_SAFETY_MARGIN", "1024"))

# Pydantic Request Models
class ChatMessage(BaseModel):
    role: str
    content: Optional[Any] = None
    name: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "default"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.2
    top_p: Optional[float] = 0.95
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    tools: Optional[List[Dict[str, Any]]] = None
    reasoning_effort: Optional[str] = "high"

class LiteRTServerState:
    def __init__(self, model_path: str, tool_context_mode: str):
        self.model_path = model_path
        self.tool_context_mode = tool_context_mode
        self.engine: Optional[litert_lm.Engine] = None
        self.active_conversation: Optional[litert_lm.Conversation] = None
        self.lock = asyncio.Lock()
        self.active_turn_count = 0

    def initialize_engine(self):
        logger.info(f"Loading LiteRT-LM model from: {self.model_path}")
        self.engine = litert_lm.Engine(
            model_path=self.model_path,
            backend=litert_lm.Backend.GPU(gpu_decode_steps_per_sync=4),
            enable_speculative_decoding=True,
            use_ringbuffers_local_attention=True,
            cache_dir=DEFAULT_CACHE_DIR
        )
        logger.info("Engine successfully initialized with GPU delegate.")

app = FastAPI(title="LiteRT-LM Selectable Tool-Context Server", version="1.0.0")
state: Optional[LiteRTServerState] = None

@app.on_event("startup")
async def startup_event():
    global state
    state.initialize_engine()

@app.on_event("shutdown")
async def shutdown_event():
    global state
    if state and state.active_conversation:
        state.active_conversation.close()
    if state and state.engine:
        state.engine.__exit__(None, None, None)
    logger.info("Server shutdown complete.")

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "model_path": state.model_path,
        "tool_context_mode": state.tool_context_mode,
        "max_context_tokens": DEFAULT_MAX_TOKENS,
        "backend": "GPU (OpenGLES/Vulkan)"
    }

@app.post("/v1/conversation/cancel")
async def cancel_active_conversation():
    if state and state.active_conversation:
        state.active_conversation.cancel_process()
        return {"status": "cancelled"}
    return {"status": "no_active_conversation"}

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    if state.lock.locked():
        raise HTTPException(status_code=429, detail="Concurrent inference requests are not permitted.")

    async with state.lock:
        # Context Preflight Check
        raw_char_count = sum(len(str(m.content or "")) for m in req.messages)
        est_tokens = raw_char_count // 4
        output_tokens = req.max_tokens or DEFAULT_OUTPUT_TOKENS
        projected_demand = est_tokens + output_tokens + DEFAULT_SAFETY_MARGIN

        if projected_demand > DEFAULT_MAX_TOKENS:
            raise HTTPException(
                status_code=413,
                detail=f"Context overflow: projected demand {projected_demand} exceeds limit {DEFAULT_MAX_TOKENS}."
            )

        # Context Mode: Separate vs Merged
        if state.tool_context_mode == "separate" or state.active_conversation is None:
            if state.active_conversation:
                state.active_conversation.close()
            state.active_conversation = state.engine.create_conversation(
                thinking_config=litert_lm.ThinkingConfig(
                    enable_thinking=(req.reasoning_effort != "none"),
                    thinking_token_budget=1024
                )
            )

        last_user_message = next((m.content for m in reversed(req.messages) if m.role == "user"), "")

        if req.stream:
            async def event_generator() -> AsyncIterator[str]:
                for chunk in state.active_conversation.send_message_async(last_user_message):
                    content_list = chunk.get("content", [])
                    delta_text = ""
                    for c in content_list:
                        if c.get("type") == "text":
                            delta_text += c.get("text", "")
                    
                    if delta_text:
                        sse_payload = {
                            "choices": [{"delta": {"content": delta_text}, "index": 0}]
                        }
                        yield f"data: {json.dumps(sse_payload)}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(event_generator(), media_type="text/event-stream")

        # Synchronous execution path
        response = state.active_conversation.send_message(last_user_message)
        text_out = response.content[0].text if response.content else ""

        return {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": req.model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": text_out},
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": est_tokens,
                "completion_tokens": len(text_out) // 4,
                "total_tokens": est_tokens + (len(text_out) // 4)
            }
        }

def main():
    global state
    parser = argparse.ArgumentParser(description="LiteRT-LM Selectable Tool-Context Server")
    parser.add_argument("--model-path", default=DEFAULT_MODEL_PATH, help="Path to .litertlm model file")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host network interface")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to listen on")
    parser.add_argument("--tool-context-mode", choices=["separate", "merged"], default=DEFAULT_TOOL_MODE, help="Tool context mode")
    args = parser.parse_args()

    state = LiteRTServerState(args.model_path, args.tool_context_mode)
    logger.info(f"Starting server on http://{args.host}:{args.port} (Mode: {args.tool_context_mode})")
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

if __name__ == "__main__":
    main()
