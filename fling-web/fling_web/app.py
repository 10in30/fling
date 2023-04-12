import hashlib
import random
import string
from cachetools import TTLCache, cached
from flask import Flask, redirect, session, render_template, request, url_for, flash
from flask_github import GitHub
from os import environ
from fling_core.github import (
    github_client_id,
    github_client_secret,
    get_username_from_token,
)
from fling_core import settings
from flask_bootstrap import Bootstrap
from fling_client.client import Client
from fling_client.api.data import (
    add_data_fling_id_add_post,
    read_data_fling_id_get,
    get_repo_list_repolist_get,
    add_to_index_index_put,
    read_index_index_get,
)

# TODO: These should be the GH app, not the OAUTH app


app = Flask(__name__)
app.secret_key = settings.flask_key
Bootstrap(app)

app.config["GITHUB_CLIENT_ID"] = github_client_id
app.config["GITHUB_CLIENT_SECRET"] = github_client_secret

github_client = GitHub(app)


@app.route("/")
def home():
    side_projects = ["herdwise", "pairswith", "fling", "tally", "smooth"]
    # TODO: add a button for logging in.
    return render_template("index.html", side_projects=side_projects)


@app.route("/login")
def login():
    # TODO(JMC): Create state variable and store in cookie
    state = ''.join(random.choice(string.ascii_letters) for i in range(20))
    session['state'] = state
    return github_client.authorize(redirect_uri=f"{settings.api_server}/callback/web-prod", state=state)


@app.route("/callback")
def authorized():
    oauth_token: str = request.args.get('oauth_token')
    state: str = request.args.get('state')
    if state != session['state']:
        flash("Bad state variable, failing auth loop.")
        return redirect("/")
    # AUTH FAILED
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect("/")

    session["token"] = oauth_token
    session["username"] = get_username_from_token(oauth_token)
    next_url = request.args.get("next") or url_for(
        "flings", username=session["username"]
    )
    return redirect(next_url, code=307)


def get_api_client(gh_token):
    headers = {"gh-token": gh_token}
    fling_client = Client(
        settings.api_server,
        headers=headers,
        verify_ssl=False,
        timeout=60,
        raise_on_unexpected_status=True,
    )
    return fling_client


@app.route("/flings/<username>")
def flings(username="Anouk"):
    api_client = get_api_client(session["token"])
    project_list = read_index_index_get.sync(client=api_client).to_dict()
    for project in project_list.keys():
        project_list[project].update(project_data(session["token"], project))
    return render_template(
        "all-flings.html", flings=project_list, username=username.capitalize()
    )


@cached(cache=TTLCache(maxsize=100, ttl=300))
def project_data(token, project):
    api_client = get_api_client(token)
    hashed_fling_id = hashlib.md5(project.encode("utf-8")).hexdigest()
    project_details = read_data_fling_id_get.sync(
        fling_id=hashed_fling_id, client=api_client
    ).to_dict()
    return project_details


@app.route("/flings/<username>/<flingname>")
def fling(username="Anouk", flingname="fling"):
    return render_template(
        "fling.html", fling=my_flings[0], username=username.capitalize()
    )


@app.route("/flings/<username>/public")
def public_flings(username="Anouk"):
    return render_template(
        "public-flings.html", flings=my_flings, username=username.capitalize()
    )

