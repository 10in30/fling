from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.read_data_fling_id_get_response_read_data_fling_id_get import (
    ReadDataFlingIdGetResponseReadDataFlingIdGet,
)
from ...types import Response


def _get_kwargs(
    fling_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/{fling_id}".format(client.base_url, fling_id=fling_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ReadDataFlingIdGetResponseReadDataFlingIdGet.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    fling_id: str,
    *,
    client: Client,
) -> Response[Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]]:
    """Read Data

    Args:
        fling_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]]
    """

    kwargs = _get_kwargs(
        fling_id=fling_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    fling_id: str,
    *,
    client: Client,
) -> Optional[Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]]:
    """Read Data

    Args:
        fling_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]
    """

    return sync_detailed(
        fling_id=fling_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    fling_id: str,
    *,
    client: Client,
) -> Response[Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]]:
    """Read Data

    Args:
        fling_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]]
    """

    kwargs = _get_kwargs(
        fling_id=fling_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    fling_id: str,
    *,
    client: Client,
) -> Optional[Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]]:
    """Read Data

    Args:
        fling_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ReadDataFlingIdGetResponseReadDataFlingIdGet]
    """

    return (
        await asyncio_detailed(
            fling_id=fling_id,
            client=client,
        )
    ).parsed
