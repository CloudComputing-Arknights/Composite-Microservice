from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_base import AddressBase


T = TypeVar("T", bound="UserCreate")


@_attrs_define
class UserCreate:
    """Creation payload for a User.

    Attributes:
        username (str): Unique handle for the user. Example: alice.
        email (str): Primary email address. Example: alice@example.com.
        phone (None | str | Unset): Contact phone number. Example: +1-212-555-0199.
        birth_date (datetime.date | None | Unset): Date of birth (YYYY-MM-DD). Example: 2000-09-01.
        addresses (list[AddressBase] | Unset): Addresses linked to this user (each has a persistent Address ID).
            Example: [{'city': 'New York', 'country': 'USA', 'id': '550e8400-e29b-41d4-a716-446655440000', 'postal_code':
            '10001', 'state': 'NY', 'street': '123 Main St'}].
    """

    username: str
    email: str
    phone: None | str | Unset = UNSET
    birth_date: datetime.date | None | Unset = UNSET
    addresses: list[AddressBase] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        email = self.email

        phone: None | str | Unset
        if isinstance(self.phone, Unset):
            phone = UNSET
        else:
            phone = self.phone

        birth_date: None | str | Unset
        if isinstance(self.birth_date, Unset):
            birth_date = UNSET
        elif isinstance(self.birth_date, datetime.date):
            birth_date = self.birth_date.isoformat()
        else:
            birth_date = self.birth_date

        addresses: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.addresses, Unset):
            addresses = []
            for addresses_item_data in self.addresses:
                addresses_item = addresses_item_data.to_dict()
                addresses.append(addresses_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "email": email,
            }
        )
        if phone is not UNSET:
            field_dict["phone"] = phone
        if birth_date is not UNSET:
            field_dict["birth_date"] = birth_date
        if addresses is not UNSET:
            field_dict["addresses"] = addresses

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_base import AddressBase

        d = dict(src_dict)
        username = d.pop("username")

        email = d.pop("email")

        def _parse_phone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        phone = _parse_phone(d.pop("phone", UNSET))

        def _parse_birth_date(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                birth_date_type_0 = isoparse(data).date()

                return birth_date_type_0
            except:  # noqa: E722
                pass
            return cast(datetime.date | None | Unset, data)

        birth_date = _parse_birth_date(d.pop("birth_date", UNSET))

        addresses = []
        _addresses = d.pop("addresses", UNSET)
        for addresses_item_data in _addresses or []:
            addresses_item = AddressBase.from_dict(addresses_item_data)

            addresses.append(addresses_item)

        user_create = cls(
            username=username,
            email=email,
            phone=phone,
            birth_date=birth_date,
            addresses=addresses,
        )

        user_create.additional_properties = d
        return user_create

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
