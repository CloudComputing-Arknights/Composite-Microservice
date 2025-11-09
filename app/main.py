from __future__ import annotations

import os
from contextlib import asynccontextmanager
from uuid import UUID

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi import HTTPException

from app.client.item.item_thread_api_client.client import Client as ItemClient
from app.client.transaction.transaction_api_client.client import Client as TransactionClient
from app.client.user.user_address_api_client.api.default.login_auth_token_post import asyncio as user_login_async
from app.client.user.user_address_api_client.client import Client as UserClient
from app.client.user.user_address_api_client.models.body_login_auth_token_post import BodyLoginAuthTokenPost
from app.client.user.user_address_api_client.models.http_validation_error import HTTPValidationError
from app.client.user.user_address_api_client.models.token import Token
from app.client.user.user_address_api_client.types import UNSET
from app.models.dto.item_user_dto import CreateOwnItemReq, UpdateOwnItemReq
from app.models.dto.user_dto import SignedInUserRes, SignInReq, SignInRes
from app.utils.auth import get_user_id_from_token
from app.utils.db_connection import SessionDep, create_db_and_tables, close_db_connection

# Table Models

# -----------------------------------------------------------------------------
# Environments and Clients
# -----------------------------------------------------------------------------
load_dotenv()

_user_client = UserClient(base_url=os.environ.get("USER_SERVICE_URL"))
_item_client = ItemClient(base_url=os.environ.get("ITEM_SERVICE_URL"))
_transaction_client = TransactionClient(base_url=os.environ.get("TRANSACTION_SERVICE_URL"))


# -----------------------------------------------------------------------------
# Lifespan: Database Initialization
# -----------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    print("Creating database tables...")
    await create_db_and_tables()
    print("Database tables created successfully!")

    yield

    # Shutdown: cleanup
    print("Closing database connection...")
    await close_db_connection()
    print("Shutdown complete!")


# -----------------------------------------------------------------------------
# FastAPI App Definition
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Composite API",
    description="An API to orchestrate calls to other microservices.",
    version="1.0.0",
    lifespan=lifespan,
)


# -----------------------------------------------------------------------------
# Root Endpoint
# -----------------------------------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Welcome to the Composite API. See /docs for details."}


# -----------------------------------------------------------------------------
# Public Endpoints
# -----------------------------------------------------------------------------
@app.post("/token", response_model=SignInRes)
async def sign_in(payload: SignInReq):
    body = BodyLoginAuthTokenPost(username=payload.username, password=payload.password)

    result = await user_login_async(client=_user_client, body=body)

    if result is None:
        raise HTTPException(status_code=500)

    if isinstance(result, HTTPValidationError):
        raise HTTPException(status_code=401)

    token: Token = result
    token_type = token.token_type if token.token_type is not UNSET else "bearer"

    return SignInRes(access_token=token.access_token, token_type=token_type)


# -----------------------------------------------------------------------------
# User Endpoints
# -----------------------------------------------------------------------------
@app.get("/me/user", response_model=SignedInUserRes)
async def auth_me(request: Request):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass


# -----------------------------------------------------------------------------
# Item User Endpoints
# -----------------------------------------------------------------------------
@app.post("/me/items")
async def create_item_for_me(payload: CreateOwnItemReq, request: Request, session: SessionDep):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass


@app.get("/me/items")
async def list_my_items(request: Request, session: SessionDep, skip: int = 0, limit: int = 10):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass


@app.patch("/me/items/{item_id}")
async def update_my_item(item_id: UUID, payload: UpdateOwnItemReq, request: Request, session: SessionDep):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass


@app.delete("/me/items/{item_id}")
async def delete_my_item(item_id: UUID, request: Request, session: SessionDep):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass
