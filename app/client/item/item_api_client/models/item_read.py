from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.condition_type import ConditionType
from ..models.transaction_type import TransactionType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_read import CategoryRead


T = TypeVar("T", bound="ItemRead")


@_attrs_define
class ItemRead:
    """Server representation returned to clients.

    Attributes:
        title (str): Title of the post of the item
        condition (ConditionType):
        transaction_type (TransactionType):
        price (float): Price of the item must be greater than 0.
        item_uuid (UUID): Server-generated item ID Example: 99999999-9999-4999-8999-999999999999.
        description (None | str | Unset): Description of the item in the post.
        address_uuid (None | Unset | UUID): The UUID of position for transaction chosen from user's address lists, can
            be online or a physical place,
        image_urls (list[str] | Unset): The list of URL images of the post
        categories (list[CategoryRead] | Unset): Categories associated with the item.
        created_at (datetime.datetime | Unset): Creation timestamp (UTC). Example: 2025-02-20T11:22:33Z.
        updated_at (datetime.datetime | Unset): Last update timestamp (UTC). Example: 2025-02-21T13:00:00Z.
    """

    title: str
    condition: ConditionType
    transaction_type: TransactionType
    price: float
    item_uuid: UUID
    description: None | str | Unset = UNSET
    address_uuid: None | Unset | UUID = UNSET
    image_urls: list[str] | Unset = UNSET
    categories: list[CategoryRead] | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        condition = self.condition.value

        transaction_type = self.transaction_type.value

        price = self.price

        item_uuid = str(self.item_uuid)

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        address_uuid: None | str | Unset
        if isinstance(self.address_uuid, Unset):
            address_uuid = UNSET
        elif isinstance(self.address_uuid, UUID):
            address_uuid = str(self.address_uuid)
        else:
            address_uuid = self.address_uuid

        image_urls: list[str] | Unset = UNSET
        if not isinstance(self.image_urls, Unset):
            image_urls = self.image_urls

        categories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "condition": condition,
                "transaction_type": transaction_type,
                "price": price,
                "item_UUID": item_uuid,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if address_uuid is not UNSET:
            field_dict["address_UUID"] = address_uuid
        if image_urls is not UNSET:
            field_dict["image_urls"] = image_urls
        if categories is not UNSET:
            field_dict["categories"] = categories
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_read import CategoryRead

        d = dict(src_dict)
        title = d.pop("title")

        condition = ConditionType(d.pop("condition"))

        transaction_type = TransactionType(d.pop("transaction_type"))

        price = d.pop("price")

        item_uuid = UUID(d.pop("item_UUID"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_address_uuid(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                address_uuid_type_0 = UUID(data)

                return address_uuid_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        address_uuid = _parse_address_uuid(d.pop("address_UUID", UNSET))

        image_urls = cast(list[str], d.pop("image_urls", UNSET))

        _categories = d.pop("categories", UNSET)
        categories: list[CategoryRead] | Unset = UNSET
        if _categories is not UNSET:
            categories = []
            for categories_item_data in _categories:
                categories_item = CategoryRead.from_dict(categories_item_data)

                categories.append(categories_item)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        item_read = cls(
            title=title,
            condition=condition,
            transaction_type=transaction_type,
            price=price,
            item_uuid=item_uuid,
            description=description,
            address_uuid=address_uuid,
            image_urls=image_urls,
            categories=categories,
            created_at=created_at,
            updated_at=updated_at,
        )

        item_read.additional_properties = d
        return item_read

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
