from app.utils.http_client import call_service

ITEM_SERVICE_URL = "https://microservice-item-848539791549.us-central1.run.app"  

async def get_all_items(session):
    """
    Fetch all items from the external Item Service.
    """
    return await call_service("GET", f"{ITEM_SERVICE_URL}/items")

async def get_item_by_id(session, item_id: str):
    """
    Get item details by ID from the external Item Service.
    """
    return await call_service("GET", f"{ITEM_SERVICE_URL}/items/{item_id}")

async def create_item(session, item_data: dict):
    """
    Create a new item.
    """
    return await call_service("POST", f"{ITEM_SERVICE_URL}/items", json=item_data)

async def update_item(session, item_id: str, update_data: dict):
    """
    Update item details.
    """
    return await call_service("PUT", f"{ITEM_SERVICE_URL}/items/{item_id}", json=update_data)

async def delete_item(session, item_id: str):
    """
    Delete item by ID.
    """
    return await call_service("DELETE", f"{ITEM_SERVICE_URL}/items/{item_id}")