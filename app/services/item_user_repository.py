from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.models.po.item_user_po import ItemUser


async def create_item_user_relation(
        item_id: str,
        user_id: str,
        session: AsyncSession
) -> ItemUser:
    item_user = ItemUser(item_id=item_id, user_id=user_id)
    session.add(item_user)
    await session.commit()
    await session.refresh(item_user)
    return item_user


async def get_item_owner(item_id: str, session: AsyncSession) -> str:
    statement = select(ItemUser).where(ItemUser.item_id == item_id)
    result = await session.exec(statement)
    item_user = result.first()
    if not item_user:
        raise HTTPException(status_code=404, detail="Item owner not found")
    return item_user.user_id


async def get_user_items(user_id: str, session: AsyncSession) -> List[str]:
    statement = select(ItemUser).where(ItemUser.user_id == user_id)
    result = await session.exec(statement)
    item_users = result.all()
    return [item_user.item_id for item_user in item_users]


async def delete_item_user_relation(item_id: str, session: AsyncSession) -> None:
    statement = select(ItemUser).where(ItemUser.item_id == item_id)
    result = await session.exec(statement)
    item_user = result.first()
    if not item_user:
        raise HTTPException(status_code=404, detail="Item-User relation not found")
    await session.delete(item_user)
    await session.commit()


async def verify_item_ownership(
        item_id: str,
        user_id: str,
        session: AsyncSession
) -> bool:
    statement = select(ItemUser).where(
        ItemUser.item_id == item_id,
        ItemUser.user_id == user_id
    )
    result = await session.exec(statement)
    item_user = result.first()
    return item_user is not None
