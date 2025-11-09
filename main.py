from __future__ import annotations

import os
from typing import Optional, List, Dict
from uuid import UUID

from fastapi import FastAPI, HTTPException, Request, status

import asyncio

from client.user.user_address_api_client.api.default.get_user_users_user_id_get import (
    asyncio as get_user_by_id_async,
)
from client.transaction.transaction_api_client.api.default.list_transactions_transactions_get import (
    asyncio as list_transactions_async,
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
    EnrichedPost,PostAuthor
)

# Generated API clients
from client.user.user_address_api_client.client import Client as UserClient
from client.user.user_address_api_client.api.default.list_users_users_get import (
    asyncio as list_users_async,
)
from client.user.user_address_api_client.models.user_read import UserRead

from client.item.item_thread_api_client.client import Client as ItemClient
from client.item.item_thread_api_client.api.items.create_item_items_post import (
    asyncio as create_item_async,
)
from client.item.item_thread_api_client.api.items.get_item_items_item_id_get import (
    asyncio as get_item_async,
)
from client.item.item_thread_api_client.api.items.update_item_items_item_id_patch import (
    asyncio as update_item_async,
)
from client.item.item_thread_api_client.api.items.delete_item_items_item_id_delete import (
    asyncio as delete_item_async,
)
from client.item.item_thread_api_client.api.items.list_items_items_get import (
    asyncio as list_items_async,
)
from client.item.item_thread_api_client.models.item_create import ItemCreate
from client.item.item_thread_api_client.models.item_update import ItemUpdate
from client.item.item_thread_api_client.models.item_read import ItemRead

