from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.po.messaging_thread_user_po import MessagingThreadUser


async def create_thread_user_relation(
        session: AsyncSession,
        thread_id: str,
        user_id: str,
) -> MessagingThreadUser:

    relation = MessagingThreadUser(thread_id=thread_id, user_id=user_id)
    session.add(relation)
    await session.commit()
    await session.refresh(relation)
    return relation


async def get_thread_users(
        session: AsyncSession,
        thread_id: str,
) -> list[str]:

    statement = select(MessagingThreadUser).where(
        MessagingThreadUser.thread_id == thread_id
    )
    result = await session.exec(statement)
    relations = result.all()

    if not relations:
        raise HTTPException(status_code=404, detail="No users found for this thread")

    return [rel.user_id for rel in relations]

async def get_user_threads(
        session: AsyncSession,
        user_id: str,
) -> list[str]:

    statement = select(MessagingThreadUser).where(
        MessagingThreadUser.user_id == user_id
    )
    result = await session.exec(statement)
    relations = result.all()

    return [rel.thread_id for rel in relations]

