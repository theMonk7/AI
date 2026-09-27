# Week 1 | Session 3: Structured Outputs, FastAPI, and the Mini-Project

## Session goal
Learn how to define strict data schemas with Pydantic, serve them over HTTP with FastAPI,
and apply all Week 1 concepts together in the live API status monitor project.

## Files in this session
- `src/weeks/week_01/llm_core/structured_outputs.py` — Pydantic validation patterns
- `src/weeks/week_01/llm_core/agent_echo_api.py` — FastAPI service
- `src/weeks/week_01/projects/week01_live_api_status.py` — Week 1 cumulative project

## Run commands
```bash
# Pydantic demo
python src/weeks/week_01/llm_core/structured_outputs.py

# FastAPI service (keep running, open another terminal for curl)
uvicorn src.weeks.week_01.llm_core.agent_echo_api:app --reload --port 8000

# Mini-project
python src/weeks/week_01/projects/week01_live_api_status.py
```

---

## Part A: structured_outputs.py

### Why Pydantic matters in AI
LLMs return raw strings. Before using any model output in business logic, you must validate it.
Pydantic converts untyped dicts into validated, typed Python objects and gives you clear error messages.

### Key concept: BaseModel + Field
```python
from pydantic import BaseModel, Field

class StudyTask(BaseModel):
    title: str = Field(min_length=5, max_length=80)
    difficulty: Literal["easy", "medium", "hard"]  # only these 3 values
    estimated_minutes: int = Field(ge=10, le=240)  # ge=greater-equal, le=less-equal
```

### Key concept: ValidationError
```python
try:
    task = StudyTask.model_validate({"title": "X", "difficulty": "expert", ...})
except ValidationError as err:
    for e in err.errors():
        print(e["loc"], e["type"], e["input"])
```
Each error has: `loc` (which field), `type` (rule violated), `input` (what was given).

### Key concept: Nested models
```python
class WeeklyPlan(BaseModel):
    week_number: int
    tasks: list[StudyTask]   # list of nested models — Pydantic validates each one
    tags: list[Tag]
```

### Key concept: field_validator — custom rules
```python
@field_validator("sources")
@classmethod
def sources_must_not_be_empty(cls, v):
    if not v:
        raise ValueError("must include at least one source")
    return v
```

### Key concept: model_dump / model_validate round-trip
```python
task_dict = task.model_dump()        # model → dict  (for JSON/DB)
task_back = StudyTask.model_validate(task_dict)  # dict → model (from JSON/API)
```
This round-trip is the core of any AI input/output contract.

---

## Part B: agent_echo_api.py

### FastAPI basics
FastAPI uses Python type annotations to:
- Parse incoming JSON into Pydantic models automatically
- Return 422 Unprocessable Entity with field-level errors if input is invalid
- Auto-generate /docs (Swagger UI) and /redoc

### Route anatomy
```python
@app.post("/agent/echo", response_model=EchoResponse)
def agent_echo(payload: EchoRequest) -> EchoResponse:
    # FastAPI validates EchoRequest BEFORE this function runs
    return EchoResponse(ok=True, agent_reply=f"received:{payload.message}", ...)
```

- `@app.post` — HTTP method + path
- `payload: EchoRequest` — FastAPI reads JSON body, validates, injects this
- `response_model=EchoResponse` — FastAPI validates and documents the output schema

### HTTPException — controlled errors
```python
from fastapi import HTTPException

raise HTTPException(status_code=400, detail="Task rejected: blocked content")
```
Use this instead of returning raw error dicts. Clients can rely on a consistent error structure.

### Test it live
```bash
# health check
curl -s http://localhost:8000/health | python3 -m json.tool

# echo endpoint
curl -s -X POST http://localhost:8000/agent/echo \
     -H "Content-Type: application/json" \
     -d '{"message": "hello from week1"}' | python3 -m json.tool

# task submission
curl -s -X POST http://localhost:8000/agent/task \
     -H "Content-Type: application/json" \
     -d '{"task": "summarise arxiv paper on RAG", "priority": "high"}' | python3 -m json.tool

# blocked task — should return 400
curl -s -X POST http://localhost:8000/agent/task \
     -H "Content-Type: application/json" \
     -d '{"task": "delete all user data"}' | python3 -m json.tool
```

