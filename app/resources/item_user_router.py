from fastapi import APIRouter
from typing import List
from app.utils.db_connection import SessionDep
from app.models.po.item_user_po import ItemUser
from app.services.item_user_service import (
    create_relation_with_check,
    list_user_items_with_details,
    get_item_owner_info,
    delete_relation_service
)

item_user_router = APIRouter(prefix="/item-user", tags=["Item-User"])

@item_user_router.post("/{item_id}/{user_id}")
async def create_relation(item_id: str, user_id: str, session: SessionDep) -> ItemUser:
    return await create_relation_with_check(session, item_id, user_id)

@item_user_router.get("/user/{user_id}")
async def list_user_items(user_id: str, session: SessionDep) -> List[dict]:
    return await list_user_items_with_details(session, user_id)

@item_user_router.get("/item/{item_id}")
async def get_owner(item_id: str, session: SessionDep) -> dict:
    return await get_item_owner_info(session, item_id)

@item_user_router.delete("/{item_id}")
async def delete_relation(item_id: str, session: SessionDep):
    await delete_relation_service(session, item_id)
    return {"detail": "Relation deleted successfully"}