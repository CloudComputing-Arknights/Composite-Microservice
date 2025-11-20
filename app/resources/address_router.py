from fastapi import APIRouter, HTTPException, Request
from uuid import UUID

from app.models.dto.address_dto import AddressDTO
# Import the Update model for address updates
from app.client.user.user_address_api_client.models.address_update import AddressUpdate

# Downstream Client Import
from app.client.user.user_address_api_client.api.default.update_address_addresses_address_id_put import (
    asyncio as update_address_async
)
from app.utils.config import get_address_client

from app.client.user.user_address_api_client.api.default.delete_address_addresses_address_id_delete import (
    asyncio as delete_address_async
)
from app.utils.config import get_address_client

address_router = APIRouter()

@address_router.put("/addresses/{address_id}", response_model=AddressDTO)
async def update_address(
    address_id: UUID,
    payload: AddressDTO,
    request: Request
):
    # 1. Verify Token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Token")
    
    # 2. Prepare body for downstream service
    downstream_body = AddressUpdate(
        street=payload.street,
        city=payload.city,
        state=payload.state,
        postal_code=payload.postal_code,
        country=payload.country
    )

    # 3. Call downstream service
    result = await update_address_async(
        client=get_address_client(),
        address_id=address_id,
        body=downstream_body
    )

    if not result:
        raise HTTPException(status_code=500, detail="Failed to update address downstream")

    # 4. Return updated address
    return AddressDTO(
        id=result.id,
        street=result.street,
        city=result.city,
        state=getattr(result, "state", None),
        postal_code=getattr(result, "postal_code", None),
        country=result.country
    )

@address_router.delete("/addresses/{address_id}")
async def delete_address(
    address_id: UUID,
    request: Request
):
    # 1. Verify Token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Token")
    
    # 2. Call Downstream Service
    response = await delete_address_async(
        client=get_address_client(),
        address_id=address_id
    )
    
    # Return success message
    return {"message": "Address deleted successfully"}