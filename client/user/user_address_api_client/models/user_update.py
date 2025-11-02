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


T = TypeVar("T", bound="UserUpdate")


@_attrs_define
class UserUpdate:
    """Partial update for a User; supply only fields to change.

    Attributes:
        username (None | str | Unset):  Example: alice_new.
        email (None | str | Unset):  Example: alice@newmail.com.
        phone (None | str | Unset):  Example: +44 20 7946 0958.
        birth_date (datetime.date | None | Unset):  Example: 2000-09-01.
        addresses (list[AddressBase] | None | Unset): Replace the entire set of addresses with this list. Example:
            [{'city': 'London', 'country': 'UK', 'id': 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb', 'postal_code': 'SW1A 2AA',
            'street': '10 Downing St'}].
    """

    username: None | str | Unset = UNSET
    email: None | str | Unset = UNSET
    phone: None | str | Unset = UNSET
    birth_date: datetime.date | None | Unset = UNSET
    addresses: list[AddressBase] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username: None | str | Unset
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
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

        addresses: list[dict[str, Any]] | None | Unset
        if isinstance(self.addresses, Unset):
            addresses = UNSET
        elif isinstance(self.addresses, list):
            addresses = []
            for addresses_type_0_item_data in self.addresses:
                addresses_type_0_item = addresses_type_0_item_data.to_dict()
                addresses.append(addresses_type_0_item)

        else:
            addresses = self.addresses

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if email is not UNSET:
            field_dict["email"] = email
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

        def _parse_username(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        username = _parse_username(d.pop("username", UNSET))

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

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

        def _parse_addresses(data: object) -> list[AddressBase] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                addresses_type_0 = []
                _addresses_type_0 = data
                for addresses_type_0_item_data in _addresses_type_0:
                    addresses_type_0_item = AddressBase.from_dict(addresses_type_0_item_data)

                    addresses_type_0.append(addresses_type_0_item)

                return addresses_type_0
            except:  # noqa: E722
                pass
            return cast(list[AddressBase] | None | Unset, data)

        addresses = _parse_addresses(d.pop("addresses", UNSET))

        user_update = cls(
            username=username,
            email=email,
            phone=phone,
            birth_date=birth_date,
            addresses=addresses,
        )

        user_update.additional_properties = d
        return user_update

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
