from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional

from app.models.po.transaction_item_po import TransactionItem, ItemRole

# Transaction-Item: Many-to-Many

async def create_transaction_item_relation(
        session: AsyncSession,
        transaction_id: str,
        item_id: str,
        item_role: ItemRole,
) -> TransactionItem:
    transaction_item = TransactionItem(transaction_id=transaction_id, item_id=item_id, item_role=item_role)
    session.add(transaction_item)
    await session.commit()
    await session.refresh(transaction_item)
    return transaction_item


async def get_transaction_items(
        session: AsyncSession,
        transaction_id: str,
        item_role: Optional[ItemRole] = None,
) -> list[str]:
    statement = select(TransactionItem).where(TransactionItem.transaction_id == transaction_id)
    if item_role is not None:
        statement = statement.where(TransactionItem.item_role == item_role)
    result = await session.exec(statement)
    links = result.all()
    return [link.item_id for link in links]


async def get_item_transactions(
        session: AsyncSession,
        item_id: str,
        item_role: Optional[ItemRole] = None,
) -> list[str]:
    statement = select(TransactionItem).where(TransactionItem.item_id == item_id)
    if item_role is not None:
        statement = statement.where(TransactionItem.item_role == item_role)
    result = await session.exec(statement)
    links = result.all()
    return [link.transaction_id for link in links]


async def delete_transaction_item_relation(
        session: AsyncSession,
        transaction_id: str,
) -> None:
    statement = select(TransactionItem).where(TransactionItem.transaction_id == transaction_id)
    result = await session.exec(statement)
    link = result.first()
    if not link:
        raise HTTPException(status_code=404, detail="Transaction-Item relation not found")
    await session.delete(link)
    await session.commit()


async def verify_transaction_item_link(
        session: AsyncSession,
        transaction_id: str,
        item_id: str,
        item_role: ItemRole,
) -> bool:
    statement = select(TransactionItem).where(
        TransactionItem.transaction_id == transaction_id,
        TransactionItem.item_id == item_id,
        TransactionItem.item_role == item_role,
    )
    result = await session.exec(statement)
    link = result.first()
    return link is not None
