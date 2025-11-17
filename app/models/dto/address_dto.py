from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AddressDTO(BaseModel):
    id: Optional[UUID] = None

    street: str
    city: str
    country: str

    state: Optional[str] = None
    postal_code: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None