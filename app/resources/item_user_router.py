from fastapi import APIRouter, Request

from app.models.dto.item_user_dto import CreateOwnItemReq, UpdateOwnItemReq
from app.models.dto.user_dto import SignedInUserRes
from app.utils.auth import get_user_id_from_token
from app.utils.db_connection import SessionDep

item_user_router = APIRouter()


@item_user_router.post("/me/items")
async def create_item_for_me(payload: CreateOwnItemReq, request: Request, session: SessionDep):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass


@item_user_router.get("/me/items")
async def list_my_items(request: Request, session: SessionDep, skip: int = 0, limit: int = 10):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass


@item_user_router.patch("/me/items/{item_id}")
async def update_my_item(item_id: str, payload: UpdateOwnItemReq, request: Request, session: SessionDep):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass


@item_user_router.delete("/me/items/{item_id}")
async def delete_my_item(item_id: str, request: Request, session: SessionDep):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass
