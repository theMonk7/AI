# Week 16: Build a Custom Agent From Scratch + LangGraph Agents

## Phase
Phase 5 — Agents & Agentic AI

## Where this fits
- **Prerequisites:** Week 15 (agent loop, ReAct).
- **Next:** Week 17 (multi-agent systems).

## Why this week matters
Frameworks hide the agent loop; senior engineers can build it themselves. This week you implement a working agent **from scratch** (no framework) — LLM call, tool registry, parsing tool calls, executing, feeding results back, stopping — then rebuild it in LangGraph. Building it by hand demystifies every agent framework you'll ever touch.

## Learning objectives
1. Implement a complete agent loop in plain Python (no agent framework).
2. Design a tool registry with validated arguments and safe execution.
3. Rebuild the same agent in LangGraph and compare.

## Topics to master (in detail)
### A. Agent from scratch
- The loop: prompt → LLM → parse tool call → validate → execute → append result → repeat
- Tool registry: name → schema → function
- Argument validation with Pydantic before execution
- Stopping conditions, max steps, and error recovery
- Building the running "scratchpad" / message history

### B. Robustness
- Handling invalid tool calls / hallucinated tools
- Timeouts and retries per tool (reuse Phase 1 skills)
- Structured final-answer detection

### C. LangGraph version
- Same agent as a graph (LLM node, ToolNode, conditional loop)
- Trade-offs: control vs convenience
- Adding persistence/HITL from Week 14

## Tools for this week
- Python + an LLM SDK (scratch build), Pydantic, then langgraph

## Guided coding labs
1. Implement the from-scratch agent loop with 2–3 tools and a step guard.
2. Add argument validation + graceful handling of bad tool calls.
3. Reimplement in LangGraph; verify identical behavior.

## Mini project
**Custom coding/utility agent** — a from-scratch agent (with a LangGraph twin) that uses tools (e.g., file read, calculator, search stub) to complete multi-step tasks reliably. (Brief + skeleton + rubric.)

## Deliverables / evidence
- From-scratch agent module + LangGraph twin
- Trace showing tool validation catching a bad call
- Notes: what the framework does for you that you built by hand

## Checkpoints before moving on
- You can build an agent loop without a framework.
- Tool arguments are validated before execution.
- You can map every framework concept to your hand-built version.

## Suggested study split (8–10 hours)
1. Concept learning: 2h
2. Scratch build: 4h
3. LangGraph twin: 2h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
