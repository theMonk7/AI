# Week 11: LangChain Core — LCEL, Runnables, Prompts, Parsers

## Phase
Phase 4 — LangChain & LangGraph

## Where this fits
- **Prerequisites:** Phases 2–3 (LLM calls, structured outputs, RAG).
- **Next:** Week 12 wires retrieval, memory, and tools into LangChain.

## Why this week matters
LangChain is the most widely used LLM orchestration framework. Its modern core — LCEL (LangChain Expression Language) and Runnables — lets you compose prompts, models, and parsers into pipelines that stream, batch, and run async by default. Learning the *core abstractions* (not memorizing every integration) is what makes you productive and framework-fluent.

## Learning objectives
1. Compose chains with LCEL (`|` pipe) from prompt → model → parser.
2. Use the Runnable interface (`invoke`, `batch`, `stream`, `ainvoke`).
3. Produce structured outputs with output parsers and `with_structured_output`.

## Topics to master (in detail)
### A. Core primitives
- Chat models & message types in LangChain
- Prompt templates (system/human, few-shot, partials)
- Output parsers (str, JSON, Pydantic) and `with_structured_output`

### B. LCEL & Runnables
- The `|` pipe: prompt | model | parser
- `RunnablePassthrough`, `RunnableParallel`, `RunnableLambda`
- `invoke` / `batch` / `stream` / async variants
- Configuration, fallbacks, and retries at the chain level

### C. Practical patterns
- Reusing your Week 4–5 prompting/structured-output skills in LangChain
- When to use LangChain vs raw SDK calls (trade-offs)

## Tools for this week
- langchain, langchain-core, an LLM provider (OpenAI or Ollama via langchain)

## Guided coding labs
1. Build a `prompt | model | parser` chain returning a Pydantic object.
2. Use `RunnableParallel` to run two sub-chains and merge results.
3. Stream and batch the same chain; compare behavior.

## Mini project
**Composable LLM chain toolkit** — a small set of reusable LCEL chains (summarize, extract, classify) with structured outputs and fallbacks. (Brief + skeleton + rubric.)

## Deliverables / evidence
- LCEL chains with structured outputs
- Streaming + batch demo
- Notes: where LCEL helped vs raw SDK

## Checkpoints before moving on
- You can compose, stream, and batch chains with LCEL.
- You can return validated structured objects from a chain.

## Suggested study split (8–10 hours)
1. Concept learning: 2.5h
2. Guided implementation: 4h
3. Experiments: 1.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
