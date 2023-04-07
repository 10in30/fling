import logging
import random
import signal
import string
from subprocess import call

import keyring
import uvicorn
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import HTMLResponse
from fling_core import settings


stored_state = None


def make_app():
    app = FastAPI()

    @app.on_event("startup")
    async def login():
        global stored_state
        stored_state = ''.join(random.choice(string.ascii_letters) for i in range(20))
        authorization_url = f"{settings.fling.api_server}/github-login?state={stored_state}"
        print("Going to GitHub authorization url in a browser window...")
        call(f'sleep 0.1 && open "{authorization_url}"', shell=True)

    @app.get("/callback")
    async def callback(state: str, token: str, username: str, background_tasks: BackgroundTasks):
        background_tasks.add_task(signal.raise_signal, signal.SIGINT)
        # Die after this request finishes, no matter what

        if state != stored_state:
            raise Exception("State doesn't match, bad!")
        print(f"Saving token for `{username}` to keyring.")
        keyring.set_password("fling-github-token", username, token)
        return HTMLResponse(
            """<html><head>
            <meta http-equiv="refresh"
            content="0;URL='http://localhost:5817'" />
            </head><h1>Redirecting...</h1></html>"""
        )

    @app.get("/")
    def app_index():
        return HTMLResponse(
            "<html><h1>GitHub login succeeded. You may close this window.</h1></html>"
        )

    return app


def gh_authenticate():
    temp_port = int(settings.fling.local_cli_port)
    app = make_app()
    try:
        uvicorn.run(
            app, host="0.0.0.0", port=temp_port, log_level=logging.CRITICAL)
    finally:
        print("Ok.")


if __name__ == "__main__":
    gh_authenticate()
