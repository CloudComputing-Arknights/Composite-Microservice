from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_base import AddressBase


T = TypeVar("T", bound="UserRead")


@_attrs_define
class UserRead:
    """Server representation returned to clients.

    Attributes:
        username (str): Unique handle for the user. Example: alice.
        email (str): Primary email address. Example: alice@example.com.
        phone (None | str | Unset): Contact phone number. Example: +1-212-555-0199.
        birth_date (datetime.date | None | Unset): Date of birth (YYYY-MM-DD). Example: 2000-09-01.
        addresses (list[AddressBase] | Unset): Addresses linked to this user (each has a persistent Address ID).
            Example: [{'city': 'New York', 'country': 'USA', 'id': '550e8400-e29b-41d4-a716-446655440000', 'postal_code':
            '10001', 'state': 'NY', 'street': '123 Main St'}].
        id (UUID | Unset): Server-generated User ID. Example: 99999999-9999-4999-8999-999999999999.
        created_at (datetime.datetime | Unset): Creation timestamp (UTC). Example: 2025-01-15T10:20:30Z.
        updated_at (datetime.datetime | Unset): Last update timestamp (UTC). Example: 2025-01-16T12:00:00Z.
    """

    username: str
    email: str
    phone: None | str | Unset = UNSET
    birth_date: datetime.date | None | Unset = UNSET
    addresses: list[AddressBase] | Unset = UNSET
    id: UUID | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
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

        id: str | Unset = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

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
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

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

        _id = d.pop("id", UNSET)
        id: UUID | Unset
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

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

        user_read = cls(
            username=username,
            email=email,
            phone=phone,
            birth_date=birth_date,
            addresses=addresses,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        user_read.additional_properties = d
        return user_read

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
