from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.category_type import CategoryType
from ...models.http_validation_error import HTTPValidationError
from ...models.item_read import ItemRead
from ...models.transaction_type import TransactionType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    category: CategoryType | None | Unset = UNSET,
    transaction_type: None | TransactionType | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 10,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_category: None | str | Unset
    if isinstance(category, Unset):
        json_category = UNSET
    elif isinstance(category, CategoryType):
        json_category = category.value
    else:
        json_category = category
    params["category"] = json_category

    json_transaction_type: None | str | Unset
    if isinstance(transaction_type, Unset):
        json_transaction_type = UNSET
    elif isinstance(transaction_type, TransactionType):
        json_transaction_type = transaction_type.value
    else:
        json_transaction_type = transaction_type
    params["transaction_type"] = json_transaction_type

    params["skip"] = skip

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/items/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[ItemRead] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ItemRead.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[ItemRead]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    category: CategoryType | None | Unset = UNSET,
    transaction_type: None | TransactionType | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 10,
) -> Response[HTTPValidationError | list[ItemRead]]:
    """List Items

     Get a list of all items, with optional filtering.

    Args:
        category (CategoryType | None | Unset): Filter by item's category
        transaction_type (None | TransactionType | Unset): Filter by item's transaction type
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ItemRead]]
    """

    kwargs = _get_kwargs(
        category=category,
        transaction_type=transaction_type,
        skip=skip,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    category: CategoryType | None | Unset = UNSET,
    transaction_type: None | TransactionType | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 10,
) -> HTTPValidationError | list[ItemRead] | None:
    """List Items

     Get a list of all items, with optional filtering.

    Args:
        category (CategoryType | None | Unset): Filter by item's category
        transaction_type (None | TransactionType | Unset): Filter by item's transaction type
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ItemRead]
    """

    return sync_detailed(
        client=client,
        category=category,
        transaction_type=transaction_type,
        skip=skip,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    category: CategoryType | None | Unset = UNSET,
    transaction_type: None | TransactionType | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 10,
) -> Response[HTTPValidationError | list[ItemRead]]:
    """List Items

     Get a list of all items, with optional filtering.

    Args:
        category (CategoryType | None | Unset): Filter by item's category
        transaction_type (None | TransactionType | Unset): Filter by item's transaction type
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ItemRead]]
    """

    kwargs = _get_kwargs(
        category=category,
        transaction_type=transaction_type,
        skip=skip,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    category: CategoryType | None | Unset = UNSET,
    transaction_type: None | TransactionType | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 10,
) -> HTTPValidationError | list[ItemRead] | None:
    """List Items

     Get a list of all items, with optional filtering.

    Args:
        category (CategoryType | None | Unset): Filter by item's category
        transaction_type (None | TransactionType | Unset): Filter by item's transaction type
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ItemRead]
    """

    return (
        await asyncio_detailed(
            client=client,
            category=category,
            transaction_type=transaction_type,
            skip=skip,
            limit=limit,
        )
    ).parsed
