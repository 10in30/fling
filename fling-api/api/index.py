import hashlib
import io
from typing import Annotated, Union
from fastapi import FastAPI, Header
import requests
from .namefinder import get_all_domains
from starlette.responses import RedirectResponse
from fling_core.github import (
    github_client_id,
    github_client_secret,
    validate_token,
    get_username_from_token,
)
from fling_core import settings
import json
import botocore
from . import BUCKET, s3_client
from cachetools import TTLCache, cached


app = FastAPI(title="fling")


@app.get("/")
async def index():
    return {"hello": "world"}


@app.get("/namer", tags=["names"])
async def generate_names(
    phrase: str, gh_token: Annotated[Union[str, None], Header()] = None
) -> dict:
    names = get_all_domains(phrase)
    return {"names": names}


@app.get("/github-login")
async def github_login(state: str):
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={github_client_id}&state={state}&scope=repo",
        status_code=307,
    )


def get_token_from_code(code):
    params = {
        "client_id": github_client_id,
        "client_secret": github_client_secret,
        "code": code,
    }

    headers = {"Accept": "application/json"}
    response = requests.post(
        url="https://github.com/login/oauth/access_token",
        params=params,
        headers=headers,
    )
    response_json = response.json()
    print(response_json)
    access_token: str = response_json.get("access_token")
    return access_token


@app.get("/callback")
async def github_code(code: str, state: str):
    # TODO(JMC): Accept parameter for local port number
    access_token = get_token_from_code(code)
    validation = validate_token(access_token)
    if validation.status_code != 200:
        raise "Token is invalid"
    username: str = validation.json()["user"]["login"]
    return RedirectResponse(
        f"http://localhost:5817/callback?token={access_token}&username={username}&state={state}",
        status_code=307,
    )


@app.get("/callback/web-prod")
async def token_to_web(code: str, state: str):
    access_token = get_token_from_code(code)
    return RedirectResponse(
        f"{settings.web_server}/callback?oauth_token={access_token}&state={state}",
        status_code=307,
    )


@app.get("/repolist", tags=["data"])
async def get_repo_list(gh_token: Annotated[Union[str, None], Header()] = None):
    username = get_username_from_token(gh_token)
    if not username:
        return {"error": "No Github Token or Token not valid"}
    repos = get_repos_by_username(username, gh_token)
    return repos


@cached(cache=TTLCache(maxsize=100, ttl=60))
def get_repos_by_username(username, gh_token):
    headers = {"Accept": "application/json", "Authorization": f"Bearer {gh_token}"}
    return paginated_gh_api("https://api.github.com/user/repos?per_page=200", headers)


def paginated_gh_api(first_url, headers):
    session = requests.Session()
    repo_list = []
    url = first_url
    while url:
        repos_response = session.get(url=url, headers=headers)
        repo_list.extend(repos_response.json())
        url = repos_response.links.get("next", {}).get("url", None)
    return repo_list


@app.get("/index", tags=["data"])
async def read_index(gh_token: Annotated[Union[str, None], Header()] = None) -> dict:
    username = get_username_from_token(gh_token)
    return project_index_for_user(username)


index_cache = TTLCache(maxsize=100, ttl=30)


@cached(cache=index_cache)
def project_index_for_user(username):
    index = safe_read_data(f"gh{username}")
    print(f"Reading index for {username}, got {json.dumps(index)}")
    return index.get("projects", {})


@app.put("/index", tags=["data"])
async def add_to_index(
    fling_id, gh_token: Annotated[Union[str, None], Header()] = None
) -> dict:
    username = get_username_from_token(gh_token)
    repos = get_repos_by_username(username, gh_token)
    allowed_fling_ids = [f"github.com/{x['full_name']}" for x in repos]
    if fling_id not in allowed_fling_ids:
        raise Exception("This project is not in your repo list, not allowed?")

    index = safe_read_data(f"gh{username}")
    projects = index.get("projects", {})
    projects[fling_id] = {"visibility": "private"}
    index["projects"] = projects
    print(f"Writing {json.dumps(index)} to index file for {username}")
    s3_client.put_object(
        Body=json.dumps(index), Bucket=BUCKET, Key=f"gh{username}.json"
    )
    index_cache.clear()
    return index


@app.post("/{fling_id}/add", tags=["data"])
async def add_data(
    fling_id: str,
    key: str,
    val: str,
    gh_token: Annotated[Union[str, None], Header()] = None,
) -> dict:
    username = get_username_from_token(gh_token)
    index = project_index_for_user(username)
    # TODO(JMC): Optimize this, store the hashes maybe?
    hashes = [hashlib.md5(x.encode("utf-8")).hexdigest() for x in index.keys()]
    if fling_id not in hashes:
        raise Exception("You don't have permissions on this fling")
    cache = safe_read_data(fling_id)
    cache[key] = val
    s3_client.put_object(Body=json.dumps(cache), Bucket=BUCKET, Key=f"{fling_id}.json")
    return cache


@app.get("/{fling_id}", tags=["data"])
async def read_data(
    fling_id: str, gh_token: Annotated[Union[str, None], Header()] = None
) -> dict:
    username = get_username_from_token(gh_token)
    index = project_index_for_user(username)
    # TODO(JMC): Optimize this, store the hashes maybe?
    hashes = [hashlib.md5(x.encode("utf-8")).hexdigest() for x in index.keys()]
    if fling_id not in hashes:
        raise Exception("You don't have permissions on this fling")
    cache = safe_read_data(fling_id)
    return cache


def safe_read_data(fling_id: str):
    s3_obj = {}
    try:
        s3_obj = s3_client.get_object(Bucket=BUCKET, Key=f"{fling_id}.json")
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            pass
        else:
            raise e
    raw_cache = s3_obj.get("Body", io.BytesIO("{}".encode("utf-8")))
    cache = json.loads(raw_cache.read() or {})
    return cache
