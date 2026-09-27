# Week 04: How LLMs Work + Calling LLM APIs + Prompt Engineering

## Phase
Phase 2 — LLM Application Fundamentals

## Where this fits
- **Prerequisites:** Weeks 1–3 (async, typed clients, validation).
- **Next:** Week 5 (structured outputs & tool calling) turns raw LLM calls into reliable, machine-usable results.

## Why this week matters
LLMs are the engine of everything ahead. You do not need the deep math, but you must understand — at a working level — what a token is, what the context window limits, how sampling (temperature) changes behavior, and how to talk to models (hosted and local). Prompt engineering is the highest-leverage skill in the entire field.

## Learning objectives
1. Explain tokens, context windows, temperature/top-p, and cost in plain terms.
2. Call a hosted LLM (OpenAI) and a local LLM (Ollama) from Python.
3. Design effective prompts (system/user roles, few-shot, delimiters, instructions).
4. Measure and control cost + latency with token counting.

## Topics to master (in detail)
### A. LLM mental model (no heavy math)
- What a token is; tokenization and why it matters for cost/limits
- Context window: what fits, truncation, and why "long context ≠ free"
- Sampling: temperature, top-p, max tokens, stop sequences
- Determinism vs creativity; when to set temperature=0
- Model families & selection (small vs large, hosted vs open-weight)

### B. Calling LLMs from Python
- OpenAI Chat Completions API (messages, roles)
- Running open models locally with **Ollama** (free, private)
- **LiteLLM** to switch providers behind one interface
- Streaming token responses (reuse Week 3 async generators)

### C. Prompt engineering fundamentals
- Roles: system vs user vs assistant
- Instruction clarity, delimiters, examples (few-shot), output format hints
- Chain-of-thought vs concise answers; when each helps
- Prompt templates and variables (sets up LangChain later)

### D. Cost & latency awareness
- Token counting with `tiktoken`; estimating request cost
- Caching and prompt-size discipline

## Tools for this week
- OpenAI API, Ollama, LiteLLM, tiktoken

## Guided coding labs
1. Send the same prompt at temperature 0 vs 1 and compare outputs.
2. Run the same prompt on a hosted model and a local Ollama model.
3. Count tokens and estimate cost for a batch of prompts.

## Mini project
**Multi-provider prompt playground** — a script that runs a prompt against OpenAI and a local Ollama model, streams output, counts tokens, and logs cost/latency for each. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Working hosted + local LLM calls
- Token/cost log artifact
- Notes: 3 prompt techniques that measurably improved output

## Checkpoints before moving on
- You can call both a hosted and a local model.
- You can explain temperature, context window, and token cost.
- You can improve a weak prompt and justify why it's better.

## Suggested study split (8–10 hours)
1. Concept learning: 3h
2. Guided implementation: 3.5h
3. Prompt experiments: 1.5h
4. Reflection and notes: 1–2h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
