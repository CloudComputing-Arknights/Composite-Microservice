from app.repositories.item_user_repository import (
    create_item_user_relation,
    get_user_items,
    get_item_owner,
    delete_item_user_relation,
    verify_item_ownership
)
from app.utils.http_client import call_service

USER_SERVICE_URL = "https://users-api-121084561869.us-central1.run.app"
ITEM_SERVICE_URL = "https://microservice-item-848539791549.us-central1.run.app"

async def create_relation_with_check(session, item_id: str, user_id: str):
    await call_service("GET", f"{USER_SERVICE_URL}/users/{user_id}")
    await call_service("GET", f"{ITEM_SERVICE_URL}/items/{item_id}")
    return await create_item_user_relation(session, item_id, user_id)

async def list_user_items_with_details(session, user_id: str):
    item_ids = await get_user_items(session, user_id)
    return [await call_service("GET", f"{ITEM_SERVICE_URL}/items/{iid}") for iid in item_ids]

async def get_item_owner_info(session, item_id: str):
    owner_id = await get_item_owner(session, item_id)
    return await call_service("GET", f"{USER_SERVICE_URL}/users/{owner_id}")

async def delete_relation_service(session, item_id: str):
    return await delete_item_user_relation(session, item_id)

async def verify_item_ownership_service(session, item_id: str, user_id: str) -> bool:
    return await verify_item_ownership(session, item_id, user_id)