from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from app.models.dto.address_dto import AddressDTO
from app.models.po.address_user_po import AddressUser # Local relationship model
from app.utils.auth import get_user_id_from_token
from app.utils.config import get_address_client
from app.utils.db_connection import SessionDep

# Downstream Client Imports (Check your files for exact names)
from app.client.user.user_address_api_client.api.default.create_address_addresses_post import (
    asyncio as create_address_async
)
from app.client.user.user_address_api_client.models.address_create import AddressCreate


security = HTTPBearer()

address_user_router = APIRouter(
    tags=["Address User"]
)

@address_user_router.post("/me/addresses", response_model=AddressDTO)
async def create_my_address(
    payload: AddressDTO,
    session: SessionDep,
    token: HTTPAuthorizationCredentials = Depends(security),
):
    # 1. Extract User ID from Token
    try:
        token_str = token.credentials
        user_id = get_user_id_from_token(token_str)
        user_uuid = UUID(str(user_id))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")
    

    # 2. Create Address Downstream (without user_id)
    downstream_body = AddressCreate(
        street=payload.street,
        city=payload.city,
        state=payload.state,
        postal_code=payload.postal_code,
        country=payload.country
    )

    result = await create_address_async(
        client=get_address_client(),
        body=downstream_body
    )

    if not result:
        raise HTTPException(status_code=500, detail="Failed to create address downstream")

    # 3. CRITICAL FIX: Link Address to User Locally
    try:
        new_relation = AddressUser(
            user_id=str(user_uuid),
            address_id=str(result.id) 
        )
        session.add(new_relation)
        await session.commit()
        await session.refresh(new_relation)
    except Exception as e:
        print(f"Error linking address: {e}")
        raise HTTPException(status_code=500, detail="Failed to link address to user")

    # 4. Return Result
    return AddressDTO(
        id=result.id,
        street=result.street,
        city=result.city,
        state=getattr(result, "state", None),
        postal_code=getattr(result, "postal_code", None),
        country=result.country
    )
