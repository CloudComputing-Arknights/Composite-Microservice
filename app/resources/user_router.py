from fastapi import APIRouter, Request, HTTPException

from app.client.user.user_address_api_client.api.default.login_auth_token_post import asyncio as user_login_async
from app.client.user.user_address_api_client.models.body_login_auth_token_post import BodyLoginAuthTokenPost
from app.client.user.user_address_api_client.models.http_validation_error import HTTPValidationError
from app.client.user.user_address_api_client.models.token import Token
from app.client.user.user_address_api_client.types import UNSET
from app.models.dto.user_dto import SignInRes, SignInReq
from app.models.dto.user_dto import SignedInUserRes
from app.utils.auth import get_user_id_from_token
from app.utils.config import get_user_client

USER_SERVICE_URL = "https://users-api-121084561869.us-central1.run.app"

user_router = APIRouter()

@user_router.post("/token", response_model=SignInRes)
async def sign_in(payload: SignInReq):
    body = BodyLoginAuthTokenPost(username=payload.username, password=payload.password)

    result = await user_login_async(client=get_user_client(), body=body)

    if result is None:
        raise HTTPException(status_code=500, detail="User service is unavailable")

    if isinstance(result, HTTPValidationError):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token: Token = result
    token_type = token.token_type if token.token_type is not UNSET else "bearer"

    return SignInRes(access_token=token.access_token, token_type=token_type)

@user_router.get("/me/user", response_model=SignedInUserRes)
async def auth_me(request: Request):
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    user_id = get_user_id_from_token(authorization_header)
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Failed to fetch user info")
    
    return SignedInUserRes(**resp.json())