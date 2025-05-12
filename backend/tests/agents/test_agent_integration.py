import pytest
import asyncio
from backend.app.agents.my_agent import run_agent

@pytest.mark.asyncio
async def test_agent_flow():
    query = "What is the capital of France?"
    session = {"user_id": "test_user"}
    result = await run_agent(query, session)
    assert isinstance(result, dict)
    assert "response" in result
    assert result["response"] is not None
    assert "Paris".lower() in result["response"].lower()