from __future__ import annotations

import os
from contextlib import asynccontextmanager
from uuid import UUID

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from client.item.item_thread_api_client.client import Client as ItemClient
from client.transaction.transaction_api_client.client import Client as TransactionClient
from client.user.user_address_api_client.client import Client as UserClient
from models.dto.item_user_dto import CreateOwnItemReq, UpdateOwnItemReq
from models.dto.user_dto import SignedInUserRes, SignInReq, SignInRes
from utils.db_connection import SessionDep, create_db_and_tables, close_db_connection

# Table Models
from models.po.item_user_po import ItemUser

# -----------------------------------------------------------------------------
# Environments and Clients
# -----------------------------------------------------------------------------
load_dotenv()

port = int(os.environ.get("FASTAPIPORT", 8000))

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
# Auth Utilities
# -----------------------------------------------------------------------------

async def get_user_by_token(request: Request):
    pass


# -----------------------------------------------------------------------------
# Auth Endpoints
# -----------------------------------------------------------------------------
@app.post("/auth/login", response_model=SignInRes)
async def sign_in(payload: SignInReq):
    pass


@app.get("/auth/me", response_model=SignedInUserRes)
async def auth_me(request: Request):
    pass


# -----------------------------------------------------------------------------
# Item User Endpoints
# -----------------------------------------------------------------------------
@app.post("/me/items")
async def create_item_for_me(payload: CreateOwnItemReq, request: Request, session: SessionDep):
    pass


@app.get("/me/items")
async def list_my_items(request: Request, session: SessionDep, skip: int = 0, limit: int = 10):
    pass


@app.patch("/me/items/{item_id}")
async def update_my_item(item_id: UUID, payload: UpdateOwnItemReq, request: Request, session: SessionDep):
    pass


@app.delete("/me/items/{item_id}")
async def delete_my_item(item_id: UUID, request: Request, session: SessionDep):
    pass


# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
