from fastapi import FastAPI
from .namefinder import get_all_domains
from starlette.responses import RedirectResponse
from os import environ
import httpx

app = FastAPI(title="fling")

github_client_id = environ["GITHUB_CLIENT_ID"]
github_client_secret = environ["GITHUB_CLIENT_SECRET"]
github_dev_client_id = environ["GITHUB_DEV_CLIENT_ID"]
github_dev_client_secret = environ["GITHUB_DEV_CLIENT_SECRET"]

@app.get("/namer", tags=["names"])
async def generate_names(
        phrase: str = "Clothing for Autistic Children") -> dict:
    names = get_all_domains(phrase)
    return {'names': names}

@app.get('github-login')
async def github_login():
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={github_dev_client_id}", status_code=302)

@app.get('github-code')
async def github_code(code:str):
    params = {
        'client_id': github_dev_client_id,
        'client_secret': github_dev_client_secret,
        'code': code
    }

    headers = {'Accept': 'application/json'}
    async with httpx.AsyncClient() as client:
        response = await client.post(url="https://github.com/login/oauth/access_token", params=params, headers=headers)
    response_json = response.json()
    access_token = response_json['access_token']

    async with httpx.AsyncClient() as client:
        headers.update({'Authorization': f'Bearer {access_token}'})
        response = await client.get(url="https:api.github.com/user", headers=headers)
    return response.json()
