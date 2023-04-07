import io
from typing import Annotated, Union
from fastapi import FastAPI, Header
import requests
from .namefinder import get_all_domains
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fling_core.github import (
    github_client_id,
    github_client_secret,
    validate_token,
    get_username_from_token,
)

import json
import botocore
from . import BUCKET, s3_client


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
        status_code=302,
    )


@app.get("/callback")
async def github_code(code: str, state: str):
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
    access_token: str = response_json["access_token"]
    print(response_json)

    validation = validate_token(access_token)
    if validation.status_code != 200:
        raise "Token is invalid"
    username: str = validation.json()["user"]["login"]
    return RedirectResponse(f"http://localhost:5817/callback?token={access_token}&username={username}&state={state}")
    # return HTMLResponse(
    #     f"""<html><head>
    #         <meta http-equiv="refresh"
    #         content="0;URL='http://localhost:5817/callback?token={access_token}&username={username}&state={state}'" />
    #         </head><h1>Redirecting...</h1></html>"""
    # )


@app.get("/repolist", tags=["data"])
async def get_repo_list(gh_token: Annotated[Union[str, None], Header()] = None):
    username = get_username_from_token(gh_token)
    if not username:
        return {"error": "No Github Token or Token not valid"}
    headers = {"Accept": "application/json", "Authorization": f"Bearer {gh_token}"}
    repo_list = requests.get(
        url=f"https://api.github.com/search/repositories?q=user:{username}",
        headers=headers,
    )
    return repo_list.json()


@app.post("/{fling_id}/add", tags=["data"])
async def add_data(fling_id: str, key: str, val: str) -> dict:
    cache = safe_read_data(fling_id)
    cache[key] = val
    s3_client.put_object(Body=json.dumps(cache), Bucket=BUCKET, Key=f"{fling_id}.json")
    return cache


@app.get("/{fling_id}", tags=["data"])
async def read_data(fling_id: str) -> dict:
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
    cache = json.loads(raw_cache.read())
    return cache
