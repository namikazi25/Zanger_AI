import pytest
from backend.app.models.gemini import GeminiFlash, BaseModelWrapper

@pytest.mark.asyncio
async def test_gemini_flash_instantiation_with_key():
    model = GeminiFlash(api_key="test_key")
    assert isinstance(model, GeminiFlash)
    assert isinstance(model, BaseModelWrapper) # Check inheritance
    assert model.api_key == "test_key"

@pytest.mark.asyncio
async def test_gemini_flash_instantiation_without_key():
    model = GeminiFlash()
    assert isinstance(model, GeminiFlash)
    assert model.api_key is None

@pytest.mark.asyncio
async def test_gemini_flash_generate():
    model = GeminiFlash(api_key="test_key")
    prompt = "Test prompt for Gemini"
    response = await model.generate(prompt)
    assert response == f"Response from GeminiFlash for: {prompt}"

@pytest.mark.asyncio
async def test_gemini_flash_generate_with_kwargs():
    model = GeminiFlash(api_key="test_key")
    prompt = "Test prompt with kwargs"
    response = await model.generate(prompt, temperature=0.5, max_tokens=100)
    # Current stub doesn't use kwargs, but test ensures it doesn't break
    assert response == f"Response from GeminiFlash for: {prompt}"