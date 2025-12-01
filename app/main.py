from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.resources.address_router import address_router
from app.resources.address_user_router import address_user_router
from app.resources.item_address_router import item_address_router
from app.resources.item_router import item_router
from app.resources.item_user_router import item_user_router
from app.resources.root_router import root_router
from app.resources.transaction_router import transaction_router
from app.resources.transaction_user_item_router import transaction_user_item_router
from app.resources.user_router import user_router
from app.resources.message_router import message_router
from app.resources.message_thread_router import thread_router

from app.utils.config import init_env
from app.utils.db_connection import create_db_and_tables, close_db_connection

from fastapi.middleware.cors import CORSMiddleware
from app.middleware.auth_middleware import AuthMiddleware

# Table Models (Necessary)
from app.models.po.address_user_po import AddressUser
from app.models.po.item_address_po import ItemAddress
from app.models.po.item_user_po import ItemUser
from app.models.po.transaction_user_item_po import TransactionUserItem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------------------------------------------------------
# Environments and Clients
# -----------------------------------------------------------------------------
init_env()


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

app.add_middleware(
    AuthMiddleware,
    protected_prefixes=("/me/", "/transactions", "/messaging"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["ETag"]
)

# -----------------------------------------------------------------------------
# Include Routers
# -----------------------------------------------------------------------------
app.include_router(address_router)
app.include_router(address_user_router)
app.include_router(item_address_router)
app.include_router(item_router)
app.include_router(item_user_router)
app.include_router(root_router)
app.include_router(transaction_router)
app.include_router(transaction_user_item_router)
app.include_router(user_router)
app.include_router(message_router)
app.include_router(thread_router)
