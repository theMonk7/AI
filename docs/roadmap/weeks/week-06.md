# Week 06: Embeddings, Semantic Search & Your First RAG

## Phase
Phase 2 — LLM Application Fundamentals

## Where this fits
- **Prerequisites:** Weeks 4–5 (LLM calls, structured outputs).
- **Next:** Phase 3 (Weeks 7–10) turns this naive RAG into a production pipeline.

## Why this week matters
Embeddings are how machines measure *meaning*. They power semantic search, RAG, recommendation, clustering, and agent memory. This week you build intuition for vectors and similarity (no heavy math), then assemble your first end-to-end Retrieval-Augmented Generation (RAG) system — the single most common real-world LLM application.

## Learning objectives
1. Explain embeddings and cosine similarity intuitively.
2. Generate embeddings locally (free) and via API.
3. Build a naive RAG: embed docs → store → retrieve top-k → stuff into prompt → answer.

## Topics to master (in detail)
### A. Embeddings intuition
- What an embedding is: text → vector capturing meaning
- Cosine similarity / distance (concept, not proofs)
- Embedding models: `sentence-transformers` (local, free) vs API embeddings
- Dimensions, normalization, and what "similar" really means

### B. Semantic search basics
- Building a query: embed the query, compare to document vectors
- Top-k retrieval and why k matters
- Keyword search vs semantic search (and why hybrid wins later)

### C. Naive RAG end-to-end
- The RAG loop: **retrieve → augment prompt → generate**
- Why RAG (grounding, reducing hallucination, fresh/private data)
- Prompt design for RAG (context injection, "answer only from context")
- Failure modes: irrelevant retrieval, context overflow, hallucinated citations

## Tools for this week
- sentence-transformers, numpy, a simple in-memory or FAISS index, an LLM (Week 4)

## Guided coding labs
1. Embed a set of sentences and rank them by similarity to a query.
2. Build a tiny vector store (list of vectors) with top-k cosine search.
3. Assemble naive RAG: retrieve context, inject into prompt, generate a grounded answer.

## Mini project
**Naive RAG Q&A over your own notes** — ingest a folder of text/markdown, embed and index it, and answer questions grounded in the retrieved chunks with citations. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Working semantic search demo
- Naive RAG answering questions with citations
- Notes: cases where retrieval failed and why

## Checkpoints before moving on
- You can explain embeddings and cosine similarity in your own words.
- Your RAG answers only from retrieved context and cites sources.
- You can identify at least two RAG failure modes.

## Suggested study split (8–10 hours)
1. Concept learning: 2.5h
2. Guided implementation: 4h
3. Experiments with k/prompts: 1.5h
4. Reflection and notes: 1–2h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
