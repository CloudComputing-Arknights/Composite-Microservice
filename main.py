from __future__ import annotations

import os
from typing import Optional, List
from uuid import UUID

from fastapi import FastAPI, HTTPException, Request, status, JSONResponse

import concurrent.futures
from client.user.user_address_api_client.api.default.get_user_users_user_id_get import (
    sync as get_user_by_id,
)
from client.transaction.transaction_api_client.api.default.list_transactions_transactions_get import (
    sync as list_transactions,
)

# Composite models (Pydantic) used by this API layer
from models.composite import (
    LoginRequest,
    LoginResponse,
    CurrentUser,
    CreateOwnItemRequest,
    UpdateOwnItemRequest,
    TransactionInitRequest,
    TransactionInitResponse,
)

# Generated API clients
from client.user.user_address_api_client.client import Client as UserClient
from client.user.user_address_api_client.api.default.list_users_users_get import (
    sync as list_users,
)
from client.user.user_address_api_client.models.user_read import UserRead

from client.item.item_thread_api_client.client import Client as ItemClient
from client.item.item_thread_api_client.api.items.create_item_items_post import (
    sync as create_item,
)
from client.item.item_thread_api_client.api.items.get_item_items_item_id_get import (
    sync as get_item,
)
from client.item.item_thread_api_client.api.items.update_item_items_item_id_patch import (
    sync as update_item,
)
from client.item.item_thread_api_client.api.items.delete_item_items_item_id_delete import (
    sync as delete_item,
)
from client.item.item_thread_api_client.api.items.list_items_items_get import (
    sync as list_items,
)
from client.item.item_thread_api_client.models.item_create import ItemCreate
from client.item.item_thread_api_client.models.item_update import ItemUpdate
from client.item.item_thread_api_client.models.item_read import ItemRead

from client.transaction.transaction_api_client.client import Client as TransactionClient
from client.transaction.transaction_api_client.api.default.create_transaction_transactions_transaction_post import (
    sync as create_transaction,
)
from client.transaction.transaction_api_client.models.new_transaction_request import (
    NewTransactionRequest,
)
from client.transaction.transaction_api_client.models.transaction import Transaction


port = int(os.environ.get("FASTAPIPORT", 8000))


# -----------------------------------------------------------------------------
# FastAPI App Definition
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Composite API",
    description="An API to orchestrate calls to other microservices.",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# Root Endpoint
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Composite API. See /docs for details."}


# -----------------------------------------------------------------------------
# Service Base URLs (can be overridden via environment variables)
# -----------------------------------------------------------------------------
USER_SERVICE_URL = os.environ.get(
    "USER_SERVICE_URL", "https://users-api-121084561869.us-central1.run.app"
)
ITEM_SERVICE_URL = os.environ.get(
    "ITEM_SERVICE_URL", "https://microservice-item-713181822049.us-central1.run.app"
)
TRANSACTION_SERVICE_URL = os.environ.get(
    "TRANSACTION_SERVICE_URL", "http://34.172.7.104:8000"
)

# Initialize simple reusable clients (httpx clients will be opened lazily)
_user_client = UserClient(base_url=USER_SERVICE_URL)
_item_client = ItemClient(base_url=ITEM_SERVICE_URL)
_transaction_client = TransactionClient(base_url=TRANSACTION_SERVICE_URL)


# -----------------------------------------------------------------------------
# Placeholder Auth Utilities
# -----------------------------------------------------------------------------

def get_current_username(request: Request) -> Optional[str]:
    """Placeholder for extracting the current logged-in username.

    TODO: Replace with real authentication (session/cookies/JWT). For now, you can
    simulate a logged-in user by sending the "X-Debug-Username" HTTP header.
    """

    username = request.headers.get("X-Debug-Username")
    return username or None


def _resolve_user_uuid_by_username(username: str) -> Optional[UUID]:
    """Lookup the user's UUID in the User service by username."""
    try:
        users = list_users(client=_user_client, username=username)
        if isinstance(users, list) and users:
            first: UserRead = users[0]
            # attrs class exposes `id` attribute (UUID)
            return getattr(first, "id", None) or None
    except Exception:
        # Hide upstream errors behind a generic resolution failure for now
        return None
    return None


# -----------------------------------------------------------------------------
# Auth Endpoints (placeholders)
# -----------------------------------------------------------------------------
@app.post("/auth/login", response_model=LoginResponse)
def auth_login(payload: LoginRequest):
    # Placeholder only. No real authentication is performed here.
    return LoginResponse(
        message=(
            "Login not implemented. Use the 'X-Debug-Username' header to simulate "
            f"being logged in as '{payload.username}'."
        )
    )


@app.post("/auth/logout", response_model=LoginResponse)
def auth_logout():
    # Placeholder only. Instruct clients to drop any local tokens/cookies they use for simulation.
    return LoginResponse(message="Logout not implemented. Remove X-Debug-Username header to simulate logout.")


