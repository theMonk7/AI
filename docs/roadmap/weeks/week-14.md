# Week 14: LangGraph Advanced — Persistence, HITL, Streaming, Subgraphs

## Phase
Phase 4 — LangChain & LangGraph

## Where this fits
- **Prerequisites:** Week 13 (LangGraph fundamentals).
- **Next:** Phase 5 (Agents) uses these features to build reliable, resumable agents.

## Why this week matters
Real agents must remember across sessions, pause for human approval, stream progress to users, and be composed from reusable parts. LangGraph's advanced features — checkpointing (persistence), human-in-the-loop, streaming, and subgraphs — are what turn a toy graph into a dependable production agent. This is the Phase 4 capstone.

## Learning objectives
1. Persist graph state with checkpointers (resume/replay conversations).
2. Add human-in-the-loop interrupts for approval/editing.
3. Stream intermediate steps and compose subgraphs.

## Topics to master (in detail)
### A. Persistence & memory
- Checkpointers (in-memory, SQLite, Postgres) and `thread_id`
- Resuming a run; time-travel/replay of state
- Long-term memory vs per-thread short-term memory

### B. Human-in-the-loop (HITL)
- `interrupt` and approval gates before risky actions
- Editing state mid-run; resuming with human input

### C. Streaming & composition
- Streaming nodes, tokens, and state updates to a UI
- Subgraphs: encapsulate and reuse graph components
- Error handling and retries within graphs

## Tools for this week
- langgraph (checkpointers), SQLite/Postgres, an LLM

## Guided coding labs
1. Add a SQLite checkpointer; stop and resume a conversation by `thread_id`.
2. Insert a human approval interrupt before a tool that has side effects.
3. Stream state updates and refactor part of the graph into a subgraph.

## Mini project (Phase 4 capstone)
**Resumable, approval-gated assistant** — a LangGraph app with persistence (resume across runs), a HITL approval step, streaming output, and a subgraph. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Persisted graph that resumes by thread
- HITL approval gate demo
- Notes: what state you persisted and why

## Checkpoints before moving on
- Conversations survive restarts via checkpointing.
- A human can approve/deny before side effects.
- You can stream progress and reuse subgraphs.

## Suggested study split (8–10 hours)
1. Concept learning: 2h
2. Guided implementation: 4.5h
3. Experiments: 1.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
