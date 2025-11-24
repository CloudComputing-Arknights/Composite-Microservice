from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.po.item_user_po import ItemUser

# Item-User: Many-to-One

async def create_item_user_relation(
        session: AsyncSession,
        item_id: str,
        user_id: str,
) -> ItemUser:
    item_user = ItemUser(item_id=item_id, user_id=user_id)
    session.add(item_user)
    await session.commit()
    await session.refresh(item_user)
    return item_user


async def get_item_owner(
        session: AsyncSession,
        item_id: str,
) -> str:
    statement = select(ItemUser).where(ItemUser.item_id == item_id)
    result = await session.exec(statement)
    item_user = result.first()
    if not item_user:
        raise HTTPException(status_code=404, detail="Item owner not found")
    return item_user.user_id


async def get_user_items(
        session: AsyncSession,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
) -> list[str]:
    statement = (
        select(ItemUser)
        .where(ItemUser.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = await session.exec(statement)
    item_users = result.all()
    return [item_user.item_id for item_user in item_users]


async def delete_item_user_relation(
        session: AsyncSession,
        item_id: str,
) -> None:
    statement = select(ItemUser).where(ItemUser.item_id == item_id)
    result = await session.exec(statement)
    item_user = result.first()
    if not item_user:
        raise HTTPException(status_code=404, detail="Item-User relation not found")
    await session.delete(item_user)
    await session.commit()


async def verify_item_ownership(
        session: AsyncSession,
        item_id: str,
        user_id: str,
) -> bool:
    statement = select(ItemUser).where(
        ItemUser.item_id == item_id,
        ItemUser.user_id == user_id
    )
    result = await session.exec(statement)
    item_user = result.first()
    return item_user is not None
