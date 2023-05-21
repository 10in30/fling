__version__ = "0.1.6"


import keyring
from click.exceptions import UsageError
from fling_core import settings
from fling_client.client import Client


def get_fling_client(require_auth=False):
    username = "system-default"
    token = keyring.get_password("fling-github-token", username)
    if not token and require_auth:
        raise UsageError("No token found, please run ```fling auth``` first.")
    headers = {"gh-token": token or "none"}
    fling_client = Client(
        settings.api_server,
        headers=headers,
        verify_ssl=False,
        timeout=60,
        raise_on_unexpected_status=True,
    )
    return fling_client
