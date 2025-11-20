from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.category_type import CategoryType
from ..models.condition_type import ConditionType
from ..models.transaction_type import TransactionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ItemUpdate")


@_attrs_define
class ItemUpdate:
    """Partial update for an item and its post.

    Attributes:
        title (None | str | Unset): Title of the post of the item
        description (None | str | Unset): Description of the item.
        condition (ConditionType | None | Unset): Condition of the item (ConditionType)
        category (list[CategoryType] | None | Unset): Category of the posted item.
        transaction_type (None | TransactionType | Unset): Type of the transaction can be SALE or RENT.
        price (float | None | Unset): Price of the item must be greater than 0.
        address_uuid (None | Unset | UUID): The position for transaction, can be online or a physical place.
        image_urls (list[str] | None | Unset): The list of URL images of the post
    """

    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    condition: ConditionType | None | Unset = UNSET
    category: list[CategoryType] | None | Unset = UNSET
    transaction_type: None | TransactionType | Unset = UNSET
    price: float | None | Unset = UNSET
    address_uuid: None | Unset | UUID = UNSET
    image_urls: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        condition: None | str | Unset
        if isinstance(self.condition, Unset):
            condition = UNSET
        elif isinstance(self.condition, ConditionType):
            condition = self.condition.value
        else:
            condition = self.condition

        category: list[str] | None | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        elif isinstance(self.category, list):
            category = []
            for category_type_0_item_data in self.category:
                category_type_0_item = category_type_0_item_data.value
                category.append(category_type_0_item)

        else:
            category = self.category

        transaction_type: None | str | Unset
        if isinstance(self.transaction_type, Unset):
            transaction_type = UNSET
        elif isinstance(self.transaction_type, TransactionType):
            transaction_type = self.transaction_type.value
        else:
            transaction_type = self.transaction_type

        price: float | None | Unset
        if isinstance(self.price, Unset):
            price = UNSET
        else:
            price = self.price

        address_uuid: None | str | Unset
        if isinstance(self.address_uuid, Unset):
            address_uuid = UNSET
        elif isinstance(self.address_uuid, UUID):
            address_uuid = str(self.address_uuid)
        else:
            address_uuid = self.address_uuid

        image_urls: list[str] | None | Unset
        if isinstance(self.image_urls, Unset):
            image_urls = UNSET
        elif isinstance(self.image_urls, list):
            image_urls = self.image_urls

        else:
            image_urls = self.image_urls

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if condition is not UNSET:
            field_dict["condition"] = condition
        if category is not UNSET:
            field_dict["category"] = category
        if transaction_type is not UNSET:
            field_dict["transaction_type"] = transaction_type
        if price is not UNSET:
            field_dict["price"] = price
        if address_uuid is not UNSET:
            field_dict["address_UUID"] = address_uuid
        if image_urls is not UNSET:
            field_dict["image_urls"] = image_urls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_condition(data: object) -> ConditionType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                condition_type_0 = ConditionType(data)

                return condition_type_0
            except:  # noqa: E722
                pass
            return cast(ConditionType | None | Unset, data)

        condition = _parse_condition(d.pop("condition", UNSET))

        def _parse_category(data: object) -> list[CategoryType] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                category_type_0 = []
                _category_type_0 = data
                for category_type_0_item_data in _category_type_0:
                    category_type_0_item = CategoryType(category_type_0_item_data)

                    category_type_0.append(category_type_0_item)

                return category_type_0
            except:  # noqa: E722
                pass
            return cast(list[CategoryType] | None | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        def _parse_transaction_type(data: object) -> None | TransactionType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                transaction_type_type_0 = TransactionType(data)

                return transaction_type_type_0
            except:  # noqa: E722
                pass
            return cast(None | TransactionType | Unset, data)

        transaction_type = _parse_transaction_type(d.pop("transaction_type", UNSET))

        def _parse_price(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        price = _parse_price(d.pop("price", UNSET))

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
            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        address_uuid = _parse_address_uuid(d.pop("address_UUID", UNSET))

        def _parse_image_urls(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                image_urls_type_0 = cast(list[str], data)

                return image_urls_type_0
            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        image_urls = _parse_image_urls(d.pop("image_urls", UNSET))

        item_update = cls(
            title=title,
            description=description,
            condition=condition,
            category=category,
            transaction_type=transaction_type,
            price=price,
            address_uuid=address_uuid,
            image_urls=image_urls,
        )

        item_update.additional_properties = d
        return item_update

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