@app.get("/auth/me", response_model=CurrentUser)
def auth_me(request: Request):
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = _resolve_user_uuid_by_username(username)
    return CurrentUser(username=username, user_id=user_uuid)


# -----------------------------------------------------------------------------
# Endpoints for the logged-in user
# -----------------------------------------------------------------------------
@app.post("/me/items")
def create_item_for_me(payload: CreateOwnItemRequest, request: Request):
    """Create an item owned by the currently logged-in user.

    Note: Ownership is enforced server-side using the resolved user UUID; the request
    body does not allow the caller to override the user.
    """
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = _resolve_user_uuid_by_username(username)
    if not user_uuid:
        raise HTTPException(status_code=400, detail="Could not resolve current user in User service")

    body = ItemCreate(
        title=payload.title,
        condition=payload.condition,
        transaction_type=payload.transaction_type,
        price=payload.price,
        description=payload.description,
        category=payload.category or None,
        location=payload.location,
        image_urls=payload.image_urls or [],
        user_uuid=user_uuid,
    )
    created = create_item(client=_item_client, body=body)
    if created is None:
        raise HTTPException(status_code=502, detail="Item service did not return a response")
    if hasattr(created, "to_dict"):
        return created.to_dict()
    return created


@app.get("/me/items")
def list_my_items(request: Request, skip: int = 0, limit: int = 10):
    """List items belonging to the current user.

    TODO: The Item service currently does not expose a filter by user. This implementation
    retrieves a page and filters client-side. It may miss items beyond the current page.
    """
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = _resolve_user_uuid_by_username(username)
    if not user_uuid:
        raise HTTPException(status_code=400, detail="Could not resolve current user in User service")

    items = list_items(client=_item_client, skip=skip, limit=limit)
    if not isinstance(items, list):
        return []

    mine: List[ItemRead] = [it for it in items if getattr(it, "user_uuid", None) == user_uuid]
    # Convert to plain dicts for JSON response
    return [it.to_dict() if hasattr(it, "to_dict") else it for it in mine]


@app.patch("/me/items/{item_id}")
def update_my_item(item_id: UUID, payload: UpdateOwnItemRequest, request: Request):
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = _resolve_user_uuid_by_username(username)
    if not user_uuid:
        raise HTTPException(status_code=400, detail="Could not resolve current user in User service")

    # Ensure ownership (placeholder enforcement via Item service lookup)
    existing = get_item(client=_item_client, item_id=item_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Item not found")
    owner_uuid = getattr(existing, "user_uuid", None)
    if not owner_uuid or owner_uuid != user_uuid:
        raise HTTPException(status_code=403, detail="Cannot modify an item you do not own")

    body = ItemUpdate(
        title=payload.title if payload.title is not None else None,
        description=payload.description if payload.description is not None else None,
        condition=payload.condition if payload.condition is not None else None,
        category=payload.category if payload.category is not None else None,
        transaction_type=payload.transaction_type if payload.transaction_type is not None else None,
        price=payload.price if payload.price is not None else None,
        location=payload.location if payload.location is not None else None,
        image_urls=payload.image_urls if payload.image_urls is not None else None,
    )
    updated = update_item(client=_item_client, item_id=item_id, body=body)
    if updated is None:
        raise HTTPException(status_code=502, detail="Item service did not return a response")
    return updated.to_dict() if hasattr(updated, "to_dict") else updated


@app.delete("/me/items/{item_id}")
def delete_my_item(item_id: UUID, request: Request):
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = _resolve_user_uuid_by_username(username)
    if not user_uuid:
        raise HTTPException(status_code=400, detail="Could not resolve current user in User service")

    existing = get_item(client=_item_client, item_id=item_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Item not found")
    owner_uuid = getattr(existing, "user_uuid", None)
    if not owner_uuid or owner_uuid != user_uuid:
        raise HTTPException(status_code=403, detail="Cannot delete an item you do not own")

    deleted = delete_item(client=_item_client, item_id=item_id)
    # Item service delete may return validation error or nothing; respond with placeholder message
    return {"message": "Item delete requested", "item_id": str(item_id)}


@app.post("/me/transactions")
def create_transaction_for_me(payload: TransactionInitRequest, request: Request):
    """Start a transaction as the current user (placeholder).

    Note: Transaction service uses integer item IDs and string user IDs; this endpoint
    assumes your user identifier in that service equals your username.
    """
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    body = NewTransactionRequest(
        item_id=payload.item_id,
        initiator_user_id=username,
        receiver_user_id=payload.receiver_user_id,
    )
    tx = create_transaction(client=_transaction_client, body=body)
    if tx is None:
        raise HTTPException(status_code=502, detail="Transaction service did not return a response")
    return tx.to_dict() if hasattr(tx, "to_dict") else tx


# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
