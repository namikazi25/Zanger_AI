import pytest
from backend.app.models.gpt4o import GPT4O
from backend.app.models.gemini import BaseModelWrapper # Assuming BaseModelWrapper is in gemini.py or a common base

@pytest.mark.asyncio
async def test_gpt4o_instantiation_with_key():
    model = GPT4O(api_key="test_openai_key")
    assert isinstance(model, GPT4O)
    assert isinstance(model, BaseModelWrapper) # Check inheritance
    assert model.api_key == "test_openai_key"

@pytest.mark.asyncio
async def test_gpt4o_instantiation_without_key():
    model = GPT4O()
    assert isinstance(model, GPT4O)
    assert model.api_key is None

@pytest.mark.asyncio
async def test_gpt4o_generate():
    model = GPT4O(api_key="test_openai_key")
    prompt = "Test prompt for GPT-4o"
    response = await model.generate(prompt)
    assert response == f"Response from GPT4O for: {prompt}"

@pytest.mark.asyncio
async def test_gpt4o_generate_with_kwargs():
    model = GPT4O(api_key="test_openai_key")
    prompt = "Test prompt with kwargs for GPT-4o"
    response = await model.generate(prompt, temperature=0.7, max_tokens=150)
    # Current stub doesn't use kwargs, but test ensures it doesn't break
    assert response == f"Response from GPT4O for: {prompt}"