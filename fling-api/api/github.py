from os import environ
from dotenv import load_dotenv
import httpx

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
    body = f"{{\"access_token\": \"{token}\"}}"
    response = httpx.post(
        url,
        data=body,
        headers=headers,
        auth=(github_client_id, github_client_secret),
    )
    return response


__EXPORTS__ = [github_client_id, github_client_secret]
