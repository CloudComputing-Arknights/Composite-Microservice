from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.new_transaction_request import NewTransactionRequest
from ...models.transaction import Transaction
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: NewTransactionRequest,
    x_idempotency_key: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_idempotency_key, Unset):
        headers["X-Idempotency-Key"] = x_idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/transactions/transaction",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | Transaction | None:
    if response.status_code == 201:
        response_201 = Transaction.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | Transaction]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: NewTransactionRequest,
    x_idempotency_key: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | Transaction]:
    """Create Transaction

    Args:
        x_idempotency_key (None | str | Unset):
        body (NewTransactionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Transaction]
    """

    kwargs = _get_kwargs(
        body=body,
        x_idempotency_key=x_idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: NewTransactionRequest,
    x_idempotency_key: None | str | Unset = UNSET,
) -> HTTPValidationError | Transaction | None:
    """Create Transaction

    Args:
        x_idempotency_key (None | str | Unset):
        body (NewTransactionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Transaction
    """

    return sync_detailed(
        client=client,
        body=body,
        x_idempotency_key=x_idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: NewTransactionRequest,
    x_idempotency_key: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | Transaction]:
    """Create Transaction

    Args:
        x_idempotency_key (None | str | Unset):
        body (NewTransactionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Transaction]
    """

    kwargs = _get_kwargs(
        body=body,
        x_idempotency_key=x_idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: NewTransactionRequest,
    x_idempotency_key: None | str | Unset = UNSET,
) -> HTTPValidationError | Transaction | None:
    """Create Transaction

    Args:
        x_idempotency_key (None | str | Unset):
        body (NewTransactionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Transaction
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_idempotency_key=x_idempotency_key,
        )
    ).parsed
