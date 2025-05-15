from abc import ABC, abstractmethod
import httpx
import os

class BaseModelWrapper(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass

class GeminiFlash(BaseModelWrapper):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for GeminiFlash.")

    async def generate(self, prompt: str, **kwargs) -> str:
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, headers=headers, params=params, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            try:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            except Exception:
                return str(result)

# Example usage (optional, for local testing purposes)
# async def main():
#     # Ensure you have a .env file or set the API key directly
#     # from dotenv import load_dotenv
#     # import os
#     # load_dotenv()
#     # gemini_api_key = os.getenv("GEMINI_API_KEY")
#     gemini_model = GeminiFlash(api_key="YOUR_GEMINI_API_KEY_OR_NONE")
#     response = await gemini_model.generate("Hello, Gemini!")
#     print(response)
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())