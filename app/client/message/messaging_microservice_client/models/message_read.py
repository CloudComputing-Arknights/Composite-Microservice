from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageRead")


@_attrs_define
class MessageRead:
    """
    Example:
        {'content': 'Got it, thank you!', 'created_at': '2025-11-10T12:34:56Z', 'id':
            '550e8400-e29b-41d4-a716-446655440000', 'sender_id': '123e4567-e89b-12d3-a456-426614174000', 'thread_id':
            '123e4567-e89b-12d3-a456-426614173000', 'time_stamp': '2025-11-10T12:34:56Z', 'updated_at':
            '2025-11-10T12:45:00Z'}

    Attributes:
        sender_id (UUID): UUID of the sender
        content (str): Content of the message.
        thread_id (UUID): Thread this message belongs to
        time_stamp (datetime.datetime | Unset): Time when the message was sent (UTC).
        id (UUID | Unset):
        created_at (datetime.datetime | Unset):
        updated_at (datetime.datetime | Unset):
    """

    sender_id: UUID
    content: str
    thread_id: UUID
    time_stamp: datetime.datetime | Unset = UNSET
    id: UUID | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sender_id = str(self.sender_id)

        content = self.content

        thread_id = str(self.thread_id)

        time_stamp: str | Unset = UNSET
        if not isinstance(self.time_stamp, Unset):
            time_stamp = self.time_stamp.isoformat()

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
                "sender_id": sender_id,
                "content": content,
                "thread_id": thread_id,
            }
        )
        if time_stamp is not UNSET:
            field_dict["time_stamp"] = time_stamp
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sender_id = UUID(d.pop("sender_id"))

        content = d.pop("content")

        thread_id = UUID(d.pop("thread_id"))

        _time_stamp = d.pop("time_stamp", UNSET)
        time_stamp: datetime.datetime | Unset
        if isinstance(_time_stamp, Unset):
            time_stamp = UNSET
        else:
            time_stamp = isoparse(_time_stamp)

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

        message_read = cls(
            sender_id=sender_id,
            content=content,
            thread_id=thread_id,
            time_stamp=time_stamp,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        message_read.additional_properties = d
        return message_read

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
