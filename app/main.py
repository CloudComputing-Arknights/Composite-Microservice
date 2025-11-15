from __future__ import annotations

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


from app.utils.config import init_env
from app.utils.db_connection import create_db_and_tables, close_db_connection
from fastapi.openapi.utils import get_openapi

# Table Models (Necessary)
from app.models.po.address_user_po import AddressUser
from app.models.po.item_address_po import ItemAddress
from app.models.po.item_user_po import ItemUser
from app.models.po.transaction_user_item_po import TransactionUserItem

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
app.include_router(address_router)
app.include_router(address_user_router)
app.include_router(item_address_router)
app.include_router(item_router)
app.include_router(item_user_router)
app.include_router(root_router)
app.include_router(transaction_router)
app.include_router(transaction_user_item_router)
app.include_router(user_router)


# -----------------------------------------------------------------------------
# Authorizwation in OpenAPI
# -----------------------------------------------------------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Composite API",
        version="1.0.0",
        description="An API to orchestrate calls to other microservices.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi