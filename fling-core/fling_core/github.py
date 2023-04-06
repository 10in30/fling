from os import environ
from pprint import pprint
from dotenv import load_dotenv
import httpx
import keyring

load_dotenv()


github_client_id = environ["GITHUB_CLIENT_ID"]
github_client_secret = environ["GITHUB_CLIENT_SECRET"]
if environ.get("DEBUG", "False") != "False":
    github_client_id = environ["GITHUB_DEV_CLIENT_ID"]
    github_client_secret = environ["GITHUB_DEV_CLIENT_SECRET"]


def validate_token(token):
    url = f"https://api.github.com/applications/{github_client_id}/token"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    body = f'{{"access_token": "{token}"}}'
    response = httpx.post(
        url,
        data=body,
        headers=headers,
        auth=(github_client_id, github_client_secret),
    )
    return response


def get_username_from_token(access_token):
    validation = validate_token(access_token)
    if validation.status_code != 200:
        raise "Token is invalid"
    username = validation.json()['user']['login']
    return username


__EXPORTS__ = [github_client_id, github_client_secret]


if __name__ == "__main__":
    username = "joshuamckenty"
    token = keyring.get_password("fling-github-token", username)
    response = validate_token(token)
    pprint(response.json())
