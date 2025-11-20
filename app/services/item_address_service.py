from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.item_address_repository import (
    create_item_address_relation,
    get_item_address,
    get_address_items,
    delete_item_address_relation
)
from app.utils.http_client import call_service

USER_SERVICE_URL = "https://users-api-121084561869.us-central1.run.app"

async def create_relation_with_check(session: AsyncSession, item_id: str, address_id: str):
    await call_service("GET", f"{USER_SERVICE_URL}/addresses/{address_id}")
    return await create_item_address_relation(session, item_id, address_id)

async def list_items_at_address(session: AsyncSession, address_id: str):
    item_ids = await get_address_items(session, address_id)
    return [{"item_id": iid} for iid in item_ids]

async def get_item_address_info(session: AsyncSession, item_id: str):
    address_id = await get_item_address(session, item_id)
    return await call_service("GET", f"{USER_SERVICE_URL}/addresses/{address_id}")

async def delete_relation_service(session: AsyncSession, item_id: str, address_id: str):
    return await delete_item_address_relation(session, item_id, address_id)