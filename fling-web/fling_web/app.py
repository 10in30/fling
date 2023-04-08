from curses import flash
from flask import Flask, redirect, render_template, request, url_for
from flask_github import GitHub
from os import environ
from fling_core.github import github_client_id, github_client_secret
from flask_bootstrap import Bootstrap

# TODO: These should be the GH app, not the OAUTH app


app = Flask(__name__)
app.secret_key = "FLASK_KEY"
Bootstrap(app)

app.config['GITHUB_CLIENT_ID'] = github_client_id
app.config['GITHUB_CLIENT_SECRET'] = github_client_secret

github_client = GitHub(app)


@app.route('/')
def home():
    side_projects = ["herdwise", 'pairswith', 'fling', 'tally', "smooth"]
    # TODO: add a button for logging in.
    return render_template('index.html', side_projects=side_projects)

@app.route('/login')
def login():
    return github_client.authorize()

@app.route('/github-callback')
@github_client.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')

    #AUTH FAILED
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    #GOLDEN PATH



    #RETRIEVE REPOS PATH
    
    return redirect(next_url)

@app.route('/flings/<username>')
def flings(username="Anouk"): 
    side_projects = ["herdwise", 'pairswith', 'fling', 'tally', "smooth"]
    return render_template('all-flings.html', flings = my_flings, username=username.capitalize())

@app.route('/flings/<username>/<flingname>')
def fling(username="Anouk", flingname="fling"):
    return render_template('fling.html', fling = my_flings[0], username=username.capitalize())

@app.route('/flings/<username>/public')
def public_flings(username="Anouk"):
    return render_template('public-flings.html', flings = my_flings, username=username.capitalize())
    

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