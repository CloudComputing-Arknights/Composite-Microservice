from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_transaction_request_status import NewTransactionRequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="NewTransactionRequest")


@_attrs_define
class NewTransactionRequest:
    """
    Attributes:
        item_id (int): The ID of the item being requested by the initiator. Example: 8.
        initiator_user_id (str): The ID of the user who started the transaction. Example: 4.
        receiver_user_id (str): The ID of the user who owns the requested item. Example: 6.
        status (NewTransactionRequestStatus | Unset): The current status of the transaction. Default:
            NewTransactionRequestStatus.PENDING. Example: pending.
    """

    item_id: int
    initiator_user_id: str
    receiver_user_id: str
    status: NewTransactionRequestStatus | Unset = NewTransactionRequestStatus.PENDING
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        item_id = self.item_id

        initiator_user_id = self.initiator_user_id

        receiver_user_id = self.receiver_user_id

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "itemId": item_id,
                "initiatorUserId": initiator_user_id,
                "receiverUserId": receiver_user_id,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        item_id = d.pop("itemId")

        initiator_user_id = d.pop("initiatorUserId")

        receiver_user_id = d.pop("receiverUserId")

        _status = d.pop("status", UNSET)
        status: NewTransactionRequestStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = NewTransactionRequestStatus(_status)

        new_transaction_request = cls(
            item_id=item_id,
            initiator_user_id=initiator_user_id,
            receiver_user_id=receiver_user_id,
            status=status,
        )

        new_transaction_request.additional_properties = d
        return new_transaction_request

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
