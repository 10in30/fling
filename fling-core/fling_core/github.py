"""Basic libraries for authn/authz against GitHub"""
import functools
from os import environ
from pprint import pprint
from dotenv import load_dotenv
import requests
from . import settings

load_dotenv()

environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# TODO(JMC): Consider disabling this some of the time

github_client_id = settings.github_client_id
github_client_secret = settings.github_client_secret


def validate_token(token):
    url = f"https://api.github.com/applications/{github_client_id}/token"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    body = f'{{"access_token": "{token}"}}'
    response = requests.post(
        url,
        data=body,
        headers=headers,
        auth=(github_client_id, github_client_secret),
    )
    return response

@functools.lru_cache(maxsize=128)
def get_username_from_token(access_token):
    validation = validate_token(access_token)
    if validation.status_code != 200:
        raise Exception("Token is invalid")
    pprint(validation.json())
    username = validation.json()['user']['login']
    return username


__EXPORTS__ = [github_client_id, github_client_secret]
