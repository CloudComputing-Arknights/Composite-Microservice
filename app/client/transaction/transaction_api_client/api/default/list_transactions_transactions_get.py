from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_transactions_transactions_get_status_param_type_0 import (
    ListTransactionsTransactionsGetStatusParamType0,
)
from ...models.list_transactions_transactions_get_type_type_0 import ListTransactionsTransactionsGetTypeType0
from ...models.transaction import Transaction
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    status_param: ListTransactionsTransactionsGetStatusParamType0 | None | Unset = UNSET,
    initiator_user_id: None | str | Unset = UNSET,
    receiver_user_id: None | str | Unset = UNSET,
    requested_item_id: None | str | Unset = UNSET,
    type_: ListTransactionsTransactionsGetTypeType0 | None | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_status_param: None | str | Unset
    if isinstance(status_param, Unset):
        json_status_param = UNSET
    elif isinstance(status_param, ListTransactionsTransactionsGetStatusParamType0):
        json_status_param = status_param.value
    else:
        json_status_param = status_param
    params["status_param"] = json_status_param

    json_initiator_user_id: None | str | Unset
    if isinstance(initiator_user_id, Unset):
        json_initiator_user_id = UNSET
    else:
        json_initiator_user_id = initiator_user_id
    params["initiator_user_id"] = json_initiator_user_id

    json_receiver_user_id: None | str | Unset
    if isinstance(receiver_user_id, Unset):
        json_receiver_user_id = UNSET
    else:
        json_receiver_user_id = receiver_user_id
    params["receiver_user_id"] = json_receiver_user_id

    json_requested_item_id: None | str | Unset
    if isinstance(requested_item_id, Unset):
        json_requested_item_id = UNSET
    else:
        json_requested_item_id = requested_item_id
    params["requested_item_id"] = json_requested_item_id

    json_type_: None | str | Unset
    if isinstance(type_, Unset):
        json_type_ = UNSET
    elif isinstance(type_, ListTransactionsTransactionsGetTypeType0):
        json_type_ = type_.value
    else:
        json_type_ = type_
    params["type"] = json_type_

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/transactions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[Transaction] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Transaction.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | list[Transaction]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    status_param: ListTransactionsTransactionsGetStatusParamType0 | None | Unset = UNSET,
    initiator_user_id: None | str | Unset = UNSET,
    receiver_user_id: None | str | Unset = UNSET,
    requested_item_id: None | str | Unset = UNSET,
    type_: ListTransactionsTransactionsGetTypeType0 | None | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[Transaction]]:
    """List Transactions

    Args:
        status_param (ListTransactionsTransactionsGetStatusParamType0 | None | Unset):
        initiator_user_id (None | str | Unset):
        receiver_user_id (None | str | Unset):
        requested_item_id (None | str | Unset):
        type_ (ListTransactionsTransactionsGetTypeType0 | None | Unset):
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[Transaction]]
    """

    kwargs = _get_kwargs(
        status_param=status_param,
        initiator_user_id=initiator_user_id,
        receiver_user_id=receiver_user_id,
        requested_item_id=requested_item_id,
        type_=type_,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    status_param: ListTransactionsTransactionsGetStatusParamType0 | None | Unset = UNSET,
    initiator_user_id: None | str | Unset = UNSET,
    receiver_user_id: None | str | Unset = UNSET,
    requested_item_id: None | str | Unset = UNSET,
    type_: ListTransactionsTransactionsGetTypeType0 | None | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[Transaction] | None:
    """List Transactions

    Args:
        status_param (ListTransactionsTransactionsGetStatusParamType0 | None | Unset):
        initiator_user_id (None | str | Unset):
        receiver_user_id (None | str | Unset):
        requested_item_id (None | str | Unset):
        type_ (ListTransactionsTransactionsGetTypeType0 | None | Unset):
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[Transaction]
    """

    return sync_detailed(
        client=client,
        status_param=status_param,
        initiator_user_id=initiator_user_id,
        receiver_user_id=receiver_user_id,
        requested_item_id=requested_item_id,
        type_=type_,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    status_param: ListTransactionsTransactionsGetStatusParamType0 | None | Unset = UNSET,
    initiator_user_id: None | str | Unset = UNSET,
    receiver_user_id: None | str | Unset = UNSET,
    requested_item_id: None | str | Unset = UNSET,
    type_: ListTransactionsTransactionsGetTypeType0 | None | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[Transaction]]:
    """List Transactions

    Args:
        status_param (ListTransactionsTransactionsGetStatusParamType0 | None | Unset):
        initiator_user_id (None | str | Unset):
        receiver_user_id (None | str | Unset):
        requested_item_id (None | str | Unset):
        type_ (ListTransactionsTransactionsGetTypeType0 | None | Unset):
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[Transaction]]
    """

    kwargs = _get_kwargs(
        status_param=status_param,
        initiator_user_id=initiator_user_id,
        receiver_user_id=receiver_user_id,
        requested_item_id=requested_item_id,
        type_=type_,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    status_param: ListTransactionsTransactionsGetStatusParamType0 | None | Unset = UNSET,
    initiator_user_id: None | str | Unset = UNSET,
    receiver_user_id: None | str | Unset = UNSET,
    requested_item_id: None | str | Unset = UNSET,
    type_: ListTransactionsTransactionsGetTypeType0 | None | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[Transaction] | None:
    """List Transactions

    Args:
        status_param (ListTransactionsTransactionsGetStatusParamType0 | None | Unset):
        initiator_user_id (None | str | Unset):
        receiver_user_id (None | str | Unset):
        requested_item_id (None | str | Unset):
        type_ (ListTransactionsTransactionsGetTypeType0 | None | Unset):
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[Transaction]
    """

    return (
        await asyncio_detailed(
            client=client,
            status_param=status_param,
            initiator_user_id=initiator_user_id,
            receiver_user_id=receiver_user_id,
            requested_item_id=requested_item_id,
            type_=type_,
            limit=limit,
            offset=offset,
        )
    ).parsed
