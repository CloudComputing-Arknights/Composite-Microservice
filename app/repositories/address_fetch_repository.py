import httpx

USER_SERVICE_URL = "https://users-api-121084561869.us-central1.run.app"

async def fetch_address_detail(address_id: str):
    """
    Call the User Service to retrieve full address details by address_id.
    """
    async with httpx.AsyncClient(base_url=USER_SERVICE_URL) as client:
        resp = await client.get(f"/addresses/{address_id}")
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()