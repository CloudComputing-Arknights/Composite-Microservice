from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import (
    get_all_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item
)

# Create the APIRouter instance.
# `prefix="/items"` means all endpoints will start with `/items`
# `tags=["Items"]` groups them in the Swagger UI.
item_router = APIRouter(prefix="/items", tags=["Items"])

# -----------------------------------------------------------------------------
# Public endpoint: Get a list of all items.
# This does NOT require user authentication — anyone can call it.
# -----------------------------------------------------------------------------
@item_router.get("/", response_model=List[ItemResponse])
async def list_items():
    items = await get_all_items()
    return items

# -----------------------------------------------------------------------------
# Public endpoint: Get details of a single item by its ID.
# -----------------------------------------------------------------------------
@item_router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    item = await get_item_by_id(item_id)
    if not item:
        # If item is not found, return HTTP 404.
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# -----------------------------------------------------------------------------
# Admin endpoint: Create a new item in the system.
# In a real setup, you might want to add authentication and admin role checks.
# -----------------------------------------------------------------------------
@item_router.post("/", response_model=ItemResponse)
async def create_new_item(item_data: ItemCreate):
    item = await create_item(item_data)
    return item

# -----------------------------------------------------------------------------
# Admin endpoint: Update an existing item by ID.
# -----------------------------------------------------------------------------
@item_router.patch("/{item_id}", response_model=ItemResponse)
async def update_existing_item(item_id: str, item_data: ItemUpdate):
    updated_item = await update_item(item_id, item_data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

# -----------------------------------------------------------------------------
# Admin endpoint: Delete an existing item by ID.
# -----------------------------------------------------------------------------
@item_router.delete("/{item_id}")
async def delete_existing_item(item_id: str):
    success = await delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted successfully"}