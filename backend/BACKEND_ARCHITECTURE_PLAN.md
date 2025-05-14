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
- [x] Agent Architecture:
  - [x] Implement Planner (`agents/planner.py`)
  - [x] Implement Executor (`agents/executor.py`)
  - [x] Implement Evaluator (`agents/evaluator.py`)
  - [x] Orchestrate in `my_agent.py`
  - [x] Instrument logging for planning
- [x] Multimodal Input/Output:
  - [x] Extend Pydantic Schemas for file input
  - [x] Implement mime-type detection and preprocessing
- [ ] Session & State Management:
  - [x] Implement supabase memory store (`storage/session_store.py`)
  - [ ] Prepare interface for Postgres
- [x] FastAPI Integration:
  - [x] Add `/chat` route
  - [x] Add middleware (logging, error handling, CORS, rate-limit stubs)
- [x] Testing & CI:
  - [x] Unit tests for Planner, Router, Tools
  - [x] Integration tests for `/chat`
  - [x] CI pipeline (lint, type-check, pytest)

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

- **Pydantic Schemas**: Extended `ChatRequest` to accept optional files: `List[UploadFile]`.
- **Mime-Type Detection**: Implemented mime-type detection and preprocessing for images (Pillow) and documents (python-mammoth) in `app/utils/preprocessing.py`. Integrated into `my_agent.py`.
- **LangChain Pipelines**: For images/docs, wrap in a preprocessor that extracts text/embeddings for the model prompt.

---

## 6. Session & State Management

# 6. Session & State Management (GDPR-Compliant with Supabase)

## Overview

This module replaces the in-memory session store with a **Supabase PostgreSQL-backed** session store. It ensures **GDPR compliance** through encryption, user data control, and auto-expiry mechanisms.

---

## ✅ SupabaseSessionStore (`storage/session_store.py`)

Implements the following methods:

- `get(session_id)`: Retrieve decrypted messages and metadata
- `append_message(session_id, message)`: Encrypt and append a message
- `clear(session_id)`: Delete the session
- `delete_session(session_id)`: Explicit delete for GDPR "Right to be Forgotten"

### Example PostgreSQL Table Schema (Supabase)
```sql
CREATE TABLE sessions (
  session_id TEXT PRIMARY KEY,
  messages JSONB,           -- Encrypted text values
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

Example Message Format (stored)
json
Copy
Edit
[
  {
    "role": "user",
    "text": "<encrypted string>",
    "timestamp": "2025-05-13T09:00:00"
  },
  {
    "role": "agent",
    "text": "<encrypted string>",
    "timestamp": "2025-05-13T09:00:05"
  }
]
🔐 Encryption Layer (app/utils/crypto.py)
Implements AES-256 or Fernet encryption:

python
Copy
Edit
from cryptography.fernet import Fernet
import os

fernet = Fernet(os.getenv("FERNET_KEY"))

def encrypt_message(msg: str) -> str:
    return fernet.encrypt(msg.encode()).decode()

def decrypt_message(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
Encrypt only sensitive fields (message['text']). Metadata like timestamps or model name can be stored as plain text.

🔁 SupabaseSessionStore Sample Logic
python
Copy
Edit
class SupabaseSessionStore:
    def __init__(self):
        self.client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_API_KEY"))

    def get(self, session_id: str) -> dict:
        response = self.client.table("sessions").select("*").eq("session_id", session_id).single().execute()
        if not response.data:
            return {}
        decrypted = [
            {
                "role": msg["role"],
                "text": decrypt_message(msg["text"]),
                "timestamp": msg["timestamp"]
            } for msg in response.data["messages"]
        ]
        return {"session_id": session_id, "messages": decrypted, "metadata": response.data["metadata"]}

    def append_message(self, session_id: str, message: dict):
        encrypted_message = {
            "role": message["role"],
            "text": encrypt_message(message["text"]),
            "timestamp": message["timestamp"]
        }
        existing = self.get(session_id)
        messages = existing.get("messages", []) + [encrypted_message]
        metadata = existing.get("metadata", {})
        self.client.table("sessions").upsert({
            "session_id": session_id,
            "messages": messages,
            "metadata": metadata
        }).execute()

    def clear(self, session_id: str):
        self.client.table("sessions").delete().eq("session_id", session_id).execute()
⚖️ GDPR Compliance Checklist
 Encryption: All message content is encrypted before storage

 Right to be Forgotten: Users can delete their session (clear)

 Auto-Expiry: Set up Supabase cron job or pg_cron to delete stale sessions

 Key Management: Store FERNET_KEY in environment, rotate periodically

🔧 .env Variables
ini
Copy
Edit
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_API_KEY=your-service-role-key
FERNET_KEY=your-generated-key
Generate FERNET_KEY using:

bash
Copy
Edit
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
🛠️ Next Steps
Create sessions table in Supabase

Replace in-memory logic with SupabaseSessionStore

Implement crypto.py and store encryption key securely

Write unit tests for get, append_message, and clear

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