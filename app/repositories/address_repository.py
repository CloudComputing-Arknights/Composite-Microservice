import httpx
from app.schemas.address import AddressCreate, AddressUpdate

ADDRESS_SERVICE_URL = "https://your-address-service-url"


async def get_all_addresses(skip: int = 0, limit: int = 20):
    async with httpx.AsyncClient(base_url=ADDRESS_SERVICE_URL) as client:
        response = await client.get("/addresses", params={"skip": skip, "limit": limit})
        response.raise_for_status()
        return response.json()


async def get_address_by_id(address_id: str):
    async with httpx.AsyncClient(base_url=ADDRESS_SERVICE_URL) as client:
        response = await client.get(f"/addresses/{address_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


async def create_address(address_data: AddressCreate):
    async with httpx.AsyncClient(base_url=ADDRESS_SERVICE_URL) as client:
        response = await client.post("/addresses", json=address_data.dict())
        response.raise_for_status()
        return response.json()


async def update_address(address_id: str, address_data: AddressUpdate):
    async with httpx.AsyncClient(base_url=ADDRESS_SERVICE_URL) as client:
        response = await client.patch(f"/addresses/{address_id}", json=address_data.dict())
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


async def delete_address(address_id: str):
    async with httpx.AsyncClient(base_url=ADDRESS_SERVICE_URL) as client:
        response = await client.delete(f"/addresses/{address_id}")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True