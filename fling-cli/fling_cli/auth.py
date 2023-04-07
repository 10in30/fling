import signal
from subprocess import call

import keyring
import uvicorn
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import HTMLResponse
from fling_core.github import github_client_id, github_client_secret, validate_token
from requests_oauthlib import OAuth2Session

authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"
temp_port = 5817


stored_state = None


def make_app():
    oauth_client = OAuth2Session(github_client_id, scope=["user repo"])
    app = FastAPI()

    @app.on_event("startup")
    async def login():
        global stored_state
        authorization_url, stored_state = oauth_client.authorization_url(
            authorization_base_url
        )
        print(f"Gonna load {authorization_url}")
        call(f'sleep 2 && open "{authorization_url}"', shell=True)

    @app.get("/callback")
    async def callback(code: str, state: str, background_tasks: BackgroundTasks):
        background_tasks.add_task(signal.raise_signal, signal.SIGINT)
        # Die after this request finishes, no matter what
        if state != stored_state:
            raise Exception("State doesn't match, bad!")

        response_json = oauth_client.fetch_token(
            token_url,
            code=code,
            client_secret=github_client_secret,
        )
        print(f"Got some scopes: {response_json['scope']}")
        access_token = response_json["access_token"]
        validation = validate_token(access_token)
        if validation.status_code != 200:
            raise "Token is invalid"
        username = validation.json()["user"]["login"]
        print(f"Saving token for {username}")
        keyring.set_password("fling-github-token", username, access_token)
        return HTMLResponse(
            "<html><h1>GitHub login succeeded. You may close this window.</h1></html>"
        )

    return app


def gh_authenticate():
    app = make_app()
    try:
        uvicorn.run(app, host="0.0.0.0", port=temp_port)
    finally:
        print("Ok.")


if __name__ == "__main__":
    gh_authenticate()
