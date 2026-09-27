# Week 09: Advanced RAG — Reranking & Query Transformation

## Phase
Phase 3 — RAG Pipelines

## Where this fits
- **Prerequisites:** Week 8 (vector stores, hybrid retrieval).
- **Next:** Week 10 (RAG evaluation) measures whether these techniques actually help.

## Why this week matters
Naive top-k retrieval is often "good enough to demo, too weak to ship." Advanced RAG techniques — reranking, query rewriting, HyDE, multi-query, contextual retrieval — close the gap between mediocre and production-grade answer quality. Senior engineers know *which* technique to reach for and can prove it helped.

## Learning objectives
1. Rerank retrieved candidates with a cross-encoder for large quality gains.
2. Improve recall with query transformation techniques.
3. Assemble an advanced RAG pipeline and reason about each stage.

## Topics to master (in detail)
### A. Reranking
- Bi-encoder (retrieval) vs cross-encoder (reranking) — why two stages
- Cross-encoder rerankers (sentence-transformers) / Cohere Rerank (API)
- Retrieve many (e.g. 50) → rerank → keep few (e.g. 5)

### B. Query transformation
- Query rewriting / expansion for better recall
- Multi-query retrieval (generate variations, union results)
- HyDE (Hypothetical Document Embeddings)
- Step-back prompting for broad questions

### C. Context construction
- Contextual retrieval (prepend chunk context before embedding)
- Parent-document retrieval (retrieve small, supply large)
- De-duplication, ordering, and context-window budgeting
- Citation-preserving context assembly

## Tools for this week
- sentence-transformers cross-encoder, your Week 8 retriever, an LLM for query rewriting

## Guided coding labs
1. Add a cross-encoder reranker; compare answers with/without it.
2. Implement multi-query retrieval and measure recall change.
3. Add parent-document retrieval and observe answer completeness.

## Mini project
**Advanced RAG pipeline**: hybrid retrieve → multi-query → rerank → parent-doc context → grounded answer with citations. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Advanced RAG pipeline code
- Before/after examples showing improvement
- Notes: which technique helped most on your corpus

## Checkpoints before moving on
- Reranking measurably improves answer relevance.
- You can explain when to use each query-transformation technique.

## Suggested study split (8–10 hours)
1. Concept learning: 2.5h
2. Guided implementation: 4h
3. A/B experiments: 1.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
