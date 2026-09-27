# Week 13: LangGraph Fundamentals — State, Nodes, Edges, Cycles

## Phase
Phase 4 — LangChain & LangGraph

## Where this fits
- **Prerequisites:** Weeks 11–12 (LangChain chains, tools, memory).
- **Next:** Week 14 (advanced LangGraph: persistence, human-in-the-loop, streaming).

## Why this week matters
Linear chains can't loop, branch, or hold evolving state — but agents need exactly that. LangGraph models your application as a **stateful graph**: nodes do work, edges route control, and cycles enable the "think → act → observe → repeat" loop that defines agents. This is the backbone framework for the entire Agents phase ahead.

## Learning objectives
1. Model an application as a typed state graph (state, nodes, edges).
2. Add conditional routing and cycles (loops) safely.
3. Build a tool-using loop as a graph.

## Topics to master (in detail)
### A. Graph model
- State schema (`TypedDict`/Pydantic) and state reducers (how updates merge)
- Nodes as functions that read/return state
- Edges: normal, conditional, and the `START`/`END` sentinels

### B. Control flow
- Conditional edges (route based on state)
- Cycles/loops and preventing infinite loops (step limits)
- Branching and merging paths

### C. A graph-based agent loop
- LLM node emits tool calls → tool node executes → loop back
- `ToolNode` and prebuilt helpers
- Comparing graph agents vs linear chains

## Tools for this week
- langgraph, langchain-core, an LLM, your Week 12 tools

## Guided coding labs
1. Build a 3-node graph with conditional routing based on state.
2. Add a cycle with a step-limit guard.
3. Implement an LLM ↔ tool loop as a graph (mini agent).

## Mini project
**Graph-based tool agent** — a LangGraph app that loops between an LLM and tools to answer multi-step questions, with a loop guard and traced state. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Working state graph with routing + cycle
- Graph agent that uses tools in a loop
- Notes: how state evolved across steps

## Checkpoints before moving on
- You can build a graph with conditional edges and a safe cycle.
- You understand how state updates/merges across nodes.
- You can implement an LLM–tool loop as a graph.

## Suggested study split (8–10 hours)
1. Concept learning: 2.5h
2. Guided implementation: 4h
3. Experiments: 1.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
