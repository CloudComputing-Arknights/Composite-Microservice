from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

from app.client.item.item_api_client.models.item_create import ItemCreate as ClientItemCreate
from app.client.item.item_api_client.models.item_update import ItemUpdate as ClientItemUpdate
from app.client.item.item_api_client.types import UNSET


# ====================== ConditionType ======================
class ConditionType(str, Enum):
    BRAND_NEW = "BRAND_NEW"
    GOOD = "GOOD"
    LIKE_NEW = "LIKE_NEW"
    POOR = "POOR"

    def __str__(self) -> str:
        return str(self.value)


# ====================== TransactionType ======================
class TransactionType(str, Enum):
    RENT = "RENT"
    SALE = "SALE"

    def __str__(self) -> str:
        return str(self.value)


# ====================== CategoryRead ======================
class CategoryRead(BaseModel):
    """Representation of a Category returned from the server."""
    model_config = ConfigDict(extra="allow")

    name: str
    category_id: int
    description: Optional[str] = None


# ====================== Item ======================
# ====================== ItemBase ======================
class ItemBase(BaseModel):
    title: str
    condition: ConditionType
    transaction_type: TransactionType
    price: float

    description: Optional[str] = None
    address_UUID: Optional[UUID] = Field(default=None)
    image_urls: Optional[List[str]] = None


# ====================== ItemRead ======================
class ItemRead(ItemBase):
    """Server representation returned to clients."""
    model_config = ConfigDict(extra="allow")

    item_UUID: UUID
    categories: Optional[List[CategoryRead]] = Field(default=None)
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


# ====================== ItemCreate ======================
class ItemCreate(ItemBase):
    model_config = ConfigDict(extra="allow")

    category_ids: Optional[List[int]] = Field(default=None)

    def to_client_model(self) -> ClientItemCreate:
        return ClientItemCreate(
            title=self.title,
            condition=self.condition,
            transaction_type=self.transaction_type,
            price=self.price,
            description=self.description if self.description is not None else UNSET,
            address_uuid=self.address_UUID if self.address_UUID is not None else UNSET,
            image_urls=self.image_urls if self.image_urls is not None else UNSET,
            category_ids=self.category_ids if self.category_ids is not None else UNSET,
        )

# ====================== ItemUpdate ======================
class ItemUpdate(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: Optional[str] = None
    condition: Optional[ConditionType] = None
    transaction_type: Optional[TransactionType] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category_ids: Optional[List[int]] = None
    address_UUID: Optional[UUID] = None
    image_urls: Optional[List[str]] = None

    def to_client_model(self) -> ClientItemUpdate:
        return ClientItemUpdate(
            title=self.title if self.title is not None else UNSET,
            condition=self.condition if self.condition is not None else UNSET,
            transaction_type=self.transaction_type if self.transaction_type is not None else UNSET,
            price=self.price if self.price is not None else UNSET,
            description=self.description if self.description is not None else UNSET,
            address_uuid=self.address_UUID if self.address_UUID is not None else UNSET,
            image_urls=self.image_urls if self.image_urls is not None else UNSET,
            category_ids=self.category_ids if self.category_ids is not None else UNSET,
        )