from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.read_root_get_response_read_root_get import \
    ReadRootGetResponseReadRootGet
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    phrase: Union[Unset, None, str] = 'Clothing for Autistic Children',

) -> Dict[str, Any]:
    url = "{}/".format(
        client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    params: Dict[str, Any] = {}
    params["phrase"] = phrase



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[HTTPValidationError, ReadRootGetResponseReadRootGet]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ReadRootGetResponseReadRootGet.from_dict(response.json())



        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[HTTPValidationError, ReadRootGetResponseReadRootGet]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    phrase: Union[Unset, None, str] = 'Clothing for Autistic Children',

) -> Response[Union[HTTPValidationError, ReadRootGetResponseReadRootGet]]:
    """ Read Root

    Args:
        phrase (Union[Unset, None, str]):  Default: 'Clothing for Autistic Children'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ReadRootGetResponseReadRootGet]]
     """


    kwargs = _get_kwargs(
        client=client,
phrase=phrase,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Client,
    phrase: Union[Unset, None, str] = 'Clothing for Autistic Children',

) -> Optional[Union[HTTPValidationError, ReadRootGetResponseReadRootGet]]:
    """ Read Root

    Args:
        phrase (Union[Unset, None, str]):  Default: 'Clothing for Autistic Children'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ReadRootGetResponseReadRootGet]
     """


    return sync_detailed(
        client=client,
phrase=phrase,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    phrase: Union[Unset, None, str] = 'Clothing for Autistic Children',

) -> Response[Union[HTTPValidationError, ReadRootGetResponseReadRootGet]]:
    """ Read Root

    Args:
        phrase (Union[Unset, None, str]):  Default: 'Clothing for Autistic Children'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ReadRootGetResponseReadRootGet]]
     """


    kwargs = _get_kwargs(
        client=client,
phrase=phrase,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Client,
    phrase: Union[Unset, None, str] = 'Clothing for Autistic Children',

) -> Optional[Union[HTTPValidationError, ReadRootGetResponseReadRootGet]]:
    """ Read Root

    Args:
        phrase (Union[Unset, None, str]):  Default: 'Clothing for Autistic Children'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ReadRootGetResponseReadRootGet]
     """


    return (await asyncio_detailed(
        client=client,
phrase=phrase,

    )).parsed
