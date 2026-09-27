# Week 15: Agent Fundamentals — ReAct, the Tool-Calling Loop, Chains vs Agents

## Phase
Phase 5 — Agents & Agentic AI

## Where this fits
- **Prerequisites:** Phase 4 (LangChain/LangGraph, tools, state).
- **Next:** Week 16 (build a custom agent from scratch + LangGraph agents).

## Why this week matters
This is the heart of "agentic AI." An agent is an LLM that **reasons, chooses actions (tools), observes results, and repeats until done** — instead of answering in one shot. Understanding the agent loop conceptually (before any framework magic) is what separates people who *use* agents from people who can *design and debug* them.

## Learning objectives
1. Explain what an agent is and how the ReAct loop works.
2. Decide correctly between a chain (fixed steps) and an agent (dynamic steps).
3. Trace a full reason → act → observe → repeat cycle.

## Topics to master (in detail)
### A. What an agent is
- Agent = LLM + tools + a loop + a stopping condition
- Autonomy spectrum: fixed chain → router → full agent
- The cost of autonomy (latency, tokens, unpredictability)

### B. Agent reasoning patterns
- **ReAct** (Reason + Act): interleave thoughts and tool actions
- Plan-and-execute (plan first, then act)
- Reflection / self-critique loops
- Scratchpad / intermediate steps

### C. Chains vs agents (senior judgment)
- When fixed control flow (chain/graph) is better and cheaper
- When dynamic tool selection (agent) is worth it
- Guardrails: max steps, timeouts, tool allow-lists

## Tools for this week
- LangGraph prebuilt agent (`create_react_agent`), an LLM, your tools from Week 12–13

## Guided coding labs
1. Run a prebuilt ReAct agent and print every thought/action/observation.
2. Force a failure (bad tool) and watch how the loop recovers or stalls.
3. Convert a task from an agent to a fixed chain; compare cost/reliability.

## Mini project
**Instrumented ReAct agent** — a tool-using agent that logs each reasoning step, enforces a max-step guard, and answers multi-step questions. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Agent run traces (thought/action/observation)
- Chain-vs-agent comparison notes
- Notes: when you'd choose each

## Checkpoints before moving on
- You can explain the ReAct loop from memory.
- You can justify agent vs chain for a given task.
- Your agent has step/time guardrails.

## Suggested study split (8–10 hours)
1. Concept learning: 3h
2. Guided implementation: 3.5h
3. Experiments: 1.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
