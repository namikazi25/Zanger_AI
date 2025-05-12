from typing import Optional, Any
import os

from .gemini import GeminiFlash, BaseModelWrapper
from .gpt4o import GPT4O

# Placeholder for session_state typing if you have a specific class
# from ..storage.session_store import SessionData # Example import
SessionStateType = Any # Replace with actual SessionData type if available

def get_model(session_state: Optional[SessionStateType] = None, policy: Optional[str] = None) -> BaseModelWrapper:
    """
    Returns a LangChain-wrapped model instance based on the routing policy.

    Args:
        session_state: The current session state (can be used for more advanced routing).
        policy: The routing policy to use. Defaults to DEFAULT_MODEL_ROUTING_POLICY.
                Supported policies:
                - "flash_first": Try GeminiFlash, fallback to GPT4O.
                - "gpt4o_only": Always use GPT4O.
                - "gemini_only": Always use GeminiFlash.
                - "balanced" (default): Currently maps to "flash_first".

    Returns:
        An instance of a BaseModelWrapper (GeminiFlash or GPT4O).

    Raises:
        ValueError: If an unsupported policy is provided or if required API keys are missing.
    """
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL_ROUTING_POLICY = os.getenv("DEFAULT_MODEL_ROUTING_POLICY", "balanced")
    current_policy = policy or DEFAULT_MODEL_ROUTING_POLICY

    # print(f"Routing with policy: {current_policy}") # Optional: for debugging

    if current_policy == "flash_first" or current_policy == "balanced":
        if GEMINI_API_KEY:
            # print("Attempting to use GeminiFlash...") # Optional: for debugging
            return GeminiFlash(api_key=GEMINI_API_KEY)
        elif OPENAI_API_KEY:
            # print("Falling back to GPT4O as Gemini API key is missing...") # Optional: for debugging
            return GPT4O(api_key=OPENAI_API_KEY)
        else:
            raise ValueError("Policy 'flash_first'/'balanced' requires GEMINI_API_KEY or OPENAI_API_KEY to be set.")

    elif current_policy == "gpt4o_only":
        if not OPENAI_API_KEY:
            raise ValueError("Policy 'gpt4o_only' requires OPENAI_API_KEY to be set.")
        # print("Using GPT4O as per policy...") # Optional: for debugging
        return GPT4O(api_key=OPENAI_API_KEY)

    elif current_policy == "gemini_only":
        if not GEMINI_API_KEY:
            raise ValueError("Policy 'gemini_only' requires GEMINI_API_KEY to be set.")
        # print("Using GeminiFlash as per policy...") # Optional: for debugging
        return GeminiFlash(api_key=GEMINI_API_KEY)

    else:
        raise ValueError(f"Unsupported model routing policy: {current_policy}")

# Example usage (optional, for local testing purposes)
# async def main():
#     # Ensure you have a .env file with API keys set
#     # from dotenv import load_dotenv
#     # load_dotenv() # Load environment variables from .env

    # print(f"GEMINI_API_KEY set: {'Yes' if GEMINI_API_KEY else 'No'}")
    # print(f"OPENAI_API_KEY set: {'Yes' if OPENAI_API_KEY else 'No'}")
    # print(f"DEFAULT_MODEL_ROUTING_POLICY: {DEFAULT_MODEL_ROUTING_POLICY}")

    # policies_to_test = ["flash_first", "gpt4o_only", "gemini_only", "balanced", "invalid_policy"]
    # for p in policies_to_test:
    #     print(f"\n--- Testing policy: {p} ---")
    #     try:
    #         model_instance = get_model(policy=p)
    #         response = await model_instance.generate(f"Hello from policy {p}!")
    #         print(f"Model: {model_instance.__class__.__name__}, Response: {response}")
    #     except ValueError as e:
    #         print(f"Error: {e}")
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
#
# if __name__ == "__main__":
#     import asyncio
#     # You might need to load .env here if running this file directly
#     # from dotenv import load_dotenv
#     # load_dotenv()
#     asyncio.run(main())