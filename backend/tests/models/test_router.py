import pytest
import os
from unittest.mock import patch

from backend.app.models.router import get_model
from backend.app.models.gemini import GeminiFlash
from backend.app.models.gpt4o import GPT4O

# Store original environment variables
ORIGINAL_GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
ORIGINAL_OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
ORIGINAL_DEFAULT_POLICY = os.environ.get("DEFAULT_MODEL_ROUTING_POLICY")

@pytest.fixture(autouse=True)
def manage_env_vars():
    """Fixture to manage environment variables for each test."""
    # Set to None initially for controlled testing
    if "GEMINI_API_KEY" in os.environ: del os.environ["GEMINI_API_KEY"]
    if "OPENAI_API_KEY" in os.environ: del os.environ["OPENAI_API_KEY"]
    if "DEFAULT_MODEL_ROUTING_POLICY" in os.environ: del os.environ["DEFAULT_MODEL_ROUTING_POLICY"]
    
    # Reload modules to pick up changed env vars for constants like GEMINI_API_KEY
    # This is a bit heavy-handed but ensures constants in router.py are re-evaluated
    import sys
    if 'backend.app.models.router' in sys.modules:
        del sys.modules['backend.app.models.router']
    from backend.app.models import router
    global get_model # Make it available globally in this test module
    get_model = router.get_model

    yield

    # Restore original environment variables
    if ORIGINAL_GEMINI_KEY is not None: os.environ["GEMINI_API_KEY"] = ORIGINAL_GEMINI_KEY
    elif "GEMINI_API_KEY" in os.environ: del os.environ["GEMINI_API_KEY"]
    if ORIGINAL_OPENAI_KEY is not None: os.environ["OPENAI_API_KEY"] = ORIGINAL_OPENAI_KEY
    elif "OPENAI_API_KEY" in os.environ: del os.environ["OPENAI_API_KEY"]
    if ORIGINAL_DEFAULT_POLICY is not None: os.environ["DEFAULT_MODEL_ROUTING_POLICY"] = ORIGINAL_DEFAULT_POLICY
    elif "DEFAULT_MODEL_ROUTING_POLICY" in os.environ: del os.environ["DEFAULT_MODEL_ROUTING_POLICY"]
    
    # Reload again to restore original state for other tests if any
    if 'backend.app.models.router' in sys.modules:
        del sys.modules['backend.app.models.router']


@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key"})
def test_get_model_flash_first_with_gemini_key():
    model = get_model(policy="flash_first")
    assert isinstance(model, GeminiFlash)
    assert model.api_key == "test_gemini_key"

@patch.dict(os.environ, {"OPENAI_API_KEY": "test_openai_key"})
def test_get_model_flash_first_with_openai_key_only():
    # GEMINI_API_KEY is not set by this patch, relying on fixture to clear it
    model = get_model(policy="flash_first")
    assert isinstance(model, GPT4O)
    assert model.api_key == "test_openai_key"

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key", "OPENAI_API_KEY": "test_openai_key"})
def test_get_model_flash_first_with_both_keys():
    model = get_model(policy="flash_first")
    assert isinstance(model, GeminiFlash) # Gemini should be preferred
    assert model.api_key == "test_gemini_key"

def test_get_model_flash_first_no_keys():
    with pytest.raises(ValueError, match="Policy 'flash_first'/'balanced' requires GEMINI_API_KEY or OPENAI_API_KEY to be set."):
        get_model(policy="flash_first")

@patch.dict(os.environ, {"OPENAI_API_KEY": "test_openai_key"})
def test_get_model_gpt4o_only_with_key():
    model = get_model(policy="gpt4o_only")
    assert isinstance(model, GPT4O)
    assert model.api_key == "test_openai_key"

def test_get_model_gpt4o_only_no_key():
    with pytest.raises(ValueError, match="Policy 'gpt4o_only' requires OPENAI_API_KEY to be set."):
        get_model(policy="gpt4o_only")

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key"})
def test_get_model_gemini_only_with_key():
    model = get_model(policy="gemini_only")
    assert isinstance(model, GeminiFlash)
    assert model.api_key == "test_gemini_key"

def test_get_model_gemini_only_no_key():
    with pytest.raises(ValueError, match="Policy 'gemini_only' requires GEMINI_API_KEY to be set."):
        get_model(policy="gemini_only")

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key", "DEFAULT_MODEL_ROUTING_POLICY": "gemini_only"})
def test_get_model_default_policy_gemini():
    # Need to re-import or patch the router's DEFAULT_MODEL_ROUTING_POLICY if it's read at import time
    # The fixture `manage_env_vars` handles reloading router module to pick up DEFAULT_MODEL_ROUTING_POLICY
    from backend.app.models.router import get_model as reloaded_get_model
    model = reloaded_get_model() # Uses default policy from env
    assert isinstance(model, GeminiFlash)

@patch.dict(os.environ, {"OPENAI_API_KEY": "test_openai_key", "DEFAULT_MODEL_ROUTING_POLICY": "gpt4o_only"})
def test_get_model_default_policy_gpt4o():
    from backend.app.models.router import get_model as reloaded_get_model
    model = reloaded_get_model()
    assert isinstance(model, GPT4O)

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key", "DEFAULT_MODEL_ROUTING_POLICY": "balanced"})
def test_get_model_default_policy_balanced_gemini_first():
    from backend.app.models.router import get_model as reloaded_get_model
    model = reloaded_get_model()
    assert isinstance(model, GeminiFlash)

@patch.dict(os.environ, {"OPENAI_API_KEY": "test_openai_key", "DEFAULT_MODEL_ROUTING_POLICY": "balanced"})
def test_get_model_default_policy_balanced_openai_fallback():
    # Ensure GEMINI_API_KEY is not set for this specific test case if it was set by another patch
    if "GEMINI_API_KEY" in os.environ: del os.environ["GEMINI_API_KEY"]
    # Reload router to ensure GEMINI_API_KEY is None within its scope for this test
    import sys
    if 'backend.app.models.router' in sys.modules:
        del sys.modules['backend.app.models.router']
    from backend.app.models import router
    reloaded_get_model = router.get_model

    model = reloaded_get_model()
    assert isinstance(model, GPT4O)

def test_get_model_invalid_policy():
    with pytest.raises(ValueError, match="Unsupported model routing policy: invalid_policy"):
        get_model(policy="invalid_policy")

# Test session_state argument (though not used in current router.py logic, good for future-proofing)
@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key"})
def test_get_model_with_session_state():
    mock_session_state = {"user_id": "test_user"}
    model = get_model(session_state=mock_session_state, policy="gemini_only")
    assert isinstance(model, GeminiFlash)