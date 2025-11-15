import httpx
from typing import Any, Optional

async def call_service(method: str, url: str, **kwargs) -> Any:
   
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()