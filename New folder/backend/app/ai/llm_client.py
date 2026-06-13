from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel
import json

from app.config import settings

class LLMResponse(BaseModel):
    text: str

class BaseLLMClient(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> LLMResponse:
        pass

class OllamaClient(BaseLLMClient):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        
    async def generate(self, prompt: str) -> LLMResponse:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                response.raise_for_status()
                data = response.json()
                return LLMResponse(text=data.get("response", ""))
        except Exception as e:
            # Fallback or empty if LLM fails
            return LLMResponse(text="")

# Simple factory
def get_llm_client() -> BaseLLMClient:
    return OllamaClient()
