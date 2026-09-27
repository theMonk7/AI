# Agentic AI Mastery (24 Weeks)

This repo is your code-first curriculum to reach strong mid-level and near-senior practical skill in:
- Agentic AI systems
- RAG pipelines
- LangChain and workflow orchestration
- Automation tools (n8n-first)
- Async Python for production AI apps

## Who this is for
You know Python and basic ML concepts, and want to build real systems end-to-end.

## Learning model
Each week follows this loop:
1. Learn core concepts.
2. Build guided examples.
3. Ship one small deliverable.
4. Measure quality (tests/evals/cost/latency).

## Time budget
- Target: 8 to 10 hours per week
- Timeline: 24 weeks

## Repo structure
- `docs/24_week_syllabus.md`: week-by-week curriculum
- `docs/tooling_map.md`: in-demand tools and why they matter
- `docs/roadmap/00_start_here.md`: first file to open each session
- `docs/roadmap/roadmap_state.md`: current week and next action
- `docs/roadmap/progress_tracker.md`: weekly evidence and reflections
- `docs/roadmap/weeks/`: detailed week-by-week teaching plans
- `src/weeks/week_01/`: all Week 1 source code (foundations, llm_core, projects)
- `src/weeks/week_01/README.md`: week source index and run commands
- `automation/n8n/`: n8n setup and workflow exports
- `tests/`: unit and integration tests

## Session continuity
To resume from any future agent session:
1. Open `docs/roadmap/00_start_here.md`.
2. Check `docs/roadmap/roadmap_state.md`.
3. Continue the active week from `docs/roadmap/weeks/week-XX/README.md`.
4. Log progress in `docs/roadmap/progress_tracker.md`.

## Quick start
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure environment variables:
   - Copy `.env.example` to `.env`
4. Run starter examples:
   - `python src/weeks/week_01/foundations/async_patterns.py`
   - `python src/weeks/week_01/foundations/reliable_client.py`

## Milestones
- Week 4: async and reliability baseline
- Week 10: robust RAG baseline with evals
- Week 16: automation portfolio (n8n + orchestration)
- Week 22: production hardening with eval gates
- Week 24: capstone demo and architecture review

## Capstone target
Build a domain-specific autonomous assistant with:
- RAG retrieval
- tool use
- workflow state machine
- n8n automation layer
- observability and evaluation reports

## Notes
The first implementation batch includes Weeks 1-4 starter code. Additional modules for RAG, LangChain graphs, and multi-agent orchestration will be added in next steps.
