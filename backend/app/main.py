import logging
import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from .routes import chat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Legal AI Chatbot Backend",
    description="Backend services for the Legal AI Chatbot",
    version="0.1.0"
)

# Middleware
# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# 2. Logging Middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Request: {request.method} {request.url.path} - Completed in {process_time:.4f}s - Status: {response.status_code}"
        )
        return response

app.add_middleware(LoggingMiddleware)

# 3. Error Handling Middleware
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail} for {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc} for {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

# 4. Rate Limiting Stub Middleware (Placeholder)
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Placeholder for actual rate limiting logic
        # e.g., using a token bucket algorithm with Redis or an in-memory store
        # For now, it just logs a message and proceeds
        logger.debug(f"Rate limit check for: {request.client.host}")
        response = await call_next(request)
        return response

app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(chat.router)

# Example root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Legal AI Chatbot Backend"}

# To run the app (example, typically done via uvicorn command):
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
