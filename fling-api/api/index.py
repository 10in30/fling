import io
from fastapi import FastAPI
from .namefinder import get_all_domains
from starlette.responses import RedirectResponse
from os import environ
from dotenv import load_dotenv
import httpx
import json
import botocore
from . import BUCKET, s3_client

load_dotenv()

app = FastAPI(title="fling")


github_client_id = environ["GITHUB_CLIENT_ID"]
github_client_secret = environ["GITHUB_CLIENT_SECRET"]
github_dev_client_id = environ["GITHUB_DEV_CLIENT_ID"]
github_dev_client_secret = environ["GITHUB_DEV_CLIENT_SECRET"]


@app.get('/')
async def index():
    return {'hello': 'world'}


@app.get("/namer", tags=["names"])
async def generate_names(
        phrase: str = "Clothing for Autistic Children") -> dict:
    names = get_all_domains(phrase)
    return {'names': names}


@app.get('/github-login')
async def github_login():
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={github_dev_client_id}&scope=repo", status_code=302)


@app.get('/github-code')
async def github_code(code: str):
    params = {
        'client_id': github_dev_client_id,
        'client_secret': github_dev_client_secret,
        'code': code
    }

    headers = {'Accept': 'application/json'}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://github.com/login/oauth/access_token",
            params=params,
            headers=headers)
    response_json = response.json()
    access_token = response_json['access_token']

    async with httpx.AsyncClient() as client:
        headers.update({'Authorization': f'Bearer {access_token}'})
        response = await client.get(url="https://api.github.com/user", headers=headers)
        username = response.json()['login']
        repo_list = await client.get(
            url=f"https://api.github.com/search/repositories?q=user:{username}",
            headers=headers)
            # %20is:private
        return repo_list.json()


@app.post("/{fling_id}/add", tags=["data"])
async def add_data(
    fling_id: str,
    key: str, val: str
) -> dict:
    cache = safe_read_data(fling_id)
    cache[key] = val
    s3_client.put_object(Body=json.dumps(cache),
                         Bucket=BUCKET,
                         Key=f"{fling_id}.json")
    return cache


@app.get("/{fling_id}", tags=["data"])
async def read_data(fling_id: str) -> dict:
    cache = safe_read_data(fling_id)
    return cache


def safe_read_data(fling_id: str):
    s3_obj = {}
    try:
        s3_obj = s3_client.get_object(
            Bucket=BUCKET,
            Key=f"{fling_id}.json")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            pass
        else:
            raise e
    raw_cache = s3_obj.get("Body", io.BytesIO("{}".encode("utf-8")))
    cache = json.loads(raw_cache.read())
    return cache
