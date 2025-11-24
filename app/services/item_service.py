from fastapi import status
from fastapi.exceptions import HTTPException
from uuid import UUID

from app.client.user.user_address_api_client.api.default import  get_address_addresses_address_id_get
from app.client.item.item_api_client.models import HTTPValidationError
from app.models.dto.item_dto import (
    ItemRead,
)


async def merge_item_with_address(
        item_obj,
        address_client
) -> ItemRead:
    """
    Insert address information into ItemRead
    Args:
        item_obj:           client attrs model
        address_client:     client for address (user)

    Returns:                ItemRead pydantic model

    """
    item_dict = item_obj.to_dict()
    addr_id = item_dict.get("address_UUID")

    if addr_id:
        address_response = await get_address_addresses_address_id_get.asyncio(
            address_id=UUID(str(addr_id)),
            client=address_client
        )

        if isinstance(address_response, HTTPValidationError):
            log.error(
                "Downstream 'user service (address)' validation failed. Response: %s",
                address_response.to_dict()
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred."
            )
        if address_response is not None:
            item_dict["address"] = address_response.to_dict()

    return ItemRead(**item_dict)