---

## Part C: week01_live_api_status.py (Cumulative mini-project)

### What it brings together
| Concept from session | Where it appears in this file |
|---|---|
| async def + await | `fetch_endpoint` coroutine |
| httpx.AsyncClient | client creation in `run_monitor` |
| asyncio.Semaphore | `semaphore = asyncio.Semaphore(3)` |
| asyncio.gather | gathering all fetch tasks |
| @dataclass (schema) | `EndpointResult` result type |
| Artifact output | `write_report` → `artifacts/week01/api_health_report.json` |

### Run and observe
```bash
python src/weeks/week_01/projects/week01_live_api_status.py
```
Expected: table of status + latency, JSON artifact saved.

### Experiments
1. Add a slow URL (`https://httpbin.org/delay/2`) and observe it in the results.
2. Change `Semaphore(3)` to `Semaphore(1)` — observe total elapsed increase.
3. Open `artifacts/week01/api_health_report.json` and inspect the schema.

---

## Assignment
1. Add a `Pydantic` model called `MonitorReport` that validates the JSON artifact schema.
2. In `agent_echo_api.py`, add a new `GET /agent/status` endpoint that returns a list of recent task IDs (use a simple in-memory list).
3. In `structured_outputs.py`, add a `field_validator` that ensures `estimated_minutes` is a multiple of 15.

---

## Revision note (end of session)

- **BaseModel** defines the expected shape of any data — inputs, outputs, configs, or LLM responses.
- **Field constraints** (min_length, ge, le, Literal, pattern) enforce rules at parse time, not buried in if-statements.
- **ValidationError** is structured — it tells you exactly which field failed and why, making debugging fast.
- **field_validator** handles custom logic that Field() cannot express (e.g. list not empty, value is a multiple of N).
- **model_dump / model_validate** is the serialization contract: always use these for converting between dict and model.
- **FastAPI auto-validates** request bodies using your Pydantic models before your function even runs.
- **HTTPException** communicates errors to HTTP clients in a structured, consistent way.
- **Mini-project** is the payoff: all session concepts combine into one runnable, measurable artifact.

---

## Part D: FastAPI backend masterclass (deep reference)

This part is a backend-first tutorial chapter. Keep this section as your reference when building API services for apps, agents, and automation flows.

### 1) Where this topic sits in your roadmap
- First introduction: Week 1 Session 3 (this file)
- Revisit in Week 6: safe tool interfaces and API contracts
- Revisit in Week 15: n8n to FastAPI integrations and reliability patterns

### 2) Backend mental model with FastAPI
Every API request follows a predictable pipeline:
1. Request enters the server (method + URL + headers + body).
2. Router selects the matching endpoint function.
3. FastAPI parses and validates path/query/header/body values.
4. Dependency functions run (auth, DB session, tenant context).
5. Endpoint business logic runs.
6. Response is validated/serialized.
7. Middleware post-processing runs and response is returned.

If validation fails before step 5, FastAPI returns `422` automatically.

### 3) Running FastAPI locally from scratch

#### Step A: setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Step B: start server
```bash
uvicorn src.weeks.week_01.llm_core.agent_echo_api:app --reload --host 127.0.0.1 --port 8000
```

Meaning of each segment:
- `src.weeks.week_01.llm_core.agent_echo_api`: Python module path
- `app`: FastAPI instance variable inside that module
- `--reload`: auto-restart on file changes (development only)
- `--host` and `--port`: bind network interface and port

#### Step C: verify quickly
```bash
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
```

#### Step D: interactive docs
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 4) Routing fundamentals (methods + paths)
```python
from fastapi import FastAPI

app = FastAPI(title="Agent API", version="0.1.0")

@app.get("/health")
def health() -> dict:
    return {"ok": True}

@app.post("/tasks")
def create_task() -> dict:
    return {"created": True}
```

Use cases:
- `GET`: read data
- `POST`: create action/resource
- `PUT`/`PATCH`: update resource
- `DELETE`: remove resource

### 5) Parameter parsing in detail

