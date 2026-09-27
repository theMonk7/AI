# Week 05: Structured Outputs, Tool/Function Calling & Guardrails

## Phase
Phase 2 — LLM Application Fundamentals

## Where this fits
- **Prerequisites:** Week 4 (calling LLMs, prompting).
- **Next:** Week 6 (embeddings & semantic search) — the last primitive before full RAG.

## Why this week matters
Free-text LLM output is useless to a program until it's structured and validated. Reliable structured outputs and tool calling are the backbone of every agent: an agent is essentially an LLM that emits *structured tool calls* in a loop. Getting this right (with validation and guardrails) is what makes agents dependable instead of flaky.

## Learning objectives
1. Force LLMs to return schema-valid JSON and parse it into Pydantic models.
2. Implement function/tool calling: define tools, let the model choose, execute, return results.
3. Add guardrails: validation, retries on invalid output, safe fallbacks.

## Topics to master (in detail)
### A. Structured outputs
- JSON mode / structured output APIs
- Defining output schemas with Pydantic; `instructor` / Pydantic-AI
- Re-asking on validation failure (self-correction loop)
- Handling partial/streaming structured output

### B. Function / tool calling (the agent primitive)
- Describing tools as JSON schemas (name, description, parameters)
- Model selects a tool + arguments → you validate → you execute → return result
- Multiple tools, tool choice, and parallel tool calls
- Mapping tool schemas from Pydantic models automatically

### C. Guardrails & safety
- Validating arguments before executing anything (never trust raw args)
- Safe defaults, allow-lists, and refusing unknown actions
- Output guardrails (Guardrails-AI / NeMo Guardrails overview)
- Idempotency and side-effect safety for tools

## Tools for this week
- OpenAI tool calling, Pydantic v2, instructor / Pydantic-AI, Guardrails-AI (overview)

## Guided coding labs
1. Extract structured data (e.g. a `Contact` model) from messy text, with re-ask on failure.
2. Define two tools (e.g. `get_weather`, `calculator`), let the model choose, execute, return.
3. Add argument validation that rejects unsafe/invalid tool calls.

## Mini project
**Tool-calling extractor service** — a FastAPI endpoint that takes text, calls an LLM with tools, validates the tool arguments, executes, and returns a structured, schema-valid result. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Structured-output extractor with validation retry
- Working tool-calling loop (choose → validate → execute → return)
- Notes: what happened when the model returned invalid output

## Checkpoints before moving on
- LLM outputs are always parsed into validated models (never raw strings).
- Tool arguments are validated before execution.
- You can explain how tool calling underpins agents.

## Suggested study split (8–10 hours)
1. Concept learning: 2.5h
2. Guided implementation: 4h
3. Testing edge cases: 1.5h
4. Reflection and notes: 1–2h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
