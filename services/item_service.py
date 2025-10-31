import httpx
from fastapi import HTTPException

ITEM_SERVICE_URL = "https://microservice-item-713181822049.us-central1.run.app"

async def list_items() -> list[dict]:
    """
    Fetches all items from the Item service.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ITEM_SERVICE_URL}/items/")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Item Service: {e.response.text}",
            )

async def get_item_by_id(item_id: str) -> dict:
    """
    Fetches a single item by its UUID from the Item service.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ITEM_SERVICE_URL}/items/{item_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Item Service: {e.response.text}",
            )