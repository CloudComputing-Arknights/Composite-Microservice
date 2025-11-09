from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from models.po.address_user_po import AddressUser


async def create_address_user_relation(
        address_id: str,
        user_id: int,
        session: AsyncSession
) -> AddressUser:
    address_user = AddressUser(address_id=address_id, user_id=user_id)
    session.add(address_user)
    await session.commit()
    await session.refresh(address_user)
    return address_user


async def get_address_owner(address_id: str, session: AsyncSession) -> str:
    statement = select(AddressUser).where(AddressUser.address_id == address_id)
    result = await session.exec(statement)
    address_user = result.first()
    if not address_user:
        raise HTTPException(status_code=404, detail="Address owner not found")
    return address_user.user_id


async def get_user_addresses(user_id: int, session: AsyncSession) -> List[str]:
    statement = select(AddressUser).where(AddressUser.user_id == user_id)
    result = await session.exec(statement)
    address_users = result.all()
    return [address_user.address_id for address_user in address_users]


async def delete_address_user_relation(address_id: str, session: AsyncSession) -> None:
    statement = select(AddressUser).where(AddressUser.address_id == address_id)
    result = await session.exec(statement)
    address_user = result.first()
    if not address_user:
        raise HTTPException(status_code=404, detail="Address-User relation not found")
    await session.delete(address_user)
    await session.commit()


async def verify_address_ownership(
        address_id: str,
        user_id: str,
        session: AsyncSession
) -> bool:
    statement = select(AddressUser).where(
        AddressUser.address_id == address_id,
        AddressUser.user_id == user_id
    )
    result = await session.exec(statement)
    address_user = result.first()
    return address_user is not None
