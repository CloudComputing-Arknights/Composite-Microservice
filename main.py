from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, status
from typing import List
from models.composite import EnrichedPost, EnrichedTrade, TradeInitiationRequest, PostAuthor

from services import user_service, item_service, transaction_service

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
# Composite Endpoints
# -----------------------------------------------------------------------------

@app.get("/posts", response_model=List[EnrichedPost])
async def get_all_posts():
    """
    Gets all items and enriches them with author's username.
    """
    items = await item_service.list_items()
    if not items:
        return []

    user_ids = [item['user_UUID'] for item in items]
    users_map = await user_service.get_users_by_ids(user_ids)

    enriched_posts = []
    for item in items:
        author_data = users_map.get(item['user_UUID'])
        if author_data:
            author = PostAuthor(id=author_data['id'], username=author_data['username'])
            post = EnrichedPost(**item, author=author)
            enriched_posts.append(post)

    return enriched_posts

@app.post("/trades", status_code=status.HTTP_201_CREATED)
async def initiate_trade(request: TradeInitiationRequest):
    """
    Initiates a trade by creating a new transaction.
    It first fetches the item to identify the receiver (owner).
    """
    # 1. Get item details to find the owner (receiver)
    item = await item_service.get_item_by_id(request.item_id)
    receiver_user_id = item.get("user_UUID")

    if not receiver_user_id:
        raise HTTPException(status_code=404, detail="Item owner not found.")

    if request.initiator_user_id == receiver_user_id:
        raise HTTPException(status_code=400, detail="Cannot initiate a trade with yourself.")

    # 2. Create the transaction
    # The transaction service expects an integer for itemId, which is a mismatch with item service UUID.
    # This is an issue in the microservice design. For this example, we'll assume
    # the front-end has a mapping or we can't fulfill this request.
    # Let's raise a specific error to highlight this incompatibility.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Cannot create trade: Item service uses UUIDs for items, but Transaction service requires integer IDs. This is an architectural incompatibility."
    )

@app.get("/users/{user_id}/trades", response_model=List[EnrichedTrade])
async def get_user_trades(user_id: str):
    """
    Gets a user's transaction history, enriched with item and user details.
    """
    transactions = await transaction_service.list_transactions_for_user(user_id)
    if not transactions:
        return []

    # Again, we face the item ID type mismatch. We cannot proceed to fetch item details.
    # If the IDs were compatible (e.g., both UUIDs), the logic would be as follows.
    # For now, we return an error.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Cannot fetch trades: Item service uses UUIDs for items, but Transaction service uses integer IDs. This is an architectural incompatibility."
    )

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
