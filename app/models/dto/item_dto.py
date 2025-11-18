from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator
from enum import Enum


# -------------------------
# ConditionType
# -------------------------
class ConditionType(str, Enum):
    BRAND_NEW = "BRAND_NEW"
    GOOD = "GOOD"
    LIKE_NEW = "LIKE_NEW"
    POOR = "POOR"

    def __str__(self) -> str:
        return str(self.value)


# -------------------------
# TransactionType
# -------------------------
class TransactionType(str, Enum):
    RENT = "RENT"
    SALE = "SALE"

    def __str__(self) -> str:
        return str(self.value)


# -------------------------
# CategoryRead
# -------------------------
class CategoryRead(BaseModel):
    """Representation of a Category returned from the server."""
    model_config = ConfigDict(extra="allow")

    name: str
    id: UUID
    description: Optional[str] = None



# -------------------------
# ItemRead
# -------------------------
class ItemRead(BaseModel):
    """Server representation returned to clients."""
    model_config = ConfigDict(extra="allow")

    title: str
    condition: ConditionType
    transaction_type: TransactionType
    price: float
    item_uuid: UUID = Field(alias="item_UUID")

    description: Optional[str] = None
    categories_uuid: Optional[List[CategoryRead]] = Field(default=None, alias="categories")
    address_uuid: Optional[UUID] = Field(default=None, alias="address_UUID")
    image_urls: Optional[List[str]] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    # ---- validators (Pydantic v2 syntax) ----

    @field_validator("created_at", "updated_at", mode="before")
    def parse_datetime(cls, v):
        if v is None:
            return None
        if isinstance(v, datetime.datetime):
            return v
        # handle ISO8601 with Z suffix
        return datetime.datetime.fromisoformat(v.replace("Z", "+00:00"))


    @field_validator("address_uuid", mode="before")
    def parse_uuid(cls, v):
        if v is None:
            return None
        if isinstance(v, UUID):
            return v
        return UUID(v)

    # def to_dict(self) -> Dict[str, Any]:
    #     return self.model_dump(
    #         by_alias=True,
    #         exclude_none=True,
    #     )
