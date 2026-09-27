# Week 18: Agent Memory, Skills & MCP (Model Context Protocol)

## Phase
Phase 5 — Agents & Agentic AI

## Where this fits
- **Prerequisites:** Weeks 15–17 (agents, multi-agent).
- **Next:** Phase 6 (agentic automation with n8n) — deploy agents into real workflows.

## Why this week matters
To be genuinely useful, agents need **memory** (remember across sessions), reusable **skills** (packaged capabilities they can invoke), and a standard way to connect to **tools and data** — which is exactly what **MCP (Model Context Protocol)** provides. MCP is rapidly becoming the industry standard for agent–tool integration, so this week is highly in-demand and career-relevant.

## Learning objectives
1. Implement short-term and long-term agent memory.
2. Package reusable "skills" an agent can discover and invoke.
3. Understand and use MCP to expose/consume tools and data.

## Topics to master (in detail)
### A. Agent memory
- Short-term (conversation buffer/window) vs long-term (persistent)
- Vector-store memory (semantic recall of past interactions)
- Summarization/compaction to fit the context window
- Episodic vs semantic vs procedural memory (concepts)
- Reuse LangGraph checkpointers (Week 14) for durable memory

### B. Skills
- What a "skill" is: a packaged, reusable capability/tool with a clear contract
- Skill discovery, selection, and composition
- Designing skills with schemas, docs, and safety boundaries

### C. MCP (Model Context Protocol)
- The problem MCP solves: a standard interface between agents and tools/data
- MCP servers (expose tools/resources) and clients (agents that consume them)
- Building a simple MCP server and connecting an agent to it
- Why MCP matters for interoperability and portability

## Tools for this week
- MCP SDK, a vector store (memory), langgraph, an LLM

## Guided coding labs
1. Add long-term vector memory so the agent recalls prior sessions.
2. Package two capabilities as reusable skills with schemas.
3. Build a minimal MCP server and connect your agent to it.

## Mini project (Phase 5 capstone)
**Skilled agent with memory over MCP** — an agent that remembers users across sessions and invokes tools exposed via an MCP server. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Agent with persistent memory demo
- MCP server + connected agent
- Notes: what memory type fit your use case

## Checkpoints before moving on
- Your agent remembers across sessions.
- You can package and reuse skills.
- You can connect an agent to tools via MCP.

## Suggested study split (8–10 hours)
1. Concept learning: 2.5h
2. Memory + skills: 3h
3. MCP build: 2.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
