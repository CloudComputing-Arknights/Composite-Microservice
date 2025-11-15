from app.repositories.address_repository import (
    get_all_addresses,
    get_address_by_id,
    create_address,
    update_address,
    delete_address
)

async def get_all_addresses(skip: int = 0, limit: int = 20):
    return await get_all_addresses(skip=skip, limit=limit)

async def get_address_by_id(address_id: str):
    return await get_address_by_id(address_id)

async def create_address(payload):
    return await create_address(payload)

async def update_address(address_id: str, payload):
    return await update_address(address_id, payload)

async def delete_address(address_id: str):
    return await delete_address(address_id)