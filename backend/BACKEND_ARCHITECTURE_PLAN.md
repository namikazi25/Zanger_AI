# Backend Architecture Plan for Legal AI Chatbot

---

## To-Do Checklist

- [x] Repository Cleanup: Remove obsolete agent entrypoints; ensure `backend/app/agents/my_agent.py` is the sole agent entry
- [x] Directory Structure:
  - [x] `backend/app/agents/`: `planner.py`, `executor.py`, `evaluator.py`
  - [x] `backend/app/models/`: `router.py`, `gemini.py`, `gpt4o.py`
  - [x] `backend/app/tools/`: `search.py`
  - [x] `backend/app/storage/`: `session_store.py`, `placeholder_vector_db.py`
- [x] Environment & Configs:
  - [x] Add required keys to `.env`
- [x] Dependencies: Add to `requirements.txt`
  - [x] `langchain`
  - [x] `brave-search` (or equivalent)
  - [x] `python-mammoth`
  - [x] `pillow`
  - [x] `pgsql`
- [x] Model-Routing Layer:
  - [x] Implement `router.py` with policy logic
  - [x] Implement `gemini.py` and `gpt4o.py` wrappers
- [ ] Tool-Wrappers:
  - [x] Implement `BraveSearchTool` in `tools/search.py`
  - [x] Implement stubs in `storage/placeholder_vector_db.py`
- [ ] Agent Architecture:
  - [ ] Implement Planner (`agents/planner.py`)
  - [ ] Implement Executor (`agents/executor.py`)
  - [ ] Implement Evaluator (`agents/evaluator.py`)
  - [ ] Orchestrate in `my_agent.py`
  - [ ] Instrument logging for planning
- [ ] Multimodal Input/Output:
  - [ ] Extend Pydantic Schemas for file input
  - [ ] Implement mime-type detection and preprocessing
- [ ] Session & State Management:
  - [ ] Implement in-memory store (`storage/session_store.py`)
  - [ ] Prepare abstract interface for Postgres
- [ ] FastAPI Integration:
  - [ ] Add `/chat` route
  - [ ] Add middleware (logging, error handling, CORS, rate-limit stubs)
- [ ] Testing & CI:
  - [ ] Unit tests for Planner, Router, Tools
  - [ ] Integration tests for `/chat`
  - [ ] CI pipeline (lint, type-check, pytest)

This document outlines the step-by-step plan for evolving the backend of our AI-based Legal Chatbot. The focus is on modularity, extensibility, and robust orchestration, with a clear path for future enhancements.

---

## 1. Project Scaffolding & Infrastructure

- **Repository Cleanup**: Remove obsolete agent entrypoints; ensure `backend/app/agents/my_agent.py` is the sole agent entry.
- **Directory Structure**:
  - `backend/app/agents/`: `planner.py`, `executor.py`, `evaluator.py`
  - `backend/app/models/`: `router.py`, `gemini.py`, `gpt4o.py`
  - `backend/app/tools/`: `search.py`
  - `backend/app/storage/`: `session_store.py`, `placeholder_vector_db.py`
- **Environment & Configs**:
  - In `.env`, add:
    - `OPENAI_API_KEY=...`
    - `GEMINI_API_KEY=...`
    - `ENABLE_BRAVE_SEARCH=true`
    - `DEFAULT_MODEL_ROUTING_POLICY="balanced"` (e.g., "flash_first", "gpt4o_only")
- **Dependencies** (add to `requirements.txt`):
  - `langchain`, `brave-search` (or equivalent), `python-mammoth`, `pillow`, `pgsql`

---

## 2. Model-Routing Layer

- **router.py**: Expose `get_model(session_state, policy)` returning a LangChain-wrapped model instance. Map abstract policies to concrete clients:
  - If `policy == "flash_first"`: try Gemini, fallback to GPT4o
  - If `policy == "gpt4o_only"`: always GPT4o
- **gemini.py / gpt4o.py**: Implement a common interface:
  ```python
  class BaseModelWrapper(ABC):
      async def generate(self, prompt, **kwargs) -> str: ...
  class GeminiFlash(BaseModelWrapper): ...
  class GPT4O(BaseModelWrapper): ...
  ```

---

## 3. Tool-Wrappers

- **tools/search.py**: Implement `BraveSearchTool` with `run(query)` returning structured results (titles, URLs, snippets). Integrate with LangChain's Tools API.
- **storage/placeholder_vector_db.py**: Expose `add(doc)` and `query(vec)` stubs. Return dummy results but shape I/O for easy swap to e.g., Pinecone.

---

## 4. Agent Architecture

- **Planner (`agents/planner.py`)**: Input: user query + session metadata. Output: plan (sequence of tool/model calls). MVP: decide "search" → "model.generate(search_context + user_query)".
- **Executor (`agents/executor.py`)**: Walk the plan, invoke each step (tool/model).
- **Evaluator (`agents/evaluator.py`)**: Optionally score/validate output (MVP: log and pass through).
- **Agent Orchestration (`my_agent.py`)**:
  ```python
  plan = await Planner.plan(query, session)
  results = await Executor.execute(plan)
  final = await Evaluator.evaluate(results)
  return final.response
  ```
- Instrument logging to show planning in API response metadata for debugging.

---

## 5. Multimodal Input/Output

- **Pydantic Schemas**: Extend `ChatRequest` to accept optional files: `List[UploadFile]`.
- **Mime-Type Detection**: Dispatch images to Pillow, docs to python-mammoth.
- **LangChain Pipelines**: For images/docs, wrap in a preprocessor that extracts text/embeddings for the model prompt.

---

## 6. Session & State Management

- **In-Memory Store (`storage/session_store.py`)**: Dict mapping `session_id` to `SessionData` (history, metadata, etc). Provide `get`, `append_message`, `clear`.
- **Abstract Interface**: Prepare for future Postgres swap (implement `SQLSessionStore` behind same API).

---

## 7. FastAPI Integration

- **Routes**: `POST /chat` loads/creates session, calls orchestration, returns `{response, plan, tool_outputs, citations}`.
- **Middleware**: Add request logging, error handling, CORS, rate-limit stubs.

---

## 8. Testing & CI

- **Unit Tests**:
  - Planner: ensure expected tool calls for queries
  - Router: correct model selection under policies
  - Tools: mock search API for predictable snippets
- **Integration Tests**:
  - Use TestClient; run `/chat` with text/image payloads; assert valid JSON response
- **CI Pipeline**:
  - Lint, type-check, pytest

---

## Next Steps

1. Scaffold directories and files as above.
2. Implement stubs for each module, then incrementally build out logic.
3. Update `.env` and `requirements.txt`.
4. Add/expand tests as features are implemented.