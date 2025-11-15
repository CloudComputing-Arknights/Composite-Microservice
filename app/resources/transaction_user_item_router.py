from fastapi import APIRouter
from typing import Optional
from app.utils.db_connection import SessionDep
from app.models.po.transaction_user_item_po import Role
from app.services.transaction_user_item_service import (
    create_relation_with_check,
    list_relations_service,
    delete_relation_service
)

transaction_user_item_router = APIRouter(prefix="/transaction-user-item", tags=["Transaction-User-Item"])

@transaction_user_item_router.post("/{transaction_id}/{user_id}")
async def create_relation(
    transaction_id: str,
    user_id: str,
    role: Role,
    session: SessionDep,
    item_id: Optional[str] = None,
):
    return await create_relation_with_check(session, transaction_id, user_id, role, item_id)

@transaction_user_item_router.get("/")
async def list_relations(
    session: SessionDep,
    transaction_id: Optional[str] = None,
    user_id: Optional[str] = None,
    item_id: Optional[str] = None,
):
    return await list_relations_service(session, transaction_id, user_id, item_id)

@transaction_user_item_router.delete("/{transaction_id}/{user_id}")
async def delete_relation(
    transaction_id: str,
    user_id: str,
    role: Role,
    session: SessionDep,
    item_id: Optional[str] = None,
):
    return await delete_relation_service(session, transaction_id, user_id, role, item_id)