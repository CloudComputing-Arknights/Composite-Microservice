from sqlmodel import SQLModel, Field
from typing import Optional

class AddressBase(SQLModel):
    street: str
    city: str
    country: str

class AddressCreate(AddressBase):
    pass

class AddressUpdate(SQLModel):
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class AddressResponse(AddressBase):
    id: str