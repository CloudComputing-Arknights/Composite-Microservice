from fastapi import APIRouter, HTTPException, status, Request
from app.utils.db_connection import SessionDep

from app.services.message_repository import (
    create_thread_user_relation,
    get_thread_users,
    get_user_threads,
    delete_thread_user_relations,
)
from app.models.dto.thread_user_dto import MessagingThreadDto


message_user_router = APIRouter(prefix="/messaging/thread-users", tags=["Messaging Thread User"])


@message_user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_thread_user_relation_endpoint(
    request: Request,
    thread_id: str,
    user_id: str,
    session: SessionDep,
):
    current_user_id = request.state.user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You may only add yourself to a thread"
        )

    relation = await create_thread_user_relation(
        session=session,
        thread_id=thread_id,
        user_id=user_id,
    )

    dto = MessagingThreadDto(
        thread_id=relation.thread_id,
        author_id=None, 
        participant_id=relation.user_id,
        created_at=str(relation.created_at),
        updated_at=str(relation.updated_at)
    )

    return dto

@message_user_router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thread_user_relations_endpoint(
    request: Request,
    thread_id: str,
    session: SessionDep,
):
    current_user_id = request.state.user_id

    users = await get_thread_users(session, thread_id)

    if current_user_id not in users:
        raise HTTPException(status_code=403, detail="Access denied")

    await delete_thread_user_relations(session, thread_id)

    return {"message": "Thread-user relations deleted"}
