from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="MessageCreate")



@_attrs_define
class MessageCreate:
    """ 
        Example:
            {'content': 'Hey! Are you still selling the mirror?', 'sender_id': '123e4567-e89b-12d3-a456-426614174000'}

        Attributes:
            sender_id (UUID):
            content (str):
     """

    sender_id: UUID
    content: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        sender_id = str(self.sender_id)

        content = self.content


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "sender_id": sender_id,
            "content": content,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sender_id = UUID(d.pop("sender_id"))




        content = d.pop("content")

        message_create = cls(
            sender_id=sender_id,
            content=content,
        )


        message_create.additional_properties = d
        return message_create

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