my_flings = [{"summary": {
    "fling_id": "2",
    "fling_name": "HerdWise",
    "role": "Owner",
    "last_update": "2013-04-06T18:25:43.511Z",
    "started_on": "2013-04-03T18:25:43.511Z",
    "domain": "https://herdwise.io",
    "active users": "5",
    "total views": "69",
    "description": "A landing page for a Mastodon analytics service that we hope will help creators find audiences, without anyone's privacy being violated in horrible ways and tailored to all the ways in which mastodon is different/weird/better. "},
"business": {
    "currency": "CAD",
    "revenue": [{
        "date": "2013-04-05T18:25:43.511Z",
        "type": "donation",
        "source": "Simba",
        "description": "",
        "amount": "12"},
        {
            "date": "2013-05-05T18:25:43.511Z",
            "type": "Aladin",
            "source": "",
            "description": "",
            "amount": "25"
        }],
    "costs": [{
        "date": "2013-03-05T18:25:43.511Z",
        "type": "hosting",
        "recipient": "Peter Pan Hosting",
        "description": "",
        "amount": "67"}]},
"user_activity":{
    "total_views": "69",
    "active_users": [{
        "date":"2013-04-06T18:25:43.511Z",
        "count": "12" },{
        "date":"2013-04-05T18:25:43.511Z",
        "count": "5"}],
    "views": [{
        "date": "2013-04-06T18:25:43.511Z",
        "count": "29"},{
        "date": "2013-03-05T18:25:43.511Z",
        "count": "21" },{
        "date": "2013-03-04T18:25:43.511Z",
        "count": "19" }]},
"essentials":{
    "domain": "https://herdwise.io",
    "collaborators": ["Zazu", "Timon", "Mufasa", "Nala"],
    "DNS_host": "name.com",
    "hosting": "vercel",
    "repo": "https://github.com/herdwise",
    "social_media":[{
        "name": "Instagram",
        "username": "herdwise2023"
    },{
        "name": "mastodon",
        "username": "@jumbo@herdwise.io"
    }]}},
    {"summary": {
    "fling_id": "1",
    "fling_name": "PairsWith",
    "role": "Owner",
    "last_update": "2013-03-31T18:25:43.511Z",
    "started_on": "2013-03-28T18:25:43.511Z",
    "domain": "https://herdwise.io",
    "active users": "5",
    "total views": "69",
    "description": "A goofy little app that lets you match your meal to a playlist. Take an image of your food and the machine does the rest! "},
"business": {
    "currency": "CAD",
    "revenue": [{
        "date": "2013-03-31T18:25:43.511Z",
        "type": "donation",
        "source": "Simba",
        "description": "",
        "amount": "12"},
        {
            "date": "2013-03-30T18:25:43.511Z",
            "type": "Aladin",
            "source": "",
            "description": "",
            "amount": "25"
        }],
    "costs": [{
        "date": "2013-03-05T18:25:43.511Z",
        "type": "hosting",
        "recipient": "Peter Pan Hosting",
        "description": "",
        "amount": "67"}]},
"user_activity":{
    "total_views": "69",
    "active_users": [{
        "date":"2013-04-06T18:25:43.511Z",
        "count": "12" },{
        "date":"2013-04-05T18:25:43.511Z",
        "count": "5"}],
    "views": [{
        "date": "2013-04-06T18:25:43.511Z",
        "count": "29"},{
        "date": "2013-03-05T18:25:43.511Z",
        "count": "21" },{
        "date": "2013-03-04T18:25:43.511Z",
        "count": "19" }]},
"essentials":{
    "domain": "https://pairswith.xyz",
    "collaborators": [ "Timon", "Mufasa", "Nala"],
    "DNS_host": "name.com",
    "hosting": "vercel",
    "repo": "https://github.com/joshuamckenty/pairswith",
    "social_media":[{
        "name": "Instagram",
        "username": "pairswith__"
    },{
        "name": "mastodon",
        "username": "@info@pairswith.xyz"
    }]}},
    {"summary": {
    "fling_id": "2",
    "fling_name": "HerdWise",
    "role": "Owner",
    "last_update": "2013-04-06T18:25:43.511Z",
    "started_on": "2013-04-03T18:25:43.511Z",
    "domain": "http://pairswith.xyz",
    "active users": "5",
    "total views": "69",
    "description": "A landing page for a Mastodon analytics service that we hope will help creators find audiences, without anyone's privacy being violated in horrible ways and tailored to all the ways in which mastodon is different/weird/better. "},
"business": {
    "currency": "CAD",
    "revenue": [{
        "date": "2013-04-05T18:25:43.511Z",
        "type": "donation",
        "source": "Simba",
        "description": "",
        "amount": "12"},
        {
            "date": "2013-05-05T18:25:43.511Z",
            "type": "Aladin",
            "source": "",
            "description": "",
            "amount": "25"
        }],
    "costs": [{
        "date": "2013-03-05T18:25:43.511Z",
        "type": "hosting",
        "recipient": "Peter Pan Hosting",
        "description": "",
        "amount": "67"}]},
"user_activity":{
    "total_views": "69",
    "active_users": [{
        "date":"2013-04-06T18:25:43.511Z",
        "count": "12" },{
        "date":"2013-04-05T18:25:43.511Z",
        "count": "5"}],
    "views": [{
        "date": "2013-04-06T18:25:43.511Z",
        "count": "29"},{
        "date": "2013-03-05T18:25:43.511Z",
        "count": "21" },{
        "date": "2013-03-04T18:25:43.511Z",
        "count": "19" }]},
"essentials":{
    "domain": "https://herdwise.io",
    "collaborators": ["Zazu", "Timon", "Mufasa", "Nala"],
    "DNS_host": "name.com",
    "hosting": "vercel",
    "repo": "https://github.com/herdwise",
    "social_media":[{
        "name": "Instagram",
        "username": "herdwise2023"
    },{
        "name": "mastodon",
        "username": "@jumbo@herdwise.io"
    }]}},
    {"summary": {
    "fling_id": "2",
    "fling_name": "HerdWise",
    "role": "Owner",
    "last_update": "2013-04-06T18:25:43.511Z",
    "started_on": "2013-04-03T18:25:43.511Z",
    "domain": "https://herdwise.io",
    "active users": "5",
    "total views": "69",
    "description": "A landing page for a Mastodon analytics service that we hope will help creators find audiences, without anyone's privacy being violated in horrible ways and tailored to all the ways in which mastodon is different/weird/better. "},
"business": {
    "currency": "CAD",
    "revenue": [{
        "date": "2013-04-05T18:25:43.511Z",
        "type": "donation",
        "source": "Simba",
        "description": "",
        "amount": "12"},
        {
            "date": "2013-05-05T18:25:43.511Z",
            "type": "Aladin",
            "source": "",
            "description": "",
            "amount": "25"
        }],
    "costs": [{
        "date": "2013-03-05T18:25:43.511Z",
        "type": "hosting",
        "recipient": "Peter Pan Hosting",
        "description": "",
        "amount": "67"}]},
"user_activity":{
    "total_views": "69",
    "active_users": [{
        "date":"2013-04-06T18:25:43.511Z",
        "count": "12" },{
        "date":"2013-04-05T18:25:43.511Z",
        "count": "5"}],
    "views": [{
        "date": "2013-04-06T18:25:43.511Z",
        "count": "29"},{
        "date": "2013-03-05T18:25:43.511Z",
        "count": "21" },{
        "date": "2013-03-04T18:25:43.511Z",
        "count": "19" }]},
"essentials":{
    "domain": "https://herdwise.io",
    "collaborators": ["Zazu", "Timon", "Mufasa", "Nala"],
    "DNS_host": "name.com",
    "hosting": "vercel",
    "repo": "https://github.com/herdwise",
    "social_media":[{
        "name": "Instagram",
        "username": "herdwise2023"
    },{
        "name": "mastodon",
        "username": "@jumbo@herdwise.io"
    }]}}]