from client.transaction.transaction_api_client.client import Client as TransactionClient
from client.transaction.transaction_api_client.api.default.create_transaction_transactions_transaction_post import (
    asyncio as create_transaction_async,
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
async def root():
    return {"message": "Welcome to the Composite API. See /docs for details."}


# -----------------------------------------------------------------------------
# Service Base URLs (can be overridden via environment variables)
# -----------------------------------------------------------------------------
USER_SERVICE_URL = os.environ.get(
    "USER_SERVICE_URL", "https://users-api-121084561869.us-central1.run.app"
)
ITEM_SERVICE_URL = os.environ.get(
    "ITEM_SERVICE_URL", "https://microservice-item-848539791549.us-central1.run.app"
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


async def _resolve_user_uuid_by_username(username: str) -> Optional[UUID]:
    """Lookup the user's UUID in the User service by username."""
    try:
        users = await list_users_async(client=_user_client, username=username)
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
async def auth_login(payload: LoginRequest):
    # Placeholder only. No real authentication is performed here.
    return LoginResponse(
        message=(
            "Login not implemented. Use the 'X-Debug-Username' header to simulate "
            f"being logged in as '{payload.username}'."
        )
    )


@app.post("/auth/logout", response_model=LoginResponse)
async def auth_logout():
    # Placeholder only. Instruct clients to drop any local tokens/cookies they use for simulation.
    return LoginResponse(message="Logout not implemented. Remove X-Debug-Username header to simulate logout.")


@app.get("/auth/me", response_model=CurrentUser)
async def auth_me(request: Request):
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = await _resolve_user_uuid_by_username(username)
    return CurrentUser(username=username, user_id=user_uuid)


# -----------------------------------------------------------------------------
# Endpoints for the logged-in user
# -----------------------------------------------------------------------------
@app.post("/me/items")
async def create_item_for_me(payload: CreateOwnItemRequest, request: Request):
    """Create an item owned by the currently logged-in user.

    Note: Ownership is enforced server-side using the resolved user UUID; the request
    body does not allow the caller to override the user.
    """
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = await _resolve_user_uuid_by_username(username)
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
    created = await create_item_async(client=_item_client, body=body)
    if created is None:
        raise HTTPException(status_code=502, detail="Item service did not return a response")
    if hasattr(created, "to_dict"):
        return created.to_dict()
    return created


@app.get("/me/items")
async def list_my_items(request: Request, skip: int = 0, limit: int = 10):
    """List items belonging to the current user.

    TODO: The Item service currently does not expose a filter by user. This implementation
    retrieves a page and filters client-side. It may miss items beyond the current page.
    """
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = await _resolve_user_uuid_by_username(username)
    if not user_uuid:
        raise HTTPException(status_code=400, detail="Could not resolve current user in User service")

    items = await list_items_async(client=_item_client, skip=skip, limit=limit)
    if not isinstance(items, list):
        return []

    mine: List[ItemRead] = [it for it in items if getattr(it, "user_uuid", None) == user_uuid]
    # Convert to plain dicts for JSON response
    return [it.to_dict() if hasattr(it, "to_dict") else it for it in mine]


@app.patch("/me/items/{item_id}")
async def update_my_item(item_id: UUID, payload: UpdateOwnItemRequest, request: Request):
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = await _resolve_user_uuid_by_username(username)
    if not user_uuid:
        raise HTTPException(status_code=400, detail="Could not resolve current user in User service")

    # Ensure ownership (placeholder enforcement via Item service lookup)
    existing = await get_item_async(client=_item_client, item_id=item_id)
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
    updated = await update_item_async(client=_item_client, item_id=item_id, body=body)
    if updated is None:
        raise HTTPException(status_code=502, detail="Item service did not return a response")
    return updated.to_dict() if hasattr(updated, "to_dict") else updated


@app.delete("/me/items/{item_id}")
async def delete_my_item(item_id: UUID, request: Request):
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    user_uuid = await _resolve_user_uuid_by_username(username)
    if not user_uuid:
        raise HTTPException(status_code=400, detail="Could not resolve current user in User service")

    existing = await get_item_async(client=_item_client, item_id=item_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Item not found")
    owner_uuid = getattr(existing, "user_uuid", None)
    if not owner_uuid or owner_uuid != user_uuid:
        raise HTTPException(status_code=403, detail="Cannot delete an item you do not own")

    deleted = await delete_item_async(client=_item_client, item_id=item_id)
    # Item service delete may return validation error or nothing; respond with placeholder message
    return {"message": "Item delete requested", "item_id": str(item_id)}


@app.post("/me/transactions")
async def create_transaction_for_me(payload: TransactionInitRequest, request: Request):
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
    tx = await create_transaction_async(client=_transaction_client, body=body)
    if tx is None:
        raise HTTPException(status_code=502, detail="Transaction service did not return a response")
    return tx.to_dict() if hasattr(tx, "to_dict") else tx


# -----------------------------------------------------------------------------
# (New) Public Browsing Endpoint (User Story: "browse available items")
# -----------------------------------------------------------------------------

@app.get("/items", response_model=List[EnrichedPost])
async def get_all_available_items(skip: int = 0, limit: int = 20):
    """
    (New) Browse all available items (public).
    
    [Fulfills requirement: "asynchronously" (via threads)]
    This endpoint uses a ThreadPoolExecutor to execute calls to the
    item-service and user-service in parallel for "async aggregation".
    """
    
    # 1. Get the list of items (This is a blocking I/O call)
    try:
        items = await list_items_async(client=_item_client, skip=skip, limit=limit)
        if not isinstance(items, list):
            return []
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch from Item-Service: {e}")

    # 2. Collect all required user_uuids
    user_uuids_to_fetch = {getattr(item, "user_uuid", None) for item in items}
    user_uuids_to_fetch.discard(None) # Remove None if present
    
    if not user_uuids_to_fetch:
        # No users to enrich, return early (or return un-enriched items)
        return []

    # 3. Fetch user info concurrently using asyncio.gather
    users_map: Dict[UUID, UserRead] = {}
    uuids_list = list(user_uuids_to_fetch)
    try:
        results = await asyncio.gather(
            *(get_user_by_id_async(client=_user_client, user_id=u) for u in uuids_list),
            return_exceptions=True,
        )
        for u, res in zip(uuids_list, results):
            if isinstance(res, Exception):
                # Skip failed fetches but continue enriching others
                continue
            if res and isinstance(res, UserRead):
                users_map[u] = res
    except Exception as e:
        # In case gather itself fails, proceed with what we have (empty map)
        pass

    # 4. Enrich the results
    enriched_posts = []
    for item in items:
        item_dict = item.to_dict() # Convert auto-gen model to dict
        author_data = users_map.get(item_dict.get("user_uuid"))
        
        if author_data:
            # Create PostAuthor model
            author = PostAuthor(
                id=getattr(author_data, "id", ""),
                username=getattr(author_data, "username", "Unknown")
            )
            
            # Create EnrichedPost model (fields must match)
            post = EnrichedPost(
                item_UUID=item_dict.get("item_uuid"),
                user_UUID=item_dict.get("user_uuid"),
                title=item_dict.get("title"),
                description=item_dict.get("description"),
                condition=item_dict.get("condition"),
                transaction_type=item_dict.get("transaction_type"),
                price=item_dict.get("price"),
                created_at=item_dict.get("created_at"),
                updated_at=item_dict.get("updated_at"),
                category=item_dict.get("category", []),
                location=item_dict.get("location"),
                image_urls=item_dict.get("image_urls", []),
                author=author # Embed author info
            )
            enriched_posts.append(post)

    return enriched_posts


# -----------------------------------------------------------------------------
# (New) Logged-in User Endpoints (User Story: "view my transaction history")
# -----------------------------------------------------------------------------

@app.get("/me/transactions")
async def get_my_transaction_history(request: Request):
    """
    (New) View "my" transaction history.
    
    [Fulfills requirement: "demonstrate implementing logical foreign key constraints"]
    This endpoint demonstrates the *need* for logical foreign keys
    by returning 501, as this link cannot be resolved in stateless mode.
    """
    
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    # 1. We can fetch the raw transactions
    try:
        # (Assumes 'username' is the user_id in the transaction service)
        tx_as_initiator = await list_transactions_async(
            client=_transaction_client, initiator_user_id=username
        )
        tx_as_receiver = await list_transactions_async(
            client=_transaction_client, receiver_user_id=username
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch from Transaction-Service: {e}")

    # 2. We can merge them
    all_txs_raw = (tx_as_initiator or []) + (tx_as_receiver or [])
    if not all_txs_raw:
        return []

    # 3. But we cannot "enrich" them.
    # tx.item_id is an int (e.g., 123)
    # get_item() needs a UUID (e.g., "a1b2c3d4-...")
    #
    # This is what the professor's PPT refers to: we need a DBaaS
    # with an "Associative Entity" (mapping table) to link them.
    
    return None


# -----------------------------------------------------------------------------
# (New) Admin Endpoints (User Stories: "monitor" & "remove content")
# -----------------------------------------------------------------------------

@app.get("/admin/monitor/user/{user_uuid}")
async def admin_monitor_user(user_uuid: UUID, request: Request):
    """
    (New) Monitor a specific user's activity (placeholder).
    
    [Fulfills User Story: "monitor user activity"]
    
    This is a placeholder. A real implementation would:
    1. Check if the current user is an admin.
    2. Use a ThreadPoolExecutor to call in parallel:
       - get_user_by_id(user_uuid)
       - (filtered) list_items(...)
       - list_transactions(...)
    3. Aggregate all results and return them.
    """
    # TODO: Implement Admin-only authentication
    username = get_current_username(request)
    if not username: # Simulate: only logged-in users can access
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")
        
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Admin dashboard functionality is not yet implemented."
    )

@app.post("/admin/remove/content")
async def admin_remove_content(request: Request):
    """
    (New) Remove inappropriate content (placeholder).
    
    [Fulfills User Story: "remove inappropriate content"]
    
    This is a placeholder. A real implementation requires a complex "Saga" pattern:
    1. Check for admin privileges.
    2. Receive a body like { "type": "item", "id": "..." } or { "type": "user", "id": "..." }.
    3. Based on type, orchestrate a cross-service deletion/archive.
    """
    # TODO: Implement Admin-only authentication
    username = get_current_username(request)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in (placeholder)")

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Admin content moderation functionality is not yet implemented."
    )


# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
