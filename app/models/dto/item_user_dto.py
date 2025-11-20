from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Any, Dict, List, Optional
from uuid import UUID

from .item_dto import ItemBase, ConditionType, TransactionType


class CreateOwnItemReq(ItemBase):
    """Request body from frontend."""
    model_config = ConfigDict(extra="allow")

    # address_UUID: Optional[UUID] = Field(default=None)
    category_ids: Optional[List[int]] = Field(default=None)


class UpdateOwnItemReq(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: Optional[str] = None
    condition: Optional[ConditionType] = None
    transaction_type: Optional[TransactionType] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category_ids: Optional[List[int]] = None
    address_UUID: Optional[UUID] = None
    image_urls: Optional[List[str]] = None
