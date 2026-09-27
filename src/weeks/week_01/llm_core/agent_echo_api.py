"""Week 1 | Session 3 | File: agent_echo_api.py
Topic: FastAPI — building typed HTTP APIs with Pydantic schemas.

Why this matters:
  - Every agent system needs a way to receive inputs and return outputs over HTTP.
  - FastAPI + Pydantic gives you automatic request validation, response typing,
    and interactive docs at /docs for free.
  - This becomes the "agent service" that n8n, LangChain, and other tools call.

Concepts taught:
  1. FastAPI app and route definition
  2. Pydantic request/response models (automatic input validation)
  3. HTTP status codes and error handling
  4. Multiple endpoints on one app
  5. Interactive docs at /docs

Run:
    uvicorn src.weeks.week_01.llm_core.agent_echo_api:app --reload --port 8000

Then visit:
    http://localhost:8000/docs   → interactive Swagger UI
    http://localhost:8000/health → health check

Test with curl:
    curl -s -X POST http://localhost:8000/agent/echo \\
         -H "Content-Type: application/json" \\
         -d '{"message": "hello"}' | python3 -m json.tool
"""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Agent Echo API",
    description="Week 1 teaching API — demonstrates FastAPI + Pydantic patterns",
    version="0.1.0",
)

# ─────────────────────────────────────────────
# IN-MEMORY TASK REGISTRY
# ─────────────────────────────────────────────
# Simple list that accumulates task IDs submitted via /agent/task.
# In a real system this would be a database or cache.
# This demonstrates how app-level state works without a DB.
_submitted_task_ids: list[str] = []


# ─────────────────────────────────────────────
# CONCEPT: Pydantic request and response models
# ─────────────────────────────────────────────
# FastAPI reads the type annotations and automatically:
#   - Parses JSON body into the model
#   - Validates every field
#   - Returns a 422 error with details if validation fails
#   - Documents the schema in /docs
class EchoRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)


class EchoResponse(BaseModel):
    ok: bool
    agent_reply: str
    message_length: int


class TaskRequest(BaseModel):
    task: str = Field(min_length=5)
    priority: Literal["low", "medium", "high"] = "medium"


class TaskResponse(BaseModel):
    task_id: str
    status: str
    priority: str
    message: str


class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded"]
    version: str


# ─────────────────────────────────────────────
# CONCEPT: Route definitions
# ─────────────────────────────────────────────
# @app.get / @app.post declares a URL + HTTP method.
# The function's return value is automatically serialized to JSON.
@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Simple health check — always call this first to verify the service is up."""
    return HealthResponse(status="healthy", version="0.1.0")


# ─────────────────────────────────────────────
# CONCEPT: POST endpoint with validated body
# ─────────────────────────────────────────────
@app.post("/agent/echo", response_model=EchoResponse)
def agent_echo(payload: EchoRequest) -> EchoResponse:
    """
    Echo endpoint — receives a message and returns a processed reply.
    FastAPI validates EchoRequest automatically before this function runs.
    If `message` is empty, FastAPI returns 422 before reaching this code.
    """
    return EchoResponse(
        ok=True,
        agent_reply=f"received:{payload.message}",
        message_length=len(payload.message),
    )


# ─────────────────────────────────────────────
# CONCEPT: HTTPException — controlled error responses
# ─────────────────────────────────────────────
# Raise HTTPException to return a specific HTTP status code with an error message.
# This is how you communicate failures to callers in a structured way.
@app.post("/agent/task", response_model=TaskResponse)
def submit_task(payload: TaskRequest) -> TaskResponse:
    """
    Simulates receiving an agent task.
    Returns 400 if the task contains a blocked keyword (safety filter demo).
    """
    blocked_keywords = ["delete all", "drop table", "rm -rf"]
    for blocked in blocked_keywords:
        if blocked in payload.task.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Task rejected: contains blocked content '{blocked}'",
            )

    task_id = f"task-{abs(hash(payload.task)) % 10000:04d}"
    _submitted_task_ids.append(task_id)
    return TaskResponse(
        task_id=task_id,
        status="queued",
        priority=payload.priority,
        message=f"Task '{payload.task[:40]}' accepted and queued.",
    )


# ─────────────────────────────────────────────
# SESSION 3 ASSIGNMENT: GET /agent/status
# ─────────────────────────────────────────────
# Returns the list of task IDs submitted since the server started.
# Demonstrates: GET endpoint, query param filtering, in-memory state.
class StatusResponse(BaseModel):
    total: int
    task_ids: list[str]


@app.get("/agent/status", response_model=StatusResponse)
def agent_status(limit: int = 20) -> StatusResponse:
    """
    Returns recent task IDs accepted by /agent/task.
    - `limit` (query param): max number of IDs to return. Default 20.

    Example:
        GET /agent/status?limit=5
    """
    recent = _submitted_task_ids[-limit:]
    return StatusResponse(total=len(_submitted_task_ids), task_ids=recent)
