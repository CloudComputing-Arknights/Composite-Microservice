from fastapi import APIRouter, HTTPException

from app.client.user.user_address_api_client.api.default.login_auth_token_post import asyncio as user_login_async
from app.client.user.user_address_api_client.models.body_login_auth_token_post import BodyLoginAuthTokenPost
from app.client.user.user_address_api_client.models.http_validation_error import HTTPValidationError
from app.client.user.user_address_api_client.models.token import Token
from app.client.user.user_address_api_client.types import UNSET
from app.models.dto.user_dto import SignInRes, SignInReq
from app.utils.config import get_user_client

public_router = APIRouter()


@public_router.get("/")
async def root():
    return {"message": "Welcome to the Composite API. See /docs for details."}


@public_router.post("/token", response_model=SignInRes)
async def sign_in(payload: SignInReq):
    body = BodyLoginAuthTokenPost(username=payload.username, password=payload.password)

    result = await user_login_async(client=get_user_client(), body=body)

    if result is None:
        raise HTTPException(status_code=500)

    if isinstance(result, HTTPValidationError):
        raise HTTPException(status_code=401)

    token: Token = result
    token_type = token.token_type if token.token_type is not UNSET else "bearer"

    return SignInRes(access_token=token.access_token, token_type=token_type)
