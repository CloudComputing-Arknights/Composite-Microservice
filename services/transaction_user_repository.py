from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from models.po.transaction_user_po import TransactionUser


async def create_transaction_user_relation(
        transaction_id: str,
        user_id: int,
        session: AsyncSession
) -> TransactionUser:
    transaction_user = TransactionUser(transaction_id=transaction_id, user_id=user_id)
    session.add(transaction_user)
    await session.commit()
    await session.refresh(transaction_user)
    return transaction_user


async def get_transaction_owner(transaction_id: str, session: AsyncSession) -> str:
    statement = select(TransactionUser).where(TransactionUser.transaction_id == transaction_id)
    result = await session.exec(statement)
    transaction_user = result.first()
    if not transaction_user:
        raise HTTPException(status_code=404, detail="Transaction owner not found")
    return transaction_user.user_id


async def get_user_transactions(user_id: int, session: AsyncSession) -> List[str]:
    statement = select(TransactionUser).where(TransactionUser.user_id == user_id)
    result = await session.exec(statement)
    transaction_users = result.all()
    return [tu.transaction_id for tu in transaction_users]


async def delete_transaction_user_relation(transaction_id: str, session: AsyncSession) -> None:
    statement = select(TransactionUser).where(TransactionUser.transaction_id == transaction_id)
    result = await session.exec(statement)
    transaction_user = result.first()
    if not transaction_user:
        raise HTTPException(status_code=404, detail="Transaction-User relation not found")
    await session.delete(transaction_user)
    await session.commit()


async def verify_transaction_ownership(
        transaction_id: str,
        user_id: str,
        session: AsyncSession
) -> bool:
    statement = select(TransactionUser).where(
        TransactionUser.transaction_id == transaction_id,
        TransactionUser.user_id == user_id
    )
    result = await session.exec(statement)
    transaction_user = result.first()
    return transaction_user is not None
