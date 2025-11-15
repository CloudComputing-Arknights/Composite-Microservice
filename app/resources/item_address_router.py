from fastapi import APIRouter
from typing import List
from app.utils.db_connection import SessionDep
from app.services.item_address_service import (
    create_relation_with_check,
    list_items_at_address,
    get_item_address_info,
    delete_relation_service
)

item_address_router = APIRouter(prefix="/item-address", tags=["Item-Address"])

@item_address_router.post("/{item_id}/{address_id}")
async def create_relation(item_id: str, address_id: str, session: SessionDep):
    return await create_relation_with_check(session, item_id, address_id)

@item_address_router.get("/address/{address_id}")
async def list_items(address_id: str, session: SessionDep) -> List[dict]:
    return await list_items_at_address(session, address_id)

@item_address_router.get("/item/{item_id}")
async def get_address(item_id: str, session: SessionDep) -> dict:
    return await get_item_address_info(session, item_id)

# app/resources/item_address_router.py
@item_address_router.delete("/{item_id}/{address_id}")
async def delete_relation(item_id: str, address_id: str, session: SessionDep):
    await delete_relation_service(session, item_id, address_id)
    return {"detail": "Relation deleted successfully"}