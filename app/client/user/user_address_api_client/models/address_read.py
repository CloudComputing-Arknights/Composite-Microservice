from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddressRead")


@_attrs_define
class AddressRead:
    """
    Attributes:
        street (str): Street address and number. Example: 123 Main St.
        city (str): City or locality. Example: New York.
        country (str): Country name or ISO label. Example: USA.
        id (UUID | Unset): Persistent Address ID (server-generated). Example: 550e8400-e29b-41d4-a716-446655440000.
        state (None | str | Unset): State/region code if applicable. Example: NY.
        postal_code (None | str | Unset): Postal or ZIP code. Example: 10001.
        created_at (datetime.datetime | Unset): Creation timestamp (UTC). Example: 2025-01-15T10:20:30Z.
        updated_at (datetime.datetime | Unset): Last update timestamp (UTC). Example: 2025-01-16T12:00:00Z.
    """

    street: str
    city: str
    country: str
    id: UUID | Unset = UNSET
    state: None | str | Unset = UNSET
    postal_code: None | str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        street = self.street

        city = self.city

        country = self.country

        id: str | Unset = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        state: None | str | Unset
        if isinstance(self.state, Unset):
            state = UNSET
        else:
            state = self.state

        postal_code: None | str | Unset
        if isinstance(self.postal_code, Unset):
            postal_code = UNSET
        else:
            postal_code = self.postal_code

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
                "street": street,
                "city": city,
                "country": country,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if state is not UNSET:
            field_dict["state"] = state
        if postal_code is not UNSET:
            field_dict["postal_code"] = postal_code
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        street = d.pop("street")

        city = d.pop("city")

        country = d.pop("country")

        _id = d.pop("id", UNSET)
        id: UUID | Unset
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        def _parse_state(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        state = _parse_state(d.pop("state", UNSET))

        def _parse_postal_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        postal_code = _parse_postal_code(d.pop("postal_code", UNSET))

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

        address_read = cls(
            street=street,
            city=city,
            country=country,
            id=id,
            state=state,
            postal_code=postal_code,
            created_at=created_at,
            updated_at=updated_at,
        )

        address_read.additional_properties = d
        return address_read

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
