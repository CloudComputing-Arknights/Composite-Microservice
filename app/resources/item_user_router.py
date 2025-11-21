from fastapi import APIRouter, Request, Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
import logging

from app.client.item.item_api_client.client import Client
from app.client.item.item_api_client.models import HTTPValidationError
from app.client.item.item_api_client.api.items import (
    create_item_items_post,
    get_job_status_items_jobs_job_id_get,
    update_item_items_item_id_patch
)

from app.models.dto.item_user_dto import CreateOwnItemReq, UpdateOwnItemReq
from app.models.dto.item_dto import ItemCreate, ItemRead, ItemUpdate
from app.models.dto.job_dto import JobRead, JobStatus
from app.services.item_user_repository import (
    create_item_user_relation,
    verify_item_ownership
)
from app.services.item_user_repository import (
    get_user_items
)
from app.utils.auth import get_user_id_from_token
from app.utils.db_connection import SessionDep
from app.utils.config import get_item_client


log = logging.getLogger(__name__)
item_user_router = APIRouter(
    tags=["Item User"]
)

security = HTTPBearer()

@item_user_router.post(
    "/me/items",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=JobRead
)
async def create_item_for_me(
        payload: CreateOwnItemReq,
        token: HTTPAuthorizationCredentials = Depends(security),
        client: Client = Depends(get_item_client)
):
    try:
        user_uuid = get_user_id_from_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    # downstream_req = ItemCreate(**payload.model_dump(exclude={"address_UUID"}))
    downstream_req = ItemCreate(**payload.model_dump())

    # Handle the job returned by the request
    job_response = await create_item_items_post.asyncio(
        client=client,
        body=downstream_req.to_client_model(),
    )
    if job_response is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Item service didn't return job."
        )
    if isinstance(job_response, HTTPValidationError):
        log.error(
            "Downstream 'item service' validation failed for POST /me/items. Response: %s",
            job_response.to_dict()
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred."
        )

    # Return 202 & job_uuid
    return JobRead(
        job_UUID=job_response.job_uuid,
        status=job_response.status,
        item_UUID=job_response.item_uuid,
        error_message=job_response.error_message
    )


@item_user_router.get(
    "/me/items/jobs/{job_id}",
    response_model=JobRead,
    summary="Check status of job, store item-user relation when job is COMPLETED",
)
async def get_my_job_status(
        job_id: UUID,
        # address_id: UUID,   # TODO: weird to include address_id here ...
        session: SessionDep,
        token: HTTPAuthorizationCredentials = Depends(security),
        client: Client = Depends(get_item_client)
):
    try:
        user_uuid = get_user_id_from_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Request for job
    downstream_response = await get_job_status_items_jobs_job_id_get.asyncio(
        job_id=job_id,
        client=client
    )
    if downstream_response is None:
        log.error(
            "Downstream 'item service' returns none for GET /me/items/jobs/{jobs_id}.",
        )
        raise HTTPException(status_code=502, detail="Downstream service returned no content")
    if isinstance(downstream_response, HTTPValidationError):
        log.error(
            "Downstream 'item service' validation failed for GET /me/items/jobs/{jobs_id}. Response: %s",
            downstream_response.to_dict()
        )
        raise HTTPException(status_code=500, detail="Downstream integration error")

    # Store item-user relation if it's COMPLETED.
    if downstream_response.status == JobStatus.COMPLETED and downstream_response.item_uuid:
        item_id_str = str(downstream_response.item_uuid)
        user_id_str = str(user_uuid)
        # address_id_str = str(address_id)

        # [Idempotence Check] Check whether the relationship already exists
        is_owned = await verify_item_ownership(
            session=session,
            item_id=item_id_str,
            user_id=user_id_str
        )
        if not is_owned:
            await create_item_user_relation(
                session=session,
                item_id=item_id_str,
                user_id=user_id_str
            )

        # address info has been stored in item MS downstream
        # Store item-address relation
        # await create_item_address_relation(
        #     session=session,
        #     item_id=item_id_str,
        #     address_id=address_id_str
        # )

    return JobRead(
        job_UUID=downstream_response.job_uuid,
        status=JobStatus(downstream_response.status),
        item_UUID=downstream_response.item_uuid,
        error_message=getattr(downstream_response, "error_message", None)
    )


@item_user_router.get("/me/items")
async def list_my_items(
        request: Request,
        session: SessionDep,
        skip: int = 0,
        limit: int = 10,
        token: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        user_uuid = get_user_id_from_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@item_user_router.patch("/me/items/{item_id}", response_model=ItemRead)
async def update_my_item(
        item_id: UUID,
        payload: UpdateOwnItemReq,
        session: SessionDep,
        if_match: str = Header(..., alias="If-Match", description="ETag required for concurrent update protection"),
        token: HTTPAuthorizationCredentials = Depends(security),
        client: Client = Depends(get_item_client),
):
    try:
        user_uuid = get_user_id_from_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    is_owned = await verify_item_ownership(
        session=session,
        item_id=str(item_id),
        user_id=str(user_uuid)
    )

    if not is_owned:
        raise HTTPException(status_code=404, detail="Item not found or access denied")

    downstream_req = ItemUpdate(**payload.model_dump(exclude_unset=True)).to_client_model()

    print(downstream_req.to_dict())

    response = await update_item_items_item_id_patch.asyncio(
        item_id=item_id,
        client=client,
        body=downstream_req,
        if_match=if_match
    )

    if response is None:
        raise HTTPException(
            status_code=502,
            detail="Downstream item service returned None for PATCH /me/items/{item_id}."
        )
    if isinstance(response, HTTPValidationError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=response.to_dict() if hasattr(response, "to_dict") else "Validation error"
        )

    return ItemRead(**response.to_dict())

@item_user_router.delete("/me/items/{item_id}")
async def delete_my_item(item_id: str, request: Request, session: SessionDep):
    authorization_header = request.headers.get("Authorization")
    user_id = get_user_id_from_token(authorization_header)
    token = authorization_header.replace("Bearer ", "")
    pass
