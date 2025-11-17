from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

import app.services.messaging_repository as repo
from app.utils.db_connection import SessionDep

router = APIRouter(
    prefix="/messaging/thread-users",
    tags=["Messaging Thread User"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_thread_user_relation_endpoint(
    thread_id: str,
    user_id: str,
    session: SessionDep,
):
    relation = await repo.create_thread_user_relation(
        session=session,
        thread_id=thread_id,
        user_id=user_id,
    )
    return relation


@router.get("/{thread_id}/users")
async def get_users_for_thread_endpoint(
    thread_id: str,
    session: SessionDep,
):
    users = await repo.get_thread_users(session, thread_id)
    return {"thread_id": thread_id, "users": users}


@router.get("/user/{user_id}/threads")
async def get_threads_for_user_endpoint(
    user_id: str,
    session: SessionDep,
):
    threads = await repo.get_user_threads(session, user_id)
    return {"user_id": user_id, "threads": threads}


@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thread_user_relations_endpoint(
    thread_id: str,
    session: SessionDep,
):
    await repo.delete_thread_user_relations(session, thread_id)
    return {"message": "Thread-user relations deleted"}
