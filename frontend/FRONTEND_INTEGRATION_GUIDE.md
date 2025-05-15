# Frontend Integration Guide for Legal AI Chatbot

This document provides frontend developers with an overview of the backend services for the Legal AI Chatbot, details on implemented features, and guidance for integration.

---

## 1. Backend Overview

The backend is a FastAPI application designed to power the Legal AI Chatbot. It handles user queries, orchestrates interactions with AI models and tools, manages sessions, and provides responses.

**Key Technologies Used:**
- FastAPI for the web framework
- LangChain for AI agent orchestration
- Pydantic for data validation
- Supabase (PostgreSQL) for session storage (planned/implemented)

---

## 2. Implemented Backend Features

Based on the backend architecture plan and current codebase, the following features are implemented or substantially defined:

- **Core API Structure:**
  - FastAPI application setup.
  - `/chat` endpoint for primary interaction (details below).
  - `/` root endpoint for health check/welcome message.
- **Middleware:**
  - **CORS:** Configured with `allow_origins=["*"]`, `allow_credentials=True`, `allow_methods=["*"]`, `allow_headers=["*"]`. This allows requests from any origin, which is suitable for development but may need refinement for production.
  - **Logging:** Detailed request/response logging, including processing time.
  - **Error Handling:** Graceful handling of HTTP errors and unexpected exceptions, returning structured JSON error messages.
  - **Rate Limiting:** A stub for rate limiting is in place (currently logs client IP, no actual limiting).
- **Agent Architecture:**
  - Planner, Executor, and Evaluator components for processing user requests.
  - Orchestration logic within `my_agent.py`.
- **Model Routing:**
  - Dynamic routing to different AI models (e.g., Gemini, GPT-4o) based on policies.
- **Tool Integration:**
  - `BraveSearchTool` for web search capabilities.
  - Placeholder for a vector database for document querying.
- **Multimodal Input/Output:**
  - Backend schemas (`ChatRequest`) support optional file uploads (`List[UploadFile]`).
  - Mime-type detection and preprocessing for images (Pillow) and documents (python-mammoth).
- **Session & State Management (Supabase Integration):**
  - `SupabaseSessionStore` is designed for GDPR-compliant session management using Supabase (PostgreSQL).
  - Features include encrypted message storage, retrieval, and deletion.
  - **Key Environment Variables for Backend (Frontend might not need these directly but good to be aware):**
    - `OPENAI_API_KEY`
    - `GEMINI_API_KEY`
    - `ENABLE_BRAVE_SEARCH`
    - `DEFAULT_MODEL_ROUTING_POLICY`
    - `SUPABASE_URL`
    - `SUPABASE_API_KEY`
    - `FERNET_KEY` (for message encryption)
- **Testing & CI:**
  - Unit and integration tests are part of the backend development process.

---

## 3. API Endpoints for Frontend Integration

### 3.1. Root Endpoint

- **Path:** `/`
- **Method:** `GET`
- **Description:** A simple endpoint to check if the backend is running.
- **Response (Success - 200 OK):**
  ```json
  {
    "message": "Welcome to the Legal AI Chatbot Backend"
  }
  ```

### 3.2. Chat Endpoint

- **Path:** `/chat` (exact path defined in `backend/app/routes/chat.py`, assumed to be `/chat`)
- **Method:** `POST`
- **Description:** The primary endpoint for sending user queries and receiving AI-generated responses. It handles session management and orchestration of AI tasks.
- **Request Body (Expected Pydantic Schema - `ChatRequest`):**
  - The backend's `ChatRequest` schema is extended to accept optional files: `List[UploadFile]`.
  - A typical request might look like (frontend will need to construct `FormData` if files are included):
    ```json
    {
      "query": "User's text query",
      "session_id": "optional_existing_session_id", // Backend likely handles session creation/retrieval
      "files": [] // List of files if any, handled as multipart/form-data
    }
    ```
    *Frontend will need to send files as `multipart/form-data`.*
- **Response Body (Expected - based on architecture plan):**
  ```json
  {
    "response": "The AI's answer to the query",
    "plan": "Details of the execution plan (for debugging/info)",
    "tool_outputs": "Outputs from any tools used (e.g., search results)",
    "citations": "Relevant citations if applicable"
    // Potentially session_id if a new session was created
  }
  ```
- **Error Responses:**
  - Standard HTTP error codes (e.g., 4xx, 5xx) with a JSON body:
    ```json
    {
      "detail": "Error message"
    }
    ```
    For example, a 500 Internal Server Error:
    ```json
    {
      "detail": "Internal Server Error"
    }
    ```

