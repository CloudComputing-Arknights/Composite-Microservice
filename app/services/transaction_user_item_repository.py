from typing import Optional

from fastapi import HTTPException
from sqlmodel import select, or_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.po.transaction_user_item_po import TransactionUserItem

# Transaction-User-Item: Manages relationships between transactions, users, and items


async def create_transaction_user_item_relation(
    session: AsyncSession,
    transaction_id: str,
    initiator_user_id: str,
    receiver_user_id: str,
    requested_item_id: str,
    offered_item_id: Optional[str] = None,
) -> TransactionUserItem:
    """Create a new transaction-user-item relation."""
    relation = TransactionUserItem(
        transaction_id=transaction_id,
        initiator_user_id=initiator_user_id,
        receiver_user_id=receiver_user_id,
        requested_item_id=requested_item_id,
        offered_item_id=offered_item_id,
    )
    session.add(relation)
    await session.commit()
    await session.refresh(relation)
    return relation


async def get_transaction_relation(
    session: AsyncSession,
    transaction_id: str,
) -> TransactionUserItem:
    """Get transaction relation by transaction_id."""
    statement = select(TransactionUserItem).where(
        TransactionUserItem.transaction_id == transaction_id
    )
    result = await session.exec(statement)
    relation = result.first()
    if not relation:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return relation


async def get_user_transactions(
    session: AsyncSession,
    user_id: str,
) -> list[TransactionUserItem]:
    """Get all transactions where user is either initiator or receiver."""
    statement = select(TransactionUserItem).where(
        or_(
            TransactionUserItem.initiator_user_id == user_id,
            TransactionUserItem.receiver_user_id == user_id
        )
    )
    result = await session.exec(statement)
    return result.all()


async def get_transactions_by_item(
    session: AsyncSession,
    item_id: str,
) -> list[TransactionUserItem]:
    """Get all transactions involving a specific item."""
    statement = select(TransactionUserItem).where(
        or_(
            TransactionUserItem.requested_item_id == item_id,
            TransactionUserItem.offered_item_id == item_id
        )
    )
    result = await session.exec(statement)
    return result.all()


async def verify_transaction_participant(
    session: AsyncSession,
    transaction_id: str,
    user_id: str,
) -> bool:
    """Check if user is a participant (initiator or receiver) in the transaction."""
    statement = select(TransactionUserItem).where(
        TransactionUserItem.transaction_id == transaction_id,
        or_(
            TransactionUserItem.initiator_user_id == user_id,
            TransactionUserItem.receiver_user_id == user_id
        )
    )
    result = await session.exec(statement)
    relation = result.first()
    return relation is not None


async def verify_transaction_initiator(
    session: AsyncSession,
    transaction_id: str,
    user_id: str,
) -> bool:
    """Check if user is the initiator of the transaction."""
    statement = select(TransactionUserItem).where(
        TransactionUserItem.transaction_id == transaction_id,
        TransactionUserItem.initiator_user_id == user_id
    )
    result = await session.exec(statement)
    relation = result.first()
    return relation is not None


async def verify_transaction_receiver(
    session: AsyncSession,
    transaction_id: str,
    user_id: str,
) -> bool:
    """Check if user is the receiver of the transaction."""
    statement = select(TransactionUserItem).where(
        TransactionUserItem.transaction_id == transaction_id,
        TransactionUserItem.receiver_user_id == user_id
    )
    result = await session.exec(statement)
    relation = result.first()
    return relation is not None


async def delete_transaction_relation(
    session: AsyncSession,
    transaction_id: str,
) -> None:
    """Delete transaction relation by transaction_id."""
    statement = select(TransactionUserItem).where(
        TransactionUserItem.transaction_id == transaction_id
    )
    result = await session.exec(statement)
    relation = result.first()
    if not relation:
        raise HTTPException(status_code=404, detail="Transaction relation not found")
    
    await session.delete(relation)
    await session.commit()
