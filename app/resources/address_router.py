from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse
from app.services.address_service import (
    get_all_addresses,
    get_address_by_id,
    create_address,
    update_address,
    delete_address
)

address_router = APIRouter(prefix="/addresses", tags=["Addresses"])


@address_router.get("/", response_model=List[AddressResponse])
async def list_addresses(skip: int = 0, limit: int = 20):
    addresses = await get_all_addresses(skip=skip, limit=limit)
    return addresses


@address_router.get("/{address_id}", response_model=AddressResponse)
async def get_address(address_id: str):
    address = await get_address_by_id(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@address_router.post("/", response_model=AddressResponse)
async def create_new_address(payload: AddressCreate):
    return await create_address(payload)


@address_router.patch("/{address_id}", response_model=AddressResponse)
async def update_existing_address(address_id: str, payload: AddressUpdate):
    updated = await update_address(address_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated


@address_router.delete("/{address_id}")
async def delete_existing_address(address_id: str):
    success = await delete_address(address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"detail": "Address deleted successfully"}