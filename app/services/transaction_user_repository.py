from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.models.po.transaction_user_po import TransactionUser


async def create_transaction_user_relation(
        transaction_id: str,
        user_id: str,
        session: AsyncSession
) -> TransactionUser:
    transaction_user = TransactionUser(transaction_id=transaction_id, user_id=user_id)
    session.add(transaction_user)
    await session.commit()
    await session.refresh(transaction_user)
    return transaction_user


async def get_transaction_users(transaction_id: str, session: AsyncSession) -> List[str]:
    statement = select(TransactionUser).where(TransactionUser.transaction_id == transaction_id)
    result = await session.exec(statement)
    links = result.all()
    return [link.user_id for link in links]


async def get_user_transactions(user_id: str, session: AsyncSession) -> List[str]:
    statement = select(TransactionUser).where(TransactionUser.user_id == user_id)
    result = await session.exec(statement)
    links = result.all()
    return [link.transaction_id for link in links]


async def delete_transaction_user_relation(transaction_id: str, session: AsyncSession) -> None:
    statement = select(TransactionUser).where(TransactionUser.transaction_id == transaction_id)
    result = await session.exec(statement)
    link = result.first()
    if not link:
        raise HTTPException(status_code=404, detail="Transaction-User relation not found")
    await session.delete(link)
    await session.commit()


async def verify_transaction_user_link(
        transaction_id: str,
        user_id: str,
        session: AsyncSession
) -> bool:
    statement = select(TransactionUser).where(
        TransactionUser.transaction_id == transaction_id,
        TransactionUser.user_id == user_id
    )
    result = await session.exec(statement)
    link = result.first()
    return link is not None
