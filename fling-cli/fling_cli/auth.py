import logging
import os
import random
import signal
import string
from subprocess import call

import keyring
import uvicorn
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fling_core import settings
import pathlib


stored_state = None


def make_app():
    app = FastAPI()

    @app.on_event("startup")
    async def login():
        global stored_state
        stored_state = ''.join(random.choice(string.ascii_letters) for i in range(20))
        authorization_url = f"{settings.api_server}/github-login?state={stored_state}"
        print("Going to GitHub authorization url in a browser window...")
        call(f'sleep 0.1 && open "{authorization_url}"', shell=True)

    @app.get("/callback")
    async def callback(state: str, token: str, username: str):
        # Die after this request finishes, no matter what

        if state != stored_state:
            raise Exception("State doesn't match, bad!")
        print(f"Saving token for `{username}` to keyring.")
        os.makedirs(pathlib.Path(pathlib.Path.home(), ".flingdev"), exist_ok=True)
        with open(pathlib.Path(pathlib.Path.home(), ".flingdev", "flinguser.txt"), "w") as userfile:
            userfile.write(username)
        keyring.set_password("fling-github-token", username, token)
        # default_password = keyring.get_password("fling-github-token", "system-default")
        # if not default_password:
        #     print(f"No default account, Saving token for `{username}` as default.")
        keyring.set_password("fling-github-token", "system-default", token)
        return RedirectResponse('http://localhost:5817', status_code=302)

    @app.get("/")
    def app_index(background_tasks: BackgroundTasks):
        background_tasks.add_task(signal.raise_signal, signal.SIGINT)
        return HTMLResponse(
            "<html><h1>GitHub login succeeded. You may close this window.</h1></html>"
        )

    return app


def gh_authenticate():
    temp_port = int(settings.local_cli_port)
    app = make_app()
    try:
        uvicorn.run(
            app, host="0.0.0.0", port=temp_port, log_level=logging.CRITICAL)
    finally:
        print("Ok.")


if __name__ == "__main__":
    gh_authenticate()
