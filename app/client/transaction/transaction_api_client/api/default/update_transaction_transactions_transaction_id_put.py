from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.transaction import Transaction
from ...models.update_status_request import UpdateStatusRequest
from ...types import Response


def _get_kwargs(
    transaction_id: str,
    *,
    body: UpdateStatusRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/transactions/{transaction_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | Transaction | None:
    if response.status_code == 200:
        response_200 = Transaction.from_dict(response.json())

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
) -> Response[HTTPValidationError | Transaction]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateStatusRequest,
) -> Response[HTTPValidationError | Transaction]:
    """Update Transaction

    Args:
        transaction_id (str):
        body (UpdateStatusRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Transaction]
    """

    kwargs = _get_kwargs(
        transaction_id=transaction_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateStatusRequest,
) -> HTTPValidationError | Transaction | None:
    """Update Transaction

    Args:
        transaction_id (str):
        body (UpdateStatusRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Transaction
    """

    return sync_detailed(
        transaction_id=transaction_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateStatusRequest,
) -> Response[HTTPValidationError | Transaction]:
    """Update Transaction

    Args:
        transaction_id (str):
        body (UpdateStatusRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Transaction]
    """

    kwargs = _get_kwargs(
        transaction_id=transaction_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateStatusRequest,
) -> HTTPValidationError | Transaction | None:
    """Update Transaction

    Args:
        transaction_id (str):
        body (UpdateStatusRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Transaction
    """

    return (
        await asyncio_detailed(
            transaction_id=transaction_id,
            client=client,
            body=body,
        )
    ).parsed
