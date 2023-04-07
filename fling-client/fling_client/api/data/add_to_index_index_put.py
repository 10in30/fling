from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.add_to_index_index_put_response_add_to_index_index_put import (
    AddToIndexIndexPutResponseAddToIndexIndexPut,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    fling_id: Any,
    gh_token: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/index".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(gh_token, Unset):
        headers["gh-token"] = gh_token

    params: Dict[str, Any] = {}
    params["fling_id"] = fling_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AddToIndexIndexPutResponseAddToIndexIndexPut.from_dict(response.json())

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
) -> Response[Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    fling_id: Any,
    gh_token: Union[Unset, str] = UNSET,
) -> Response[Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]]:
    """Add To Index

    Args:
        fling_id (Any):
        gh_token (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        fling_id=fling_id,
        gh_token=gh_token,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    fling_id: Any,
    gh_token: Union[Unset, str] = UNSET,
) -> Optional[Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]]:
    """Add To Index

    Args:
        fling_id (Any):
        gh_token (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        fling_id=fling_id,
        gh_token=gh_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    fling_id: Any,
    gh_token: Union[Unset, str] = UNSET,
) -> Response[Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]]:
    """Add To Index

    Args:
        fling_id (Any):
        gh_token (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        fling_id=fling_id,
        gh_token=gh_token,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    fling_id: Any,
    gh_token: Union[Unset, str] = UNSET,
) -> Optional[Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]]:
    """Add To Index

    Args:
        fling_id (Any):
        gh_token (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddToIndexIndexPutResponseAddToIndexIndexPut, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            fling_id=fling_id,
            gh_token=gh_token,
        )
    ).parsed
