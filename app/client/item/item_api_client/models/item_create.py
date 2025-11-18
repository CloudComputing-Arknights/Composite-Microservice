from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.condition_type import ConditionType
from ..models.transaction_type import TransactionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ItemCreate")


@_attrs_define
class ItemCreate:
    """Creation payload for an item and its post.

    Attributes:
        title (str): Title of the post of the item
        condition (ConditionType):
        transaction_type (TransactionType):
        price (float): Price of the item must be greater than 0.
        description (None | str | Unset): Description of the item in the post.
        address_uuid (None | Unset | UUID): The UUID of position for transaction chosen from user's address lists, can
            be online or a physical place,
        image_urls (list[str] | Unset): The list of URL images of the post
        category_ids (list[UUID] | None | Unset): List of Category IDs to associate with this item.
    """

    title: str
    condition: ConditionType
    transaction_type: TransactionType
    price: float
    description: None | str | Unset = UNSET
    address_uuid: None | Unset | UUID = UNSET
    image_urls: list[str] | Unset = UNSET
    category_ids: list[UUID] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        condition = self.condition.value

        transaction_type = self.transaction_type.value

        price = self.price

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

        category_ids: list[str] | None | Unset
        if isinstance(self.category_ids, Unset):
            category_ids = UNSET
        elif isinstance(self.category_ids, list):
            category_ids = []
            for category_ids_type_0_item_data in self.category_ids:
                category_ids_type_0_item = str(category_ids_type_0_item_data)
                category_ids.append(category_ids_type_0_item)

        else:
            category_ids = self.category_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "condition": condition,
                "transaction_type": transaction_type,
                "price": price,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if address_uuid is not UNSET:
            field_dict["address_UUID"] = address_uuid
        if image_urls is not UNSET:
            field_dict["image_urls"] = image_urls
        if category_ids is not UNSET:
            field_dict["category_ids"] = category_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        condition = ConditionType(d.pop("condition"))

        transaction_type = TransactionType(d.pop("transaction_type"))

        price = d.pop("price")

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

        def _parse_category_ids(data: object) -> list[UUID] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                category_ids_type_0 = []
                _category_ids_type_0 = data
                for category_ids_type_0_item_data in _category_ids_type_0:
                    category_ids_type_0_item = UUID(category_ids_type_0_item_data)

                    category_ids_type_0.append(category_ids_type_0_item)

                return category_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UUID] | None | Unset, data)

        category_ids = _parse_category_ids(d.pop("category_ids", UNSET))

        item_create = cls(
            title=title,
            condition=condition,
            transaction_type=transaction_type,
            price=price,
            description=description,
            address_uuid=address_uuid,
            image_urls=image_urls,
            category_ids=category_ids,
        )

        item_create.additional_properties = d
        return item_create

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
