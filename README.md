# ZangerAI

ZangerAI is a conversational AI application with a FastAPI backend. The project is structured with separate backend and frontend components.

## Project Structure

```
ZangerAI/
├── README.md
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   └── routes/
│   │       └── chat.py
│   └── .env
└── frontend/
```

## Backend

The backend is a FastAPI application that provides a chat endpoint for processing messages through an AI agent.

### Features

- Langchain endpoint for chat functionality
- Session management for conversations
- FastAPI for high-performance API handling

### Dependencies

The backend requires Python 3.8+ and includes the following key dependencies:
- FastAPI - High-performance web framework
- Uvicorn - ASGI server for FastAPI
- LangChain - Framework for working with language models
- OpenAI - API client for OpenAI's models
- Pydantic - Data validation library

### Prerequisites

Before running the backend, ensure you have:
- Python 3.8 or higher installed
- pip package manager
- Virtual environment setup (recommended)

### Setup Instructions

1. Clone the repository
   ```
   git clone https://github.com/yourusername/ZangerAI.git
   cd ZangerAI
   ```

2. Create and activate a virtual environment (optional but recommended)
   ```
   # Windows
   python -m venv backend/venv
   backend/venv/Scripts/activate

   # macOS/Linux
   python3 -m venv backend/venv
   source backend/venv/bin/activate
   ```

3. Install required dependencies
   ```
   cd backend
   pip install -r requirements.txt
   ```

4. Environment Configuration

   Create or update the `.env` file in the backend directory with necessary API keys and configuration:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run the backend server
   ```
   cd backend
   uvicorn app.main:app --reload
   ```

   The server will start at `http://127.0.0.1:8000`

### API Endpoints

- **POST /chat**
  - Accepts a JSON body with `message` and `session_id` fields
  - Returns AI-generated responses

### Development Notes

- The agent implementation needs to be completed in `app/agents/my_agent.py`
- Environment variables should be properly configured in the `.env` file for API keys

## Future Work

- Complete the agent implementation
- Add authentication and user management
- Develop the frontend interface
- Improve error handling and response validation