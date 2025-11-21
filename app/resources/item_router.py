import logging
from fastapi import APIRouter, Depends, status, Query, Response
from fastapi.exceptions import HTTPException
from typing import List, Optional
from uuid import UUID

from app.client.item.item_api_client.client import Client
from app.client.item.item_api_client.api.items import (
    list_items_items_get,
    get_item_items_item_id_get,
    list_categories_items_categories_get
)
from app.client.item.item_api_client.models import HTTPValidationError
from app.models.dto.item_dto import (
    ItemRead,
    CategoryRead,
    TransactionType
)
from app.utils.config import get_item_client

log = logging.getLogger(__name__)

item_router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@item_router.get(
    "/",
    response_model=List[ItemRead],
    summary="Get items through pagination.",
)
async def list_public_items(
    item_ids: Optional[List[UUID]] = Query(
        None, alias="id", description="Filter by a list of item IDs"
    ),
    category_id: Optional[int] = Query(
        None, description="Filter by item's category"
    ),
    transaction_type: Optional[TransactionType] = Query(
        None, description="Filter by item's transaction type"
    ),
    search: Optional[str] = Query(None, description="Search by item title (case-insensitive, partial match)"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of items to return"),
    client: Client = Depends(get_item_client)
):
    """
    Get items through pagination, can be filtered by ID, category, condition, transaction type
    """
    print("in list_public_items")
    response = await list_items_items_get.asyncio(
        client=client,
        id=item_ids,
        category_id=category_id,
        # condition=condition,
        transaction_type=transaction_type,
        search=search,
        skip=skip,
        limit=limit,
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Item service is unavailable."
        )

    if isinstance(response, HTTPValidationError):
        log.error(
            "Downstream 'item service' validation failed. Response: %s",
            response.to_dict()
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred."
        )
    return [ItemRead(**item.to_dict()) for item in response]


@item_router.get(
    "/categories",
    response_model=List[CategoryRead]
)
async def list_categories(
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(10, ge=1, le=100, description="Max number of items to return"),
        client: Client = Depends(get_item_client)
) -> List[CategoryRead]:
    downstream_response = await list_categories_items_categories_get.asyncio(
        client=client,
        skip=skip,
        limit=limit
    )
    return [CategoryRead(**category.to_dict()) for category in downstream_response]


@item_router.get(
    "/{item_id}",
    response_model=ItemRead,
    summary="Get an item by its id",
)
async def get_public_item_by_id(
    item_id: UUID,
    response: Response,
    client: Client = Depends(get_item_client)
):
    """
    Get an item by its id
    """
    downstream_response = await get_item_items_item_id_get.asyncio(
        client=client,
        item_id=item_id
    )

    if downstream_response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    if isinstance(downstream_response, HTTPValidationError):
        log.error(
            "Downstream 'item service' validation failed for GET /items/%s. Response: %s",
            item_id,
            downstream_response.to_dict()
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred."
        )
    etag_value = downstream_response.updated_at.isoformat()    # timestamp -> ISO string
    response.headers["ETag"] = f'"{etag_value}"'
    return ItemRead(**downstream_response.to_dict())
