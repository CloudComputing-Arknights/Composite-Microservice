from typing import Optional

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.po.transaction_user_item_po import TransactionUserItem, Role

# Transaction-User-Item: Many-to-Many (transaction<->user)

async def create_transaction_user_item_relation(
    session: AsyncSession,
    transaction_id: str,
    user_id: str,
    role: Role,
    item_id: Optional[str] = None,
) -> TransactionUserItem:
    relation = TransactionUserItem(
        transaction_id=transaction_id,
        user_id=user_id,
        item_id=item_id,
        role=role,
    )
    session.add(relation)
    await session.commit()
    await session.refresh(relation)
    return relation


async def get_transaction_user_item_relations(
    session: AsyncSession,
    transaction_id: Optional[str] = None,
    user_id: Optional[str] = None,
    item_id: Optional[str] = None,
) -> list[TransactionUserItem]:
    conditions = []
    if transaction_id is not None:
        conditions.append(TransactionUserItem.transaction_id == transaction_id)
    if user_id is not None:
        conditions.append(TransactionUserItem.user_id == user_id)
    if item_id is not None:
        conditions.append(TransactionUserItem.item_id == item_id)

    statement = select(TransactionUserItem)
    if conditions:
        statement = statement.where(*conditions)

    result = await session.exec(statement)
    return result.all()


async def delete_transaction_user_item_relation(
    session: AsyncSession,
    transaction_id: str,
    user_id: str,
    role: Role,
    item_id: Optional[str] = None,
) -> None:
    conditions = [
        TransactionUserItem.transaction_id == transaction_id,
        TransactionUserItem.user_id == user_id,
        TransactionUserItem.role == role,
    ]
    if item_id is not None:
        conditions.append(TransactionUserItem.item_id == item_id)

    statement = select(TransactionUserItem).where(*conditions)
    result = await session.exec(statement)
    relation = result.first()
    if not relation:
        raise HTTPException(status_code=404, detail="Transaction-User-Item relation not found")

    await session.delete(relation)
    await session.commit()
