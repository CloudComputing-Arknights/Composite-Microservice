from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.address_read import AddressRead
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    street: None | str | Unset = UNSET,
    city: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    postal_code: None | str | Unset = UNSET,
    country: None | str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_street: None | str | Unset
    if isinstance(street, Unset):
        json_street = UNSET
    else:
        json_street = street
    params["street"] = json_street

    json_city: None | str | Unset
    if isinstance(city, Unset):
        json_city = UNSET
    else:
        json_city = city
    params["city"] = json_city

    json_state: None | str | Unset
    if isinstance(state, Unset):
        json_state = UNSET
    else:
        json_state = state
    params["state"] = json_state

    json_postal_code: None | str | Unset
    if isinstance(postal_code, Unset):
        json_postal_code = UNSET
    else:
        json_postal_code = postal_code
    params["postal_code"] = json_postal_code

    json_country: None | str | Unset
    if isinstance(country, Unset):
        json_country = UNSET
    else:
        json_country = country
    params["country"] = json_country

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/addresses",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[AddressRead] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AddressRead.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[AddressRead]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    street: None | str | Unset = UNSET,
    city: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    postal_code: None | str | Unset = UNSET,
    country: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[AddressRead]]:
    """List Addresses

    Args:
        street (None | str | Unset): Filter by street
        city (None | str | Unset): Filter by city
        state (None | str | Unset): Filter by state/region
        postal_code (None | str | Unset): Filter by postal code
        country (None | str | Unset): Filter by country

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AddressRead]]
    """

    kwargs = _get_kwargs(
        street=street,
        city=city,
        state=state,
        postal_code=postal_code,
        country=country,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    street: None | str | Unset = UNSET,
    city: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    postal_code: None | str | Unset = UNSET,
    country: None | str | Unset = UNSET,
) -> HTTPValidationError | list[AddressRead] | None:
    """List Addresses

    Args:
        street (None | str | Unset): Filter by street
        city (None | str | Unset): Filter by city
        state (None | str | Unset): Filter by state/region
        postal_code (None | str | Unset): Filter by postal code
        country (None | str | Unset): Filter by country

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AddressRead]
    """

    return sync_detailed(
        client=client,
        street=street,
        city=city,
        state=state,
        postal_code=postal_code,
        country=country,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    street: None | str | Unset = UNSET,
    city: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    postal_code: None | str | Unset = UNSET,
    country: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[AddressRead]]:
    """List Addresses

    Args:
        street (None | str | Unset): Filter by street
        city (None | str | Unset): Filter by city
        state (None | str | Unset): Filter by state/region
        postal_code (None | str | Unset): Filter by postal code
        country (None | str | Unset): Filter by country

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AddressRead]]
    """

    kwargs = _get_kwargs(
        street=street,
        city=city,
        state=state,
        postal_code=postal_code,
        country=country,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    street: None | str | Unset = UNSET,
    city: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    postal_code: None | str | Unset = UNSET,
    country: None | str | Unset = UNSET,
) -> HTTPValidationError | list[AddressRead] | None:
    """List Addresses

    Args:
        street (None | str | Unset): Filter by street
        city (None | str | Unset): Filter by city
        state (None | str | Unset): Filter by state/region
        postal_code (None | str | Unset): Filter by postal code
        country (None | str | Unset): Filter by country

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AddressRead]
    """

    return (
        await asyncio_detailed(
            client=client,
            street=street,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
        )
    ).parsed
