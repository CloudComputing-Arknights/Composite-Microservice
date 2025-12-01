from fastapi import APIRouter, HTTPException, Depends, Request, status
from app.utils.db_connection import SessionDep
from app.services.message_repository import get_thread_users
from app.utils.config import get_messaging_client
from app.client.message.messaging_microservice_client.api.messaging.send_message_threads_thread_id_messages_post import (
    asyncio_detailed as send_message_async_detailed,
)
from app.client.message.messaging_microservice_client.models.message_create import MessageCreate
from app.client.message.messaging_microservice_client.models.http_validation_error import HTTPValidationError

message_router = APIRouter(
    prefix="/messaging/messages",
    tags=["Messages"],
)

@message_router.post("/{thread_id}", status_code=status.HTTP_201_CREATED)
async def send_message(
    request: Request,
    thread_id: str,
    content: str,
    session: SessionDep,
    messaging_client = Depends(get_messaging_client),
):
    current_user_id = request.state.user_id

    # Validate membership
    users = await get_thread_users(session, thread_id)
    if current_user_id not in users:
        raise HTTPException(403, "You are not a participant in this thread")

    body = MessageCreate(
        author_id=current_user_id,
        content=content,
    )

    response = await send_message_async_detailed(
        client=messaging_client,
        thread_id=thread_id,
        body=body,
    )

    parsed = response.parsed

    if isinstance(parsed, HTTPValidationError):
        raise HTTPException(
            status_code=400,
            detail={"error": "Messaging MS validation failed", "downstream": parsed.to_dict()},
        )

    if parsed is None:
        raise HTTPException(502, "Messaging microservice returned no data")

    return parsed.to_dict()
