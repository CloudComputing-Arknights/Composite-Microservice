from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.models.po.transaction_item_po import TransactionItem


async def create_transaction_item_relation(
        transaction_id: str,
        item_id: str,
        session: AsyncSession
) -> TransactionItem:
    transaction_item = TransactionItem(transaction_id=transaction_id, item_id=item_id)
    session.add(transaction_item)
    await session.commit()
    await session.refresh(transaction_item)
    return transaction_item


async def get_transaction_items(transaction_id: str, session: AsyncSession) -> List[str]:
    statement = select(TransactionItem).where(TransactionItem.transaction_id == transaction_id)
    result = await session.exec(statement)
    links = result.all()
    return [link.item_id for link in links]


async def get_item_transactions(item_id: str, session: AsyncSession) -> List[str]:
    statement = select(TransactionItem).where(TransactionItem.item_id == item_id)
    result = await session.exec(statement)
    links = result.all()
    return [link.transaction_id for link in links]


async def delete_transaction_item_relation(transaction_id: str, session: AsyncSession) -> None:
    statement = select(TransactionItem).where(TransactionItem.transaction_id == transaction_id)
    result = await session.exec(statement)
    link = result.first()
    if not link:
        raise HTTPException(status_code=404, detail="Transaction-Item relation not found")
    await session.delete(link)
    await session.commit()


async def verify_transaction_item_link(
        transaction_id: str,
        item_id: str,
        session: AsyncSession
) -> bool:
    statement = select(TransactionItem).where(
        TransactionItem.transaction_id == transaction_id,
        TransactionItem.item_id == item_id
    )
    result = await session.exec(statement)
    link = result.first()
    return link is not None