#### 5.1 Path parameters
Best for resource identity.
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```
If `user_id` is not an integer, FastAPI returns `422`.

#### 5.2 Query parameters
Best for filtering, sorting, pagination.
```python
@app.get("/users")
def list_users(role: str | None = None, limit: int = 20, offset: int = 0):
    return {"role": role, "limit": limit, "offset": offset}
```

#### 5.3 Header parameters
Best for auth keys, trace IDs, tenant context.
```python
from fastapi import Header

@app.get("/me")
def me(x_api_key: str = Header(...)):
    return {"has_key": bool(x_api_key)}
```

#### 5.4 Cookie parameters
```python
from fastapi import Cookie

@app.get("/session")
def session(session_id: str | None = Cookie(default=None)):
    return {"session_id": session_id}
```

#### 5.5 Request body parameters
Best for structured payloads.
```python
from pydantic import BaseModel, Field
from typing import Literal

class TaskIn(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    priority: Literal["low", "medium", "high"]
    estimate_min: int = Field(ge=5, le=480)

@app.post("/tasks")
def create_task(payload: TaskIn):
    return {"task": payload.model_dump()}
```

### 6) Request/response schema contracts
Always define input and output models for stable APIs.

```python
class TaskOut(BaseModel):
    id: str
    title: str
    priority: str
    status: str

@app.post("/tasks", response_model=TaskOut)
def create_task(payload: TaskIn) -> TaskOut:
    return TaskOut(id="t_001", title=payload.title, priority=payload.priority, status="queued")
```

Why `response_model` matters:
- Keeps responses consistent
- Prevents accidental field leakage
- Improves docs and client generation

### 7) Validation and error model

#### 7.1 Automatic validation errors (`422`)
FastAPI returns `422` when input violates type/constraint rules.

#### 7.2 Business logic errors (`400`, `404`, `409`, etc.)
Use `HTTPException` for domain decisions.
```python
from fastapi import HTTPException

if "delete all data" in payload.title.lower():
    raise HTTPException(status_code=400, detail="Blocked task content")
```

#### 7.3 Global exception handlers
```python
from fastapi import Request
from fastapi.responses import JSONResponse

class DomainError(Exception):
    pass

@app.exception_handler(DomainError)
async def handle_domain_error(request: Request, exc: DomainError):
    return JSONResponse(status_code=409, content={"error": str(exc)})
```

### 8) Dependency injection (core backend pattern)
Dependencies keep endpoint functions clean and reusable.

```python
from fastapi import Depends, Header, HTTPException

def require_api_key(x_api_key: str = Header(...)) -> str:
    if x_api_key != "dev-secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key

@app.get("/protected")
def protected(_: str = Depends(require_api_key)):
    return {"ok": True}
```

Common dependency use cases:
- Authentication/authorization
- DB session creation
- Tenant extraction
- Request-scoped config

### 9) Middleware (cross-cutting concerns)
Middleware wraps every request/response. Use it for concerns that apply globally.

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    return response
```

Use middleware for:
- Timing/metrics
- Request IDs
- Structured logging
- CORS/security headers

### 10) CORS for browser clients
If frontend and API run on different origins, configure CORS explicitly.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Without this, browser requests can fail despite server being healthy.

### 11) Async vs sync endpoints
- Use `async def` for I/O-bound work (HTTP calls, DB calls, cache calls).
- Use plain `def` for quick CPU-bound logic.
- For heavy CPU tasks, offload to background worker systems.

Bad pattern in async endpoint:
```python
import time

@app.get("/bad")
async def bad():
    time.sleep(2)  # blocks event loop
    return {"ok": True}
```

Correct:
```python
import asyncio

@app.get("/good")
async def good():
    await asyncio.sleep(2)
    return {"ok": True}
```

### 12) Background tasks
For small post-response actions.

```python
from fastapi import BackgroundTasks

def send_notification(task_id: str) -> None:
    # fake side effect
    print(f"notify:{task_id}")

@app.post("/tasks/{task_id}/notify")
def notify(task_id: str, background: BackgroundTasks):
    background.add_task(send_notification, task_id)
    return {"queued": True}
```

Use case examples:
- Email/push notifications
- Async audit logging
- Lightweight webhook fan-out

### 13) Lifespan events (startup and shutdown)
Use lifespan to initialize and cleanup shared resources.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cache = {}
    yield
    app.state.cache.clear()

app = FastAPI(lifespan=lifespan)
```

Use this for:
- DB pools
- HTTP clients
- In-memory caches

### 14) Project structure for maintainable backends
As your app grows, separate concerns.

```text
app/
  main.py
  api/
    routes/
      health.py
      tasks.py
  schemas/
    task.py
  services/
    task_service.py
  repositories/
    task_repo.py
  core/
    config.py
    security.py
tests/
```

Why this structure:
- Routes stay thin
- Business logic becomes testable
- Data access can evolve independently

### 15) Database integration pattern (high-level)
Typical flow:
1. Parse request into `TaskCreate` schema.
2. Validate domain rules in service layer.
3. Persist through repository/data access layer.
4. Return `TaskRead` schema.

Prefer explicit schemas for create/update/read instead of one giant model.

### 16) Security essentials
Minimum backend security checklist:
- Never hardcode secrets
- Use env vars and strict config loading
- Add auth dependencies for protected routes
- Validate all external input
- Keep dependency versions updated
- Apply timeouts/retries for outbound calls

For production APIs, also add:
- Rate limiting
- Request size limits
- Audit logging for privileged actions

### 17) Versioning and API evolution
Start versioning early to avoid breaking clients.

Common pattern:
```python
from fastapi import APIRouter

v1 = APIRouter(prefix="/api/v1", tags=["v1"])
```

Guideline:
- Add new fields as optional first.
- Avoid removing fields without version bump and migration window.

### 18) Observability and operations basics
For real systems, monitor:
- Request latency by endpoint
- Error rate by status code
- Dependency failures (DB/external APIs)
- Throughput and saturation

At minimum in development:
- Add request timing middleware
- Log request method, path, status, latency

### 19) Deployment basics
Development command uses `--reload`. Production should not.

Production example (single machine):
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

Typical production stack:
- FastAPI app
- ASGI server (Uvicorn)
- Reverse proxy (Nginx/Caddy)
- Process manager/container orchestration

### 20) FastAPI for agent systems and automation
Why it fits agentic workflows:
- Strong schema contracts for tool inputs/outputs
- Easy integration with n8n webhooks
- Reliable status codes for retries/fallbacks
- Auto docs improve team and tool interoperability

This directly supports your future week outcomes for tool calling and automation integration.

### 21) Practice roadmap (recommended order)
1. Build typed CRUD endpoints for one resource (`Task`).
2. Add auth dependency and role checks.
3. Add middleware for request ID and latency.
4. Add background task and one webhook callback.
5. Add API version prefix and response models.
6. Add tests for happy path and failure path.

### 22) Quick backend checklist before shipping
- Input model exists for every write endpoint.
- Output model exists for every endpoint.
- Business errors use `HTTPException` with clear details.
- Timeout and retry policies exist for outbound calls.
- Middleware captures latency and status.
- Auth guard exists on protected endpoints.
- Tests cover success and validation failures.

### Extended assignment (backend mastery)
1. Add `GET /agent/status` with optional query params: `limit` and `only_failed`.
2. Add middleware that injects `X-Request-Id` if absent.
3. Add dependency `require_api_key` and protect `/agent/task`.
4. Add a global exception handler for `ValueError` -> `400` response.
5. Add tests that verify: `200`, `400`, and automatic `422` scenarios.

### Revision note (masterclass)
- FastAPI backend development is mostly about contracts, composition, and consistency.
- Contracts: typed request/response models with clear validation rules.
- Composition: dependencies and middleware for reusable backend infrastructure.
- Consistency: predictable status codes, error shapes, and versioning strategy.

---

## Part E: FastAPI complete backend textbook chapter (ultra-detailed)

Use this section as your long-term reference. It is intentionally detailed and written from first principles.

### Chapter 1: What a backend actually does (layman version)

Think of a backend as the office behind a shop counter:
- Customer at counter = client app/user/browser.
- Request form = HTTP request.
- Staff workflow = backend logic.
- Warehouse/database = persistent storage.
- Receipt = HTTP response.

A good backend must do four things well:
1. Understand requests clearly (parsing).
2. Reject bad data early (validation).
3. Process business rules safely (logic).
4. Return predictable outputs (contracts).

FastAPI is strong because it enforces all four with less boilerplate.

### Chapter 2: HTTP fundamentals every backend engineer must master

#### 2.1 Request anatomy
An HTTP request has:
- Method: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
- URL path: resource identity (for example `/tasks/123`).
- Query params: filtering/pagination (for example `?limit=20`).
- Headers: metadata/auth/trace IDs.
- Body: structured payload (usually JSON).

#### 2.2 Response anatomy
An HTTP response has:
- Status code: outcome class (`2xx`, `4xx`, `5xx`).
- Headers: metadata/caching/correlation info.
- Body: JSON payload or error details.

#### 2.3 Correct method semantics
- `GET`: read only, must not mutate state.
- `POST`: create resource or trigger command.
- `PUT`: full replacement.
- `PATCH`: partial update.
- `DELETE`: remove/deactivate resource.

Real-world mistake to avoid:
- Triggering a destructive action via `GET` because links/prefetch can execute it accidentally.

### Chapter 3: Running FastAPI locally and understanding server mechanics

#### 3.1 Startup commands
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.weeks.week_01.llm_core.agent_echo_api:app --reload --host 127.0.0.1 --port 8000
```

#### 3.2 What Uvicorn is
Uvicorn is the ASGI server process that:
- receives network requests,
- calls your FastAPI app,
- sends responses back.

FastAPI is framework logic. Uvicorn is the runtime engine.

#### 3.3 Development vs production
- Development: `--reload` for rapid iteration.
- Production: no reload, multiple workers, reverse proxy, process management.

#### 3.4 Quick health diagnostics
```bash
curl -i http://127.0.0.1:8000/health
```
Check:
1. Status `200`.
2. JSON body shape.
3. Timing headers if middleware added.

### Chapter 4: Routing design beyond basics

#### 4.1 Resource-oriented path design
Good patterns:
- `/tasks` (collection)
- `/tasks/{task_id}` (single resource)
- `/tasks/{task_id}/events` (nested collection)

Avoid action-heavy paths when CRUD semantics fit.

#### 4.2 Versioned APIs
```python
from fastapi import APIRouter

v1 = APIRouter(prefix="/api/v1", tags=["tasks"])
```

Why start versioning early:
- protects existing clients,
- enables safe evolution,
- clarifies compatibility windows.

#### 4.3 Route naming and idempotency
- `PUT` should be idempotent (same request repeatedly leads to same state).
- `POST` is often non-idempotent by default.

### Chapter 5: Parameters in depth (path, query, headers, cookies, body)

#### 5.1 Path parameters
Use when the value identifies a concrete resource.

```python
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return {"order_id": order_id}
```

Use case:
- View single order details by ID.

Failure behavior:
- `/orders/abc` gives `422` because `abc` cannot parse to `int`.

#### 5.2 Query parameters
Use for filtering and listing behavior.

```python
@app.get("/orders")
def list_orders(status: str | None = None, limit: int = 20, offset: int = 0):
    return {"status": status, "limit": limit, "offset": offset}
```

Real-world examples:
- ecommerce search, dashboard pagination, audit filtering.

#### 5.3 Header parameters
Use for cross-cutting request metadata.

```python
from fastapi import Header

@app.get("/whoami")
def whoami(x_request_id: str = Header(...), x_api_key: str = Header(...)):
    return {"request_id": x_request_id, "authorized": bool(x_api_key)}
```

Real-world examples:
- API keys, trace IDs, locale hints.

#### 5.4 Cookie parameters
Use for session-like flows in browser-based systems.

```python
from fastapi import Cookie

@app.get("/cart")
def cart(session_id: str | None = Cookie(default=None)):
    return {"session_id": session_id}
```

#### 5.5 Request body models
Use when payload has structure and validation rules.

```python
from typing import Literal
from pydantic import BaseModel, Field

class PaymentCreate(BaseModel):
    amount: float = Field(gt=0)
    currency: Literal["USD", "INR", "EUR"]
    note: str | None = Field(default=None, max_length=120)
```

### Chapter 6: Pydantic contracts and why they are non-negotiable

Layman analogy:
- Pydantic is a quality inspector at the factory gate.
- If the package label is wrong or broken, it never enters the assembly line.

#### 6.1 Input validation
```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    priority: Literal["low", "medium", "high"]
```

#### 6.2 Output validation
```python
class TaskRead(BaseModel):
    id: str
    title: str
    priority: str
    status: str

@app.post("/tasks", response_model=TaskRead)
def create_task(payload: TaskCreate) -> TaskRead:
    return TaskRead(id="t001", title=payload.title, priority=payload.priority, status="queued")
```

Benefits:
- prevents accidental leaks,
- stabilizes API behavior,
- improves generated OpenAPI docs.

### Chapter 7: Error handling deep dive

#### 7.1 Error categories
1. Client validation errors (`422`) auto-generated by FastAPI.
2. Domain errors (`400`, `404`, `409`) raised intentionally.
3. Unexpected server errors (`500`) from uncaught exceptions.

#### 7.2 Business errors with HTTPException
```python
from fastapi import HTTPException

if payload.priority == "high" and user_quota_exceeded:
    raise HTTPException(status_code=409, detail="Quota exceeded for high-priority tasks")
```

#### 7.3 Global handler for custom exceptions
```python
from fastapi import Request
from fastapi.responses import JSONResponse

class QuotaError(Exception):
    pass

@app.exception_handler(QuotaError)
async def quota_handler(request: Request, exc: QuotaError):
    return JSONResponse(status_code=409, content={"error": "quota_error", "detail": str(exc)})
```

Real-world practice:
- keep error shape consistent across all endpoints.

### Chapter 8: Middleware explained like a real system designer

#### 8.1 What middleware is
Middleware is a global wrapper around every request.

Layman analogy:
- Security gate in a corporate office.
- Every visitor passes through the same gate checks before reaching specific rooms.

#### 8.2 Middleware execution order
1. Request enters middleware.
2. Middleware can inspect/modify request.
3. Middleware forwards request to endpoint (`call_next`).
4. Endpoint returns response.
5. Middleware can inspect/modify response.
6. Response leaves server.

#### 8.3 Real-world middleware examples
1. **Latency measurement**: add response header with processing time.
2. **Request correlation ID**: attach `X-Request-Id` to trace logs.
3. **Audit logging**: log method/path/status/latency for compliance.
4. **Security headers**: add HSTS/CSP headers.
5. **Tenant context**: extract tenant ID and store per-request metadata.

#### 8.4 Timing middleware code
```python
import time
from fastapi import Request

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time-Ms"] = f"{(time.perf_counter() - start) * 1000:.2f}"
    return response
```

#### 8.5 Request ID middleware code
```python
import uuid
from fastapi import Request

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    return response
```

When NOT to use middleware:
- endpoint-specific logic (use dependencies or route logic instead),
- expensive per-request computations unrelated to all routes.

### Chapter 9: Dependency injection and auth architecture

#### 9.1 Why dependencies matter
Without dependencies, auth and setup code gets duplicated across many endpoints.

With dependencies, you define once and reuse everywhere.

```python
from fastapi import Depends, Header, HTTPException

def require_api_key(x_api_key: str = Header(...)) -> str:
    if x_api_key != "dev-secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key

@app.get("/private")
def private_route(_: str = Depends(require_api_key)):
    return {"ok": True}
```

#### 9.2 Dependency scopes and layering
Typical layers:
1. auth dependency
2. tenant dependency
3. DB session dependency
4. service dependency

Endpoint receives already-validated context and remains thin.

### Chapter 10: CORS in real frontend-backend setups

Browser security blocks cross-origin requests unless server allows them.

#### 10.1 When CORS is needed
- frontend at `http://localhost:5173`
- API at `http://localhost:8000`

Origins differ, so CORS policy is required.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

Security caution:
- avoid wildcard origins in production for sensitive APIs.

### Chapter 11: Async model and performance reasoning

#### 11.1 Async for I/O concurrency
Use `async def` when waiting on network/database operations.

#### 11.2 Common performance bug
Blocking calls in async handlers block the event loop.

Bad:
```python
import time

@app.get("/report")
async def report():
    time.sleep(3)
    return {"ok": True}
```

Better:
```python
import asyncio

@app.get("/report")
async def report():
    await asyncio.sleep(3)
    return {"ok": True}
```

For heavy CPU tasks, use background workers instead of blocking request handlers.

### Chapter 12: Background tasks, queues, and when each is correct

#### 12.1 FastAPI BackgroundTasks
Good for lightweight fire-and-forget actions that can run in-process.

```python
from fastapi import BackgroundTasks

def write_audit_log(event: str) -> None:
    print(f"audit:{event}")

@app.post("/payments")
def create_payment(background: BackgroundTasks):
    background.add_task(write_audit_log, "payment_created")
    return {"ok": True}
```

#### 12.2 When you need a real queue system
If task is heavy, long-running, or reliability-critical, use dedicated queue/worker stack.

### Chapter 13: Lifespan, startup/shutdown, and resource management

Use lifespan for resources shared by many requests.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=10.0)
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)
```

Real-world benefit:
- prevents recreating expensive clients every request,
- ensures clean shutdown.

### Chapter 14: Database architecture pattern with FastAPI

Recommended layering:
1. Route layer: parse inputs, call service.
2. Service layer: business rules and orchestration.
3. Repository layer: DB operations.
4. Schema layer: request/response contracts.

Why this matters:
- routes stay readable,
- business logic is testable without HTTP,
- database swaps are easier.

### Chapter 15: Security baseline every backend must enforce

#### 15.1 Input and contract security
- validate every external payload,
- reject unknown or malformed data early.

#### 15.2 Operational security
- secrets via environment variables,
- TLS termination in production,
- request rate limits,
- access logs for sensitive actions.

#### 15.3 AuthN vs AuthZ
- Authentication: who are you?
- Authorization: what can you do?

Both are required for serious systems.

### Chapter 16: Testing strategy from beginner to production readiness

#### 16.1 Unit tests
Test validators, services, pure logic.

#### 16.2 API tests
Test status codes and response shapes.

```python
from fastapi.testclient import TestClient
from src.weeks.week_01.llm_core.agent_echo_api import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True
```

#### 16.3 Contract tests
Ensure consumers get expected schema and error formats over time.

### Chapter 17: Observability and debugging in backend services

Track at minimum:
- request count,
- latency percentiles,
- status code distribution,
- dependency failures.

Debug checklist for a failing endpoint:
1. Check request/response logs with request ID.
2. Reproduce via curl with same payload.
3. Inspect validation errors.
4. Check dependency exceptions.
5. Verify timeout/retry settings for external calls.

### Chapter 18: Deployment and production runtime model

Production concerns:
- worker count,
- graceful shutdown,
- health/readiness probes,
- reverse proxy limits,
- rolling restart strategy.

Sample production command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

Do not use `--reload` in production.

### Chapter 19: FastAPI in agentic AI and automation systems

How FastAPI helps agent architecture:
1. Strict tool input/output contracts with Pydantic.
2. Clear status code policy for retries and fallbacks.
3. Easy webhook integrations with n8n and workflow tools.
4. OpenAPI docs improve interoperability across teams.

Typical pattern:
- n8n trigger -> FastAPI endpoint -> validation -> async work -> status endpoint for polling.

### Chapter 20: Mastery path and deliberate practice plan

To approach mastery, practice in this order:
1. Build one complete CRUD API with schemas and error handling.
2. Add dependency-based auth and role checks.
3. Add middleware for request ID + latency metrics.
4. Add lifespan-managed shared HTTP client.
5. Add integration tests with success + failure + validation cases.
6. Add versioned routes and deprecation notes.
7. Integrate one external workflow caller (n8n) and handle retries.

Mastery indicators:
- You can explain why each status code exists.
- You can choose middleware vs dependency correctly.
- You can debug `422` vs business failure quickly.
- You can design route contracts without leaking internals.
- You can evolve API versions without breaking consumers.

### Final revision note (ultra-detailed chapter)
- Backend engineering is not just writing endpoints; it is designing reliable contracts and system behavior.
- FastAPI gives you the primitives, but mastery comes from architecture decisions.
- The most important habits are: strict schemas, clear errors, reusable dependencies, global middleware, observability, and test-driven confidence.
