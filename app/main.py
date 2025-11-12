from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.resources.item_user_router import item_user_router
from app.resources.public_router import public_router
from app.resources.user_router import user_router
from app.utils.config import init_env
from app.utils.db_connection import create_db_and_tables, close_db_connection

# Table Models (Necessary)
from app.models.po.item_user_po import ItemUser
from app.models.po.transaction_user_item_po import TransactionUserItem
from app.models.po.address_user_po import AddressUser
from app.models.po.item_address_po import ItemAddress

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


# -----------------------------------------------------------------------------
# Include Routers
# -----------------------------------------------------------------------------
app.include_router(public_router)
app.include_router(user_router)
app.include_router(item_user_router)
