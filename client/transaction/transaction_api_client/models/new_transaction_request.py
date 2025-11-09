from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_transaction_request_status import NewTransactionRequestStatus
from ..models.new_transaction_request_type import NewTransactionRequestType
from ..types import UNSET, Unset

T = TypeVar("T", bound="NewTransactionRequest")


@_attrs_define
class NewTransactionRequest:
    """
    Attributes:
        requested_item_id (str): UUID of the requested item. Example: 3f0a6a3c-6f34-4c11-9b3e-58b3b2cc0b9e.
        initiator_user_id (str): UUID of the initiator user. Example: 1b2c3d4e-5f60-7a89-b0c1-d2e3f4a5b6c7.
        receiver_user_id (str): UUID of the receiver user. Example: 7c6b5a4f-3e2d-1c0b-9a87-6f5e4d3c2b1a.
        type_ (NewTransactionRequestType): Transaction type. Example: trade.
        offered_item_id (None | str | Unset): Optional offered item UUID when type is trade. Example:
            9eaa9a7c-4e3b-4c9f-8fb0-0ea9722c9b9c.
        offered_price (float | None | Unset): Optional offered price when type is purchase. Example: 25.5.
        message (None | str | Unset): Optional initial message. Example: Can we meet this weekend?.
        status (NewTransactionRequestStatus | Unset): Initial status for the transaction. Default:
            NewTransactionRequestStatus.PENDING. Example: pending.
    """

    requested_item_id: str
    initiator_user_id: str
    receiver_user_id: str
    type_: NewTransactionRequestType
    offered_item_id: None | str | Unset = UNSET
    offered_price: float | None | Unset = UNSET
    message: None | str | Unset = UNSET
    status: NewTransactionRequestStatus | Unset = NewTransactionRequestStatus.PENDING
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        requested_item_id = self.requested_item_id

        initiator_user_id = self.initiator_user_id

        receiver_user_id = self.receiver_user_id

        type_ = self.type_.value

        offered_item_id: None | str | Unset
        if isinstance(self.offered_item_id, Unset):
            offered_item_id = UNSET
        else:
            offered_item_id = self.offered_item_id

        offered_price: float | None | Unset
        if isinstance(self.offered_price, Unset):
            offered_price = UNSET
        else:
            offered_price = self.offered_price

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requested_item_id": requested_item_id,
                "initiator_user_id": initiator_user_id,
                "receiver_user_id": receiver_user_id,
                "type": type_,
            }
        )
        if offered_item_id is not UNSET:
            field_dict["offered_item_id"] = offered_item_id
        if offered_price is not UNSET:
            field_dict["offered_price"] = offered_price
        if message is not UNSET:
            field_dict["message"] = message
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        requested_item_id = d.pop("requested_item_id")

        initiator_user_id = d.pop("initiator_user_id")

        receiver_user_id = d.pop("receiver_user_id")

        type_ = NewTransactionRequestType(d.pop("type"))

        def _parse_offered_item_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        offered_item_id = _parse_offered_item_id(d.pop("offered_item_id", UNSET))

        def _parse_offered_price(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        offered_price = _parse_offered_price(d.pop("offered_price", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        _status = d.pop("status", UNSET)
        status: NewTransactionRequestStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = NewTransactionRequestStatus(_status)

        new_transaction_request = cls(
            requested_item_id=requested_item_id,
            initiator_user_id=initiator_user_id,
            receiver_user_id=receiver_user_id,
            type_=type_,
            offered_item_id=offered_item_id,
            offered_price=offered_price,
            message=message,
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
