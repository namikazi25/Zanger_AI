from .gemini import BaseModelWrapper # Assuming BaseModelWrapper is in gemini.py
import httpx
import os

class GPT4O(BaseModelWrapper):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for GPT4O.")

    async def generate(self, prompt: str, **kwargs) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 1024),
            "temperature": kwargs.get("temperature", 0.7)
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            try:
                return result["choices"][0]["message"]["content"]
            except Exception:
                return str(result)