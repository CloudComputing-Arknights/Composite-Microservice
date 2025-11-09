from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.models.po.item_address_po import ItemAddress


async def create_item_address_relation(
        item_id: str,
        address_id: str,
        session: AsyncSession
) -> ItemAddress:
    item_address = ItemAddress(item_id=item_id, address_id=address_id)
    session.add(item_address)
    await session.commit()
    await session.refresh(item_address)
    return item_address


async def get_item_address(item_id: str, session: AsyncSession) -> str:
    statement = select(ItemAddress).where(ItemAddress.item_id == item_id)
    result = await session.exec(statement)
    item_address = result.first()
    if not item_address:
        raise HTTPException(status_code=404, detail="Item address not found")
    return item_address.address_id


async def get_address_items(address_id: str, session: AsyncSession) -> List[str]:
    statement = select(ItemAddress).where(ItemAddress.address_id == address_id)
    result = await session.exec(statement)
    item_addresses = result.all()
    return [item_address.item_id for item_address in item_addresses]


async def delete_item_address_relation(item_id: str, session: AsyncSession) -> None:
    statement = select(ItemAddress).where(ItemAddress.item_id == item_id)
    result = await session.exec(statement)
    item_address = result.first()
    if not item_address:
        raise HTTPException(status_code=404, detail="Item-Address relation not found")
    await session.delete(item_address)
    await session.commit()


async def verify_item_address_relation(
        item_id: str,
        address_id: str,
        session: AsyncSession
) -> bool:
    statement = select(ItemAddress).where(
        ItemAddress.item_id == item_id,
        ItemAddress.address_id == address_id
    )
    result = await session.exec(statement)
    item_address = result.first()
    return item_address is not None
