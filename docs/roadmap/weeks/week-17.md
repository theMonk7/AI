# Week 17: Multi-Agent Systems — Supervisor, Hierarchical, CrewAI, AutoGen

## Phase
Phase 5 — Agents & Agentic AI

## Where this fits
- **Prerequisites:** Week 16 (custom + LangGraph agents).
- **Next:** Week 18 (memory, skills, MCP) to make agents durable and extensible.

## Why this week matters
Hard problems are solved by *teams* of specialized agents, not one do-everything agent. Multi-agent architectures (a supervisor delegating to workers, hierarchical teams, debating/critiquing agents) are a leading pattern in production agentic AI. You'll learn the patterns and the top frameworks (LangGraph multi-agent, CrewAI, AutoGen).

## Learning objectives
1. Design multi-agent topologies (supervisor, hierarchical, collaborative).
2. Implement a supervisor + workers system in LangGraph.
3. Compare CrewAI and AutoGen and know when to choose each.

## Topics to master (in detail)
### A. Multi-agent patterns
- Supervisor/router delegating to specialist agents
- Hierarchical teams (supervisor of supervisors)
- Collaboration/debate, critic/reviewer agents
- Shared state vs message passing between agents
- Handoffs and when to terminate

### B. Frameworks
- LangGraph multi-agent (custom, full control)
- **CrewAI** — role/goal/task-based crews (fast to build)
- **AutoGen** — conversational multi-agent (flexible dialogues)
- Choosing based on control, complexity, and team ergonomics

### C. Reliability at scale
- Avoiding infinite agent chatter (turn limits, budgets)
- Cost explosion risks and how to cap them
- Deterministic routing where possible

## Tools for this week
- langgraph, crewai, pyautogen (AutoGen), an LLM

## Guided coding labs
1. Build a supervisor + 2 specialist workers in LangGraph.
2. Recreate a similar crew in CrewAI; compare developer experience.
3. Run an AutoGen two-agent conversation with a critic.

## Mini project
**Research/writing crew** — a supervisor delegating to researcher + writer + reviewer agents that produce a cited report, with turn/cost limits. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Working multi-agent system (LangGraph)
- CrewAI/AutoGen comparison notes
- Notes: where multi-agent beat single-agent (and where it didn't)

## Checkpoints before moving on
- You can design and build a supervisor/worker system.
- You can justify a framework choice.
- Your system has turn/cost guardrails.

## Suggested study split (8–10 hours)
1. Concept learning: 2.5h
2. LangGraph multi-agent build: 3.5h
3. Framework comparison: 2h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
