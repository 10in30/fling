import logging
import os
import random
import signal
import string

import keyring
import uvicorn
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fling_core import settings
from pathlib import Path
import webbrowser


stored_state = None


def make_app():
    app = FastAPI()

    @app.on_event("startup")
    async def login():
        global stored_state
        stored_state = ''.join(random.choice(string.ascii_letters) for i in range(20))
        authorization_url = f"{settings.api_server}/github-login?state={stored_state}"
        print("Going to GitHub authorization url in a browser window...")
        webbrowser.open(authorization_url)

    @app.get("/callback")
    async def callback(state: str, token: str, username: str):
        # Die after this request finishes, no matter what

        if state != stored_state:
            raise Exception("State doesn't match, bad!")
        os.makedirs(Path(Path.home(), ".flingdev"), exist_ok=True)
        with open(Path(Path.home(), ".flingdev", "flinguser.txt"), "w+") as userfile:
            userfile.write(username)
        os.makedirs(Path("/Users", "Shared", ".loophost"), exist_ok=True)
        with open(Path("/Users", "Shared", ".loophost", "flinguser.txt"), "w+") as userfile:
            userfile.write(username)
        print(f"Saving token for `{username}` to keyring.")
        keyring.set_password("fling-github-token", username, token)
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
            app, host="0.0.0.0", port=temp_port, log_level=logging.DEBUG)  # log_level=logging.CRITICAL)
    finally:
        print("Ok.")


if __name__ == "__main__":
    gh_authenticate()
