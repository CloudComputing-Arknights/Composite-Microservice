from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.address_user_repository import (
    create_address_user_relation,
    get_user_addresses,
    get_address_owner,
    delete_address_user_relation,
)
from app.utils.http_client import call_service

USER_SERVICE_URL = "https://users-api-121084561869.us-central1.run.app"

async def create_relation_with_check(session: AsyncSession, address_id: str, user_id: str):
    # Check user existence before creating relation
    await call_service("GET", f"{USER_SERVICE_URL}/users/{user_id}")
    return await create_address_user_relation(session, address_id, user_id)

async def list_user_addresses(session: AsyncSession, user_id: str):
    # Get address IDs from Composite DB
    address_ids = await get_user_addresses(session, user_id)
    # Fetch details from User Service
    addresses = []
    for addr_id in address_ids:
        address_detail = await call_service("GET", f"{USER_SERVICE_URL}/addresses/{addr_id}")
        addresses.append(address_detail)
    return addresses

async def get_owner_info(session: AsyncSession, address_id: str):
    owner_id = await get_address_owner(session, address_id)
    return await call_service("GET", f"{USER_SERVICE_URL}/users/{owner_id}")

async def delete_relation_service(session: AsyncSession, address_id: str, user_id: str):
    return await delete_address_user_relation(session, address_id, user_id)