---

## 4. Frontend Implementation Tasks

Based on the backend capabilities and the identified frontend stack (React, Vite, TypeScript, Tailwind CSS), the frontend team will need to implement the following:

1.  **User Interface (UI) for Chat (React & Tailwind CSS):**
    *   Develop React components for the chat interface (e.g., `ChatInput.tsx`, `MessageList.tsx`, `MessageItem.tsx`).
    *   Utilize Tailwind CSS for styling to ensure a responsive and modern UI.
    *   Input field for text queries.
    *   Display area for chat history (user messages and AI responses).
    *   Mechanism for displaying AI responses, including formatted text, and potentially handling citations or tool outputs if provided by the backend.
2.  **File Upload Functionality (React):**
    *   Implement a React component for file selection (e.g., `<input type="file">` or a custom component) allowing users to upload images and documents.
    *   Use JavaScript's `FormData` API to construct the `multipart/form-data` request when files are included.
    *   Ensure files are sent as `multipart/form-data` to the `/chat` endpoint.
3.  **API Integration (TypeScript & Fetch/Axios):**
    *   Use TypeScript for type-safe API request and response handling (define interfaces/types for `ChatRequest` and `ChatResponse` based on backend Pydantic models).
    *   Make `POST` requests to the `/chat` endpoint using the `fetch` API or a library like `axios`.
    *   Handle responses, including successful AI messages and error messages, updating the React state accordingly.
4.  **State Management (React):**
    *   Manage application state (e.g., chat messages, loading status, errors) using React's built-in state management (useState, useReducer) or a state management library (e.g., Zustand, Redux Toolkit) if complexity grows.
5.  **Session Management (Client-Side):**
    *   The backend manages sessions using Supabase. The frontend might need to store and send a `session_id` (e.g., in local storage or a React Context) if the backend expects it for subsequent requests to maintain conversation context. This needs clarification with the backend team.
    *   The `SupabaseSessionStore` on the backend supports `get(session_id)`, `append_message(session_id, message)`, `clear(session_id)`, and `delete_session(session_id)`. The frontend might trigger actions (e.g., a 'clear chat' button) that map to these, requiring API calls to backend endpoints that expose this functionality if needed.
6.  **Displaying Multimodal Content:**
    *   If the backend processes images/documents and returns information derived from them (e.g., image previews, extracted text), the frontend should render this appropriately within the chat interface.
7.  **Error Handling and User Feedback (React):**
    *   Display errors returned by the backend in a user-friendly way (e.g., toast notifications, inline messages).
    *   Provide loading indicators (e.g., spinners) during API calls to give feedback to the user.
8.  **Configuration (Vite Environment Variables):**
    *   The frontend will need to know the backend API base URL. This should be managed using Vite's environment variables (e.g., `VITE_API_BASE_URL` in a `.env` file).

---

## 5. Key Considerations for Frontend

- **Development Environment (Vite):**
    *   Utilize Vite's fast development server and Hot Module Replacement (HMR) for an efficient development experience.
    *   Understand Vite's build process for production deployment (`npm run build`).
- **TypeScript:**
    *   Leverage TypeScript for static typing to catch errors early and improve code maintainability.
    *   Define clear types/interfaces for props, state, and API payloads.
- **Tailwind CSS:**
    *   Manage Tailwind CSS configuration in `tailwind.config.js`.
    *   Be mindful of purging unused styles in production builds for optimal performance.
- **CORS:** The backend is currently configured to allow all origins (`*`). This is convenient for development. For production, this should be restricted to the frontend's domain.
- **Authentication/Authorization:** The current plan does not detail specific user authentication mechanisms beyond session management. If user-specific data or access control is required, this will need further discussion and implementation on both backend and frontend.
- **Rate Limiting:** The backend has a rate-limiting stub. If this becomes active, the frontend should be prepared to handle `429 Too Many Requests` errors gracefully (e.g., by informing the user and suggesting they try again later).
- **Data Schemas (TypeScript):** Closely follow the expected request and response schemas for the `/chat` endpoint. Define corresponding TypeScript interfaces to ensure type safety. Any deviations might lead to errors.
- **Component Reusability (React):** Design React components to be reusable and maintainable.

---

This guide should help the frontend team get started with integrating with the Legal AI Chatbot backend. Please refer to the backend team for any clarifications or further details.