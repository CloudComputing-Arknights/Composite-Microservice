from fastapi import APIRouter
from typing import List
from app.utils.db_connection import SessionDep
from app.models.po.address_user_po import AddressUser
from app.services.address_user_service import (
    create_relation_with_check,
    list_user_addresses,
    get_owner_info,
    delete_relation_service
)

address_user_router = APIRouter(prefix="/address-user", tags=["Address-User"])

@address_user_router.post("/{address_id}/{user_id}")
async def create_relation(address_id: str, user_id: str, session: SessionDep) -> AddressUser:
    return await create_relation_with_check(session, address_id, user_id)

@address_user_router.get("/user/{user_id}")
async def list_addresses(user_id: str, session: SessionDep) -> List[str]:
    return await list_user_addresses(session, user_id)

@address_user_router.get("/address/{address_id}")
async def get_owner(address_id: str, session: SessionDep) -> dict:
    return await get_owner_info(session, address_id)

@address_user_router.delete("/{address_id}")
async def delete_relation(address_id: str, session: SessionDep):
    await delete_relation_service(session, address_id)
    return {"detail": "Relation deleted successfully"}