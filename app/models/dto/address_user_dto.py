from typing import List

from pydantic import BaseModel

from .user_dto import UserDTO
from .address_dto import AddressDTO


class AddressUserDTO(BaseModel):
    """
    Example DTO if you ever need to return a 'user + addresses'
    payload explicitly from some composite endpoint.
    """
    user: UserDTO
    addresses: List[AddressDTO]