# Week 19: n8n Fundamentals + Integrating Python/LLM Services

## Phase
Phase 6 — Agentic Automation

## Where this fits
- **Prerequisites:** Phase 5 (agents). You now have agents to automate *with*.
- **Next:** Week 20 (agentic automation + orchestrator comparison).

## Why this week matters
n8n is a leading open-source, self-hostable workflow automation tool (a free "Zapier you own"). It connects apps, APIs, and now AI into event-driven workflows with a visual editor. Learning n8n lets you deploy your agents/RAG into real automations — triggered by webhooks, schedules, emails, chat — which is exactly the "automation using agentic AI" you want.

## Learning objectives
1. Run n8n locally (Docker) and build workflows visually.
2. Use triggers, nodes, data mapping, and error handling.
3. Call your Python/LLM services from n8n via HTTP/webhooks.

## Topics to master (in detail)
### A. n8n core
- Install/run n8n locally with Docker
- Nodes, connections, and the execution model
- Triggers: webhook, schedule/cron, manual, app events
- Passing and transforming data between nodes (expressions, JSON)
- Credentials management and error/retry settings

### B. Integrating your code
- HTTP Request node → your FastAPI (RAG/agent) endpoints
- Webhook node → receive events → call Python → respond
- Function/Code node for light in-workflow logic

### C. Practical patterns
- Idempotency and retries in workflows
- Logging and debugging executions

## Tools for this week
- n8n (Docker), your FastAPI RAG/agent service, webhooks

## Guided coding labs
1. Stand up n8n locally and build a webhook → transform → respond flow.
2. Call your RAG API from n8n and return the answer.
3. Add error handling + retry to a flaky external call.

## Mini project
**"Ask my docs" automation** — an n8n workflow that receives a question (webhook/chat), calls your RAG service, and returns a cited answer, with error handling. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Exported n8n workflow JSON
- Working webhook → RAG → response demo
- Notes: where you added retries/error handling

## Checkpoints before moving on
- You can build and debug n8n workflows.
- n8n can call your Python/LLM services reliably.

## Suggested study split (8–10 hours)
1. Concept learning: 2h
2. Guided implementation: 4.5h
3. Integration + debugging: 1.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
