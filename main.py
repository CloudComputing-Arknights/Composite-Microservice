from __future__ import annotations
import os
import asyncio
import time

from fastapi import (
FastAPI, 
HTTPException,
status,
BackgroundTasks,
Header,
Request,
)

from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
from pydantic import BaseModel, EmailStr

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
# (New) Global 500 Error Handler
# -----------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    (New) Catches all unhandled exceptions (bugs) in the application.
    
    [Implements: 500 Internal Server Error]
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_type": "InternalServerError",
            "message": "An unexpected internal server error occurred.",
            "detail": str(exc), # Should be hidden in production
        },
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
# (New) Pydantic Models for New Endpoints
# -----------------------------------------------------------------------------

# (New) Models for 202 Accepted
class ReportRequest(BaseModel):
    report_type: str
    user_id: str

class ReportStatus(BaseModel):
    job_id: str
    status: str
    message: str

# (New) Model for 412/428 ETag (PUT)
class ItemUpdate(BaseModel):
    title: str
    price: float

# (New) Models for DBaaS (Stateful) Placeholders
# These models represent the "JOIN" Data from your professor's slide
class UserProfileDetails(BaseModel):
    id: str
    username: str
    email: EmailStr # Example of additional data
    created_at: str # Example of additional data

class UserItemSummary(BaseModel):
    item_UUID: str
    title: str
    price: float

class UserProfileResponse(BaseModel):
    """
    This is the response model for the "Stateful" (Mode 2)
    user profile endpoint.
    """
    user_details: UserProfileDetails
    listed_items: List[UserItemSummary]
    trade_history: List[EnrichedTrade]
    

# -----------------------------------------------------------------------------
# (New) Mock Database for ETag Demonstration
# -----------------------------------------------------------------------------
MOCK_ETAG_DB = {
    # Simulates that item "item-abc" has a current version of "v1"
    "item-abc": {"version_etag": '"v1"'} 
}

# -----------------------------------------------------------------------------
# (New) "Mode 2" (Stateful DBaaS) Placeholder Endpoints
# -----------------------------------------------------------------------------

@app.get("/users/{user_id}/profile", response_model=UserProfileResponse)
async def get_user_profile_from_dbaas(user_id: str):
    """
    (New) "Stateful" (DBaaS) aggregation placeholder.
    
    [Implements: 501 Not Implemented] (as a placeholder)
    
    
    # --- Placeholder Logic ---
    #
    # In the future, the implementation here will be:
    # 1. Connect to your own DBaaS (e.g., Google Cloud SQL).
    # 2. Execute 3 parallel *local* queries:
    #    - task1 = my_dbaas.find_user(user_id)
    #    - task2 = my_dbaas.find_items_by_user(user_id)
    #    - task3 = my_dbaas.find_enriched_trades_by_user(user_id)
    # 3. (details, items, trades) = await asyncio.gather(task1, task2, task3)
    # 4. If details is None, raise [404 Not Found].
    # 5. return {"user_details": details, ...} <-- This will return [200 OK].
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="DBaaS (Stateful) pattern is not yet implemented. This endpoint will query the local 'JOIN' database in the future."
    )

# -----------------------------------------------------------------------------
# (New) Endpoints to Demonstrate Specific Requirements
# -----------------------------------------------------------------------------

def blocking_sync_report_task(user_id: str):
    """
    This is a [Synchronous] blocking function.
    It will be run by BackgroundTasks in a separate thread.
    """
    print(f"!!! [Background Thread]: Starting 10-second sync task for {user_id}...")
    time.sleep(10) # Simulates a long, blocking I/O or CPU task
    print(f"!!! [Background Thread]: ...Sync task for {user_id} complete.")
    # In a real app, this would write the report to a DB or S3 bucket.
    
@app.post("/reports", response_model=ReportStatus)
async def create_report(request: ReportRequest, background_tasks: BackgroundTasks):
    """
    (New) Demonstrates using threading for a sync call.
    
    [Implements: 202 Accepted]
    """
    job_id = f"job_{int(time.time())}"
    
    # 1. Add the "synchronous call" (blocking_sync_report_task)
    #    to the background task queue. FastAPI runs this in a threadpool.
    background_tasks.add_task(
        blocking_sync_report_task, 
        user_id=request.user_id
    )
    
    # 2. Return 202 Immediately.
    print(f"--- Main Thread: Job {job_id} queued. Returning 202 immediately. ---")
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "job_id": job_id,
            "status": "queued",
            "message": "Report generation has been queued in the background."
        }
    )


@app.put("/items-concurrency-demo/{item_id}", response_model=Dict)
async def update_item_with_etag(
    item_id: str, 
    item_update: ItemUpdate, 
    if_match: Optional[str] = Header(None) # Get ETag from Header
):
    """
    (New) Demonstrates ETag for optimistic concurrency control.
    
    [Implements: 428 Precondition Required]
    [Implements: 412 Precondition Failed]
    [Implements: 200 OK] (On successful PUT)
    """
    # 1. Check if ETag was provided
    if not if_match:
        raise HTTPException(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail="If-Match header is required for this operation to prevent lost updates.",
        )
        
    # 2. Check if resource exists (using our mock DB)
    if item_id not in MOCK_ETAG_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
        
    # 3. Check if ETag matches
    current_etag = MOCK_ETAG_DB[item_id]["version_etag"]
    if if_match != current_etag:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Resource has been modified by someone else. Your ETag '{if_match}' is stale. Please reload the resource.",
        )
        
    # 4. All checks passed. Perform update (simulate).
    print(f"ETag {if_match} matched! Performing update...")
    new_etag = f'"v{int(time.time())}"' # Create a new ETag
    MOCK_ETAG_DB[item_id]["version_etag"] = new_etag
    
    # Return 200 OK (for PUT) with the new ETag
    return JSONResponse(
        content={"message": "Update successful", "new_etag": new_etag},
        status_code=status.HTTP_200_OK,
        headers={"ETag": new_etag}
    )

@app.post("/demo-create", status_code=status.HTTP_201_CREATED)
async def demo_create_resource():
    """
    (New) Demonstrates a simple resource creation.
    
    [ImGgplements: 201 Created]
    """
    new_resource_id = "new-res-123"
    return JSONResponse(
        content={"id": new_resource_id, "message": "Resource created"},
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/demo-create/{new_resource_id}"}
    )

@app.get("/force-error")
async def force_error():
    """
    (New) Demonstrates an unexpected server bug.
    
    [Implements: 500 Internal Server Error]
    This will be caught by the global @app.exception_handler.
    """
    x = 1 / 0  # Simulates a bug
    return {"hello": "world"}
# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
