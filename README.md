# ZangerAI

ZangerAI is a proprietary conversational AI application built on a FastAPI backend, designed for internal use. The project is structured with separate backend and frontend components.

## Project Structure

```
ZangerAI/
├── README.md          # This overview file
├── backend/           # FastAPI service
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   └── routes/
│   │       └── chat.py
│   └── .env           # Internal environment configuration
└── frontend/          # React/TailwindUI client
```

## Backend

The backend is a FastAPI application exposing a `/chat` endpoint for session-based AI conversations, now featuring secure, encrypted session and state management using Supabase as the backing store.

### Features

- LangChain-driven agent for chat
- Supabase-backed session and state management
- End-to-end encryption of session data using Fernet (cryptography)
- FastAPI + Uvicorn for high-performance serving
- Secure environment variable management with python-dotenv

### Dependencies

- Python 3.8+
- FastAPI
- Uvicorn
- LangChain
- OpenAI Python SDK
- Pydantic
- supabase-py
- cryptography
- python-dotenv

### Prerequisites

- Access to the internal Git repository
- Environment variables configured in `backend/.env` (see below)
- Supabase project set up with a `sessions` table (see architecture plan for schema)

### Environment Variables

Add the following to your `backend/.env`:
```env
OPENAI_API_KEY=your_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_API_KEY=your-service-role-key
FERNET_KEY=your-generated-key
```
- Generate a Fernet key with:
  ```bash
  python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  ```
- Never commit secrets to version control.

### Setup Instructions

1. **Obtain access**: Request repository permissions from your engineering lead.
2. **Clone the internal repo**:
   ```bash
   git clone <internal-git-url>
   cd ZangerAI
   ```
3. **Create and activate** a Python virtual environment:
   ```bash
   python3 -m venv backend/venv
   source backend/venv/bin/activate
   ```
4. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
5. **Configure environment**: Populate `backend/.env` as described above.
6. **Set up Supabase**: Ensure your Supabase project has a `sessions` table matching the backend's requirements. See `BACKEND_ARCHITECTURE_PLAN.md` for schema and setup tips.
7. **Run the server**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

### API Endpoints

- **POST /chat**
  - Request body: `{ "message": "<text>", "session_id": "<id>" }`
  - Response: `{ "response": "<AI reply>" }`

## Frontend

The frontend is implemented in React + TypeScript with Vite and TailwindCSS. It connects to the backend `/chat` API to drive the conversational UI.

### Getting Started

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```
2. **Start the development server**:
   ```bash
   npm run dev
   ```
3. **Open** `http://localhost:5173` in your browser.

## Development Notes

- Agent logic is implemented in `backend/app/agents/my_agent.py` — this is the primary customization point.
- Ensure all environment variables and secret management follow internal security guidelines.

## Future Work

- Complete agent orchestration and business-logic integration
- Add authentication, user roles, and audit logging
- Enhance error handling, validations, and observability
- Extend frontend UX with advanced controls and state persistence

