from fastapi import status
from fastapi.exceptions import HTTPException
from uuid import UUID
import logging

from app.client.user.user_address_api_client.api.default import (
    get_address_addresses_address_id_get,
    get_user_users_user_id_get
)
from app.client.item.item_api_client.models import HTTPValidationError
from app.models.dto.item_dto import (
    ItemRead,
)
from app.services.item_user_repository import get_item_owner
from app.utils.db_connection import SessionDep


log = logging.getLogger(__name__)


async def complete_item(
        item_obj,
        user_id: UUID,
        client,
) -> ItemRead:
    """
    Insert address and user information into ItemRead
    Args:
        item_obj:   client attrs model
        user_id:    id for user of the item
        client:     client for address and user

    Returns:        ItemRead pydantic model
    """
    item_dict = item_obj.to_dict()
    addr_id = item_dict.get("address_UUID")

    # Insert address information
    if addr_id:
        address_response = await get_address_addresses_address_id_get.asyncio(
            address_id=UUID(str(addr_id)),
            client=client
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

    # Insert user information
    if user_id:
        user_response = await get_user_users_user_id_get.asyncio(
            user_id=user_id,
            client=client
        )
        if isinstance(user_response, HTTPValidationError):
            log.error(
                "Downstream 'user service' validation failed. Response: %s",
                user_response.to_dict()
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred."
            )
        if user_response is not None:
            item_dict["user"] = user_response.to_dict()

    return ItemRead(**item_dict)