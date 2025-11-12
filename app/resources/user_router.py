from fastapi import APIRouter, Request

from app.models.dto.user_dto import SignedInUserRes
from app.utils.auth import get_user_id_from_token

user_router = APIRouter()


@user_router.get("/me/user", response_model=SignedInUserRes)
async def auth_me(request: Request):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass
