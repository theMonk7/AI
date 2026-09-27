# Week 08: Vector Stores & Retrieval (FAISS, Qdrant, Hybrid)

## Phase
Phase 3 — RAG Pipelines

## Where this fits
- **Prerequisites:** Week 7 (chunks + metadata).
- **Next:** Week 9 (advanced RAG) improves the retrieval you build here.

## Why this week matters
A vector store is the memory of your RAG system. Choosing and operating one — plus combining semantic (dense) and keyword (sparse) search — is a core production skill. Pure semantic search misses exact terms; pure keyword misses meaning. Hybrid retrieval is what real systems ship.

## Learning objectives
1. Store and query embeddings in FAISS (local) and Qdrant (production OSS).
2. Implement metadata filtering alongside vector search.
3. Build hybrid retrieval (BM25 + dense) and fuse the results.

## Topics to master (in detail)
### A. Vector databases
- FAISS: fast local index, when it's enough
- Qdrant (OSS): collections, payloads, filtering, persistence, Docker
- Chroma: lightweight local option
- pgvector: vectors inside PostgreSQL (when you already have Postgres)
- Index types & trade-offs (flat vs ANN) at a conceptual level

### B. Retrieval mechanics
- Top-k, similarity thresholds, and metadata filters
- Batching queries; latency considerations
- Storing enough metadata for citations

### C. Hybrid search
- Sparse retrieval with BM25 (`rank-bm25`)
- Dense retrieval with embeddings
- Fusion: Reciprocal Rank Fusion (RRF) and weighting
- Why hybrid beats either alone

## Tools for this week
- FAISS, Qdrant (Docker), rank-bm25, sentence-transformers

## Guided coding labs
1. Index your Week 7 chunks in FAISS and Qdrant; compare queries.
2. Add metadata filtering (e.g., restrict to a source or date).
3. Implement BM25 + dense hybrid retrieval with RRF fusion.

## Mini project
**Hybrid retrieval service** over your chunk dataset: dense + BM25 with RRF, metadata filtering, and citations, exposed via a function/endpoint. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Qdrant collection + working queries
- Hybrid retriever with fusion
- Notes: queries where hybrid beat pure semantic

## Checkpoints before moving on
- You can run retrieval on FAISS and Qdrant.
- Hybrid retrieval measurably improves results on some queries.
- Results carry metadata for citation.

## Suggested study split (8–10 hours)
1. Concept learning: 2h
2. Guided implementation: 4.5h
3. Comparison experiments: 1.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
