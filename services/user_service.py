import httpx
from fastapi import HTTPException

USER_SERVICE_URL = "https://users-api-121084561869.us-central1.run.app"

async def get_user_by_id(user_id: str) -> dict:
    """
    Fetches a single user by their UUID from the User service.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from User Service: {e.response.text}",
            )

async def get_users_by_ids(user_ids: list[str]) -> list[dict]:
    """
    Fetches multiple users by their UUIDs.
    NOTE: The user service OpenAPI doesn't support batch fetching,
    so we fetch them one by one.
    """
    unique_ids = list(set(user_ids))
    users = {}
    async with httpx.AsyncClient() as client:
        for user_id in unique_ids:
            try:
                response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
                response.raise_for_status()
                user_data = response.json()
                users[user_data['id']] = user_data
            except httpx.HTTPStatusError:
                # Handle cases where a user might not be found, continue processing others
                continue
    return users