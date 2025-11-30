from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ThreadRead")


@_attrs_define
class ThreadRead:
    """Returned to the client when fetching thread info.

    Example:
        {'author_id': 'a1b2c3d4-e5f6-7890-1234-567890abcdef', 'created_at': '2025-11-10T12:34:56Z', 'participant_id':
            'bb12cc34-dd56-ee78-9900-aabbccddeeff', 'thread_id': '550e8400-e29b-41d4-a716-446655440000', 'updated_at':
            '2025-11-10T12:35:56Z'}

    Attributes:
        author_id (UUID): The user who created the thread.
        participant_id (UUID): The other person in the conversation.
        thread_id (UUID):
        created_at (datetime.datetime | Unset):
        updated_at (datetime.datetime | Unset):
    """

    author_id: UUID
    participant_id: UUID
    thread_id: UUID
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        author_id = str(self.author_id)

        participant_id = str(self.participant_id)

        thread_id = str(self.thread_id)

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
                "author_id": author_id,
                "participant_id": participant_id,
                "thread_id": thread_id,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        author_id = UUID(d.pop("author_id"))

        participant_id = UUID(d.pop("participant_id"))

        thread_id = UUID(d.pop("thread_id"))

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

        thread_read = cls(
            author_id=author_id,
            participant_id=participant_id,
            thread_id=thread_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        thread_read.additional_properties = d
        return thread_read

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
