# Week 12: LangChain Retrieval, Memory & Tools (RAG in LangChain)

## Phase
Phase 4 — LangChain & LangGraph

## Where this fits
- **Prerequisites:** Week 11 (LCEL, Runnables).
- **Next:** Week 13 (LangGraph) — stateful graphs for anything a linear chain can't express.

## Why this week matters
Now you connect LangChain's core to the real building blocks: retrievers (RAG), memory (conversation state), and tools (actions). Rebuilding your Phase 3 RAG inside LangChain shows how the framework accelerates real apps — and reveals its limits, which motivates LangGraph next week.

## Learning objectives
1. Build a retrieval chain (RAG) in LangChain with your vector store.
2. Add conversation memory and history-aware retrieval.
3. Define and bind tools to a model; execute tool calls.

## Topics to master (in detail)
### A. Retrieval in LangChain
- `VectorStore` + `Retriever` interfaces (FAISS/Qdrant integrations)
- Retrieval chains and the modern `create_retrieval_chain` pattern
- History-aware retriever (rewrite follow-up questions using chat history)
- Passing citations through the chain

### B. Memory & state
- Chat message history and windowed/summary memory
- Why naive memory doesn't scale (motivates LangGraph persistence)

### C. Tools
- Defining tools (`@tool`), tool schemas, and `bind_tools`
- Executing tool calls and returning results to the model
- Built-in vs custom tools; safety on tool execution

## Tools for this week
- langchain, langchain integrations, your Qdrant/FAISS store, an LLM

## Guided coding labs
1. Rebuild your RAG as a LangChain retrieval chain with citations.
2. Add history-aware retrieval so follow-up questions work.
3. Bind two tools to a model and run a tool call.

## Mini project
**Conversational RAG assistant** in LangChain: memory + history-aware retrieval + a tool (e.g., calculator or web/search stub), returning cited answers. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Conversational RAG chain with memory
- Working tool binding + execution
- Notes: where linear chains became awkward (sets up LangGraph)

## Checkpoints before moving on
- Multi-turn RAG works with history-aware retrieval.
- You can define, bind, and execute tools.
- You can articulate why you need a graph for complex control flow.

## Suggested study split (8–10 hours)
1. Concept learning: 2h
2. Guided implementation: 4.5h
3. Experiments: 1.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
