from fastapi import APIRouter, status, HTTPException
from app.utils.db_connection import SessionDep
from app.services.messaging_repository import create_thread_user_relation
import app.utils.env_clients as clients

from app.client.messaging.messaging_microservice_client.api.threads.create_thread_threads_post import (
    asyncio as create_thread_async,
    asyncio_detailed as create_thread_async_detailed,
)

from app.client.messaging.messaging_microservice_client.models.thread_create import ThreadCreate
from app.client.messaging.messaging_microservice_client.models.http_validation_error import HTTPValidationError


router = APIRouter(
    prefix="/messaging/threads",
    tags=["Messaging Threads"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_thread(
    author_id: str,
    participant_id: str,
    session: SessionDep,
):
    messaging_client = clients.get_messaging_client()

    body = ThreadCreate(
        author_id=author_id,
        participant_id=participant_id,
    )

    response = await create_thread_async_detailed(
        client=messaging_client,
        body=body,
    )

    parsed = response.parsed

    if isinstance(parsed, HTTPValidationError):
        raise HTTPException(
            status_code=400,
            detail=f"Messaging validation error: {parsed.to_dict()}"
        )

    if parsed is None:
        raise HTTPException(
            status_code=500,
            detail="Messaging microservice returned no data"
        )

    thread_id = parsed.thread_id
    await create_thread_user_relation(session, thread_id, author_id)
    await create_thread_user_relation(session, thread_id, participant_id)
    return parsed.to_dict()
