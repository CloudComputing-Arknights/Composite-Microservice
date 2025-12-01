from fastapi import APIRouter, status, HTTPException, Request
from app.client.item.item_api_client.models.http_validation_error import HTTPValidationError
from app.utils.db_connection import SessionDep

from app.utils.config import get_messaging_client
from fastapi import Depends

from app.client.message.messaging_microservice_client.api.threads.create_thread_threads_post import \
    asyncio_detailed as create_thread_async_detailed

from app.client.message.messaging_microservice_client.models.thread_create import ThreadCreate

from app.services.message_repository import (
    create_thread_user_relation,
    get_thread_users,
    get_user_threads,
)

thread_router = APIRouter(
    prefix="/messaging/threads",
    tags=["Messaging Threads"]
)


@thread_router.post("/", status_code=201)
async def create_thread(
    request: Request,
    participant_id: str,
    session: SessionDep,
    messaging_client=Depends(get_messaging_client)
):
    current_user_id = request.state.user_id

    body = ThreadCreate(
        author_id=current_user_id,
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
            detail=f"Validation error from messaging service: {parsed.to_dict()}"
        )


    thread_id = parsed.thread_id

    await create_thread_user_relation(session, thread_id, current_user_id)
    await create_thread_user_relation(session, thread_id, participant_id)

    return parsed.to_dict()



@thread_router.get("/me")
async def get_my_threads(
    request: Request,
    session: SessionDep,
):
    current_user_id = request.state.user_id
    threads = await get_user_threads(session, current_user_id)
    return {"user_id": current_user_id, "threads": threads}



@thread_router.get("/{thread_id}/users")
async def get_users_for_thread(
    request: Request,
    thread_id: str,
    session: SessionDep,
):
    current_user_id = request.state.user_id

    users = await get_thread_users(session, thread_id)

    if current_user_id not in users:
        raise HTTPException(status_code=403, detail="Unauthorized access to thread")

    return {"thread_id": thread_id, "users": users}


@thread_router.get("/user/{user_id}/threads")
async def get_threads_for_user(
    request: Request,
    user_id: str,
    session: SessionDep,
):
    current_user_id = request.state.user_id

    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Cannot view other users' threads")

    threads = await get_user_threads(session, user_id)
    return {"user_id": user_id, "threads": threads}
