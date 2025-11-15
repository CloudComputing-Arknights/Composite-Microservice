from typing import Optional
from app.repositories.transaction_user_item_repository import (
    create_transaction_user_item_relation,
    get_transaction_user_item_relations,
    delete_transaction_user_item_relation
)
from app.models.po.transaction_user_item_po import Role
from app.utils.http_client import call_service

USER_SERVICE_URL = "https://users-api-121084561869.us-central1.run.app"
ITEM_SERVICE_URL = "https://microservice-item-848539791549.us-central1.run.app"
TRANSACTION_SERVICE_URL = "http://34.172.7.104:8000"

async def create_relation_with_check(
    session, transaction_id: str, user_id: str, role: Role, item_id: Optional[str] = None
):
    
    await call_service("GET", f"{TRANSACTION_SERVICE_URL}/transactions/{transaction_id}")
    await call_service("GET", f"{USER_SERVICE_URL}/users/{user_id}")
    if item_id:
        await call_service("GET", f"{ITEM_SERVICE_URL}/items/{item_id}")
    return await create_transaction_user_item_relation(session, transaction_id, user_id, role, item_id)

async def list_relations_service(session, transaction_id=None, user_id=None, item_id=None):
    return await get_transaction_user_item_relations(session, transaction_id, user_id, item_id)

async def delete_relation_service(
    session, transaction_id: str, user_id: str, role: Role, item_id: Optional[str] = None
):
    return await delete_transaction_user_item_relation(session, transaction_id, user_id, role, item_id)