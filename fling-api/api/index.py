import io
from fastapi import FastAPI
import requests
from .namefinder import get_all_domains
from starlette.responses import RedirectResponse

import json
import botocore
from . import BUCKET, s3_client
from fling_core.github import (
    get_username_from_token,
)

app = FastAPI(title="fling")


@app.get("/")
async def index():
    return {"hello": "world"}


@app.get("/namer", tags=["names"])
async def generate_names(phrase: str = "Clothing for Autistic Children") -> dict:
    names = get_all_domains(phrase)
    return {"names": names}


# @app.get("/github-login")
# async def github_login():
#     return RedirectResponse(
#         f"https://github.com/login/oauth/authorize?client_id={github_client_id}&scope=repo",
#         status_code=302,
#     )


# @app.get("/github-code")
# async def github_code(code: str):
#     params = {
#         "client_id": github_client_id,
#         "client_secret": github_client_secret,
#         "code": code,
#     }

#     headers = {"Accept": "application/json"}
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             url="https://github.com/login/oauth/access_token",
#             params=params,
#             headers=headers,
#         )
#     response_json = response.json()
#     access_token = response_json["access_token"]
#     print(response_json)

#     validation = validate_token(access_token)
#     if validation.status_code != 200:
#         raise "Token is invalid"
#     username = validation.json()['user']['login']
#     keyring.set_password("fling-github-token", username, access_token)
#     return {"message": "Access Token saved."}
#     # return RedirectResponse("/repolist")


@app.get("/repolist")
async def get_repo_list(access_token: str):
    username = get_username_from_token(access_token)
    headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
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
