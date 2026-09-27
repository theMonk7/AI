# Week 07: Document Ingestion & Chunking Strategies

## Phase
Phase 3 — RAG Pipelines

## Where this fits
- **Prerequisites:** Week 6 (embeddings, naive RAG).
- **Next:** Week 8 (vector stores & retrieval) indexes the chunks you produce here.

## Why this week matters
Retrieval quality is capped by ingestion quality: "garbage in, garbage out." How you load, clean, chunk, and attach metadata to documents determines whether your RAG finds the right context. This is the least glamorous and most impactful part of RAG.

## Learning objectives
1. Load and parse diverse sources (PDF, HTML, markdown, code) into clean text.
2. Choose chunking strategies deliberately and understand their trade-offs.
3. Attach normalized metadata for filtering and citations.

## Topics to master (in detail)
### A. Loading & parsing
- Loaders for PDF (`pypdf`), HTML, markdown, plaintext, code
- Cleaning: whitespace, boilerplate removal, encoding issues
- `unstructured` for messy real-world documents (overview)

### B. Chunking strategies (the core skill)
- Fixed-size vs recursive character splitting
- Token-based chunking (align with embedding model limits)
- Semantic / structure-aware chunking (headings, paragraphs, code blocks)
- Chunk size vs overlap trade-offs (recall vs precision vs cost)
- Parent/child chunking (small chunks to retrieve, large to read)

### C. Metadata & normalization
- Source, title, section, page, timestamps, tags
- Why metadata enables filtering, citations, and hybrid ranking
- Consistent schema across sources (Pydantic model for a chunk)

## Tools for this week
- pypdf, markdown, unstructured (overview), LangChain text splitters (or custom), Pydantic

## Guided coding labs
1. Ingest a PDF + markdown set into a unified cleaned-text form.
2. Benchmark 3 chunk configurations (size/overlap) on retrieval recall.
3. Produce a normalized `Chunk` dataset with consistent metadata.

## Mini project
**Ingestion pipeline** producing a normalized, metadata-rich chunk dataset from mixed document types, with a report comparing chunk configs. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Chunk dataset (with metadata) artifact
- Chunk-config comparison report
- Notes: which chunking won for your corpus and why

## Checkpoints before moving on
- Chunks are clean, consistently sized, and carry citation metadata.
- You can justify your chunking choice with evidence.

## Suggested study split (8–10 hours)
1. Concept learning: 2h
2. Guided implementation: 4h
3. Chunk experiments: 2h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
