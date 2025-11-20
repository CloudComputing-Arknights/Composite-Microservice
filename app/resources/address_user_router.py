from fastapi import APIRouter, HTTPException, Request, Depends
from uuid import UUID

# 1. DTOs
from app.models.dto.address_dto import AddressDTO

# 2. PO (Database Model for the relationship)
from app.models.po.address_user_po import AddressUser

# 3. Utilities
from app.utils.auth import get_user_id_from_token
from app.utils.config import get_address_client
from app.utils.db_connection import SessionDep

# 4. Downstream Client Imports
# Note: Using the correct file names found in previous steps
from app.client.user.user_address_api_client.api.default.create_address_addresses_post import (
    asyncio as create_address_async
)
from app.client.user.user_address_api_client.models.address_create import AddressCreate

address_user_router = APIRouter()

@address_user_router.post("/me/addresses", response_model=AddressDTO)
async def create_my_address(
    payload: AddressDTO,
    request: Request,
    session: SessionDep, # Database session required for linking
):
    # --- A. Verify Token & Get User ID ---
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Token")
    
    try:
        token_str = auth_header.split(" ")[1]
        user_id = get_user_id_from_token(token_str)
        user_uuid = UUID(str(user_id))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")

    # --- B. Create Address Downstream (User Service) ---
    # We do NOT send user_id here because the downstream model doesn't accept it.
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

    # --- C. Link Address to User Locally (CRITICAL STEP) ---
    # Since the downstream service created an "orphan" address, 
    # we must link it to the current user in our local Composite DB.
    try:
        new_relation = AddressUser(
            user_id=str(user_uuid),  # Convert UUID to string for SQLModel
            address_id=str(result.id) # Convert UUID to string for SQLModel
        )
        session.add(new_relation)
        await session.commit()
        await session.refresh(new_relation)
    except Exception as e:
        print(f"Error linking address to user: {e}")
        # In a production environment, you might want to rollback/delete the downstream address here.
        raise HTTPException(status_code=500, detail="Failed to link address to user")

    # --- D. Return the Result ---
    return AddressDTO(
        id=result.id,
        street=result.street,
        city=result.city,
        state=getattr(result, "state", None),
        postal_code=getattr(result, "postal_code", None),
        country=result.country
    )