from app.repositories.item_repository import (
    get_all_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item
)

async def get_all_items():
    return await get_all_items()

async def get_item_by_id(item_id: str):
    return await get_item_by_id(item_id)

async def create_item(item_data):
    return await create_item(item_data)

async def update_item(item_id: str, item_data):
    return await update_item(item_id, item_data)

async def delete_item(item_id: str):
    return await delete_item(item_id)