from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware
import pytest
import logging
import time

# --- Mock Application Setup ---

# Basic app for testing middleware
app_for_middleware_tests = FastAPI()

# Dummy endpoint
@app_for_middleware_tests.get("/test-middleware")
async def read_test_middleware():
    return {"message": "Middleware test endpoint"}

@app_for_middleware_tests.get("/error-endpoint")
async def error_endpoint():
    raise HTTPException(status_code=500, detail="Intentional server error")

# --- Logging Middleware (Example) ---
# In a real app, this would be more sophisticated and likely part of a larger setup
async def logging_middleware(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

# --- Error Handling Middleware (Example) ---
async def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "path": str(request.url.path)}
    )

# --- Rate Limiting Stub Middleware (Example) ---
# This is a very basic stub. Real rate limiting is more complex.
RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 10 # Per 10 seconds
request_counts = {}

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in request_counts:
        request_counts[client_ip] = []

    # Filter out old requests
    request_counts[client_ip] = [t for t in request_counts[client_ip] if current_time - t < RATE_LIMIT_WINDOW_SECONDS]

    if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    request_counts[client_ip].append(current_time)
    response = await call_next(request)
    return response

# Apply middleware to the test app
# Note: In a real application, these would be added in main.py or a similar setup file.
app_for_middleware_tests.middleware("http")(logging_middleware)
app_for_middleware_tests.add_exception_handler(HTTPException, http_error_handler)
app_for_middleware_tests.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app_for_middleware_tests.middleware("http")(rate_limit_middleware) # Add this if you want to test it directly here

client_middleware = TestClient(app_for_middleware_tests)

# --- Test Cases ---

def test_logging_middleware(caplog):
    """Test that the logging middleware logs request and response info."""
    with caplog.at_level(logging.INFO):
        response = client_middleware.get("/test-middleware")
    assert response.status_code == 200
    assert "Request: GET /test-middleware" in caplog.text
    assert "Response status: 200" in caplog.text

def test_error_handling_middleware():
    """Test that the error handling middleware catches HTTPExceptions and returns a JSON response."""
    response = client_middleware.get("/error-endpoint")
    assert response.status_code == 500
    assert response.json() == {"error": "Intentional server error", "path": "/error-endpoint"}

def test_cors_middleware_allows_all_origins():
    """Test that CORS middleware is configured to allow all origins (for this test setup)."""
    response = client_middleware.options(
        "/test-middleware",
        headers={
            "Origin": "http://example.com",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://example.com"
    assert "GET" in response.headers["access-control-allow-methods"]

# --- Rate Limiting Test (More involved, might be in its own app or mocked differently) ---
# For simplicity, we'll create a separate app instance to test rate limiting in isolation
# to avoid interference from other middleware or complex state.

app_for_rate_limit_test = FastAPI()

@app_for_rate_limit_test.get("/rate-limited-resource")
async def rate_limited_resource():
    return {"message": "You got the resource!"}

# Reset request_counts for this specific test environment
rate_limit_test_request_counts = {}

async def specific_rate_limit_middleware(request: Request, call_next):
    # Use a separate counter for this test to avoid state leakage
    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in rate_limit_test_request_counts:
        rate_limit_test_request_counts[client_ip] = []

    rate_limit_test_request_counts[client_ip] = [t for t in rate_limit_test_request_counts[client_ip] if current_time - t < RATE_LIMIT_WINDOW_SECONDS]

    if len(rate_limit_test_request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        # Return a standard JSON response for 429, as TestClient expects it
        return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

    rate_limit_test_request_counts[client_ip].append(current_time)
    response = await call_next(request)
    return response

app_for_rate_limit_test.middleware("http")(specific_rate_limit_middleware)
client_rate_limit = TestClient(app_for_rate_limit_test)

@pytest.mark.parametrize("run", range(RATE_LIMIT_REQUESTS + 2))
def test_rate_limit_middleware_stub(run):
    """Test the rate limiting stub middleware."""
    # Reset for each parameter run to ensure clean state for this specific test
    if run == 0:
        rate_limit_test_request_counts.clear() # Clear at the beginning of the parametrized test runs

    response = client_rate_limit.get("/rate-limited-resource")

    if run < RATE_LIMIT_REQUESTS:
        assert response.status_code == 200
        assert response.json() == {"message": "You got the resource!"}
    else:
        assert response.status_code == 429
        assert response.json() == {"detail": "Too Many Requests"}

# Note: Real-world middleware testing might involve:
# - More complex app setups.
# - Mocking external services (e.g., Redis for distributed rate limiting).
# - Testing middleware order and interactions.
# - More granular checks on headers, response bodies, and side effects.