from curses import flash
from flask import Flask, redirect, render_template, request, url_for
from flask_github import GitHub, User
from os import environ

app = Flask(__name__)
app.secret_key = environ["FLASK_KEY"]

github = GitHub(app)

app.config['GITHUB_CLIENT_ID'] = environ["GITHUB_CLIENT_ID"]
app.config['GITHUB_CLIENT_SECRET'] = environ["GITHUB_CLIENT_SECRET"]

if environ.get("DEBUG", "False") != "False":
    app.config['GITHUB_CLIENT_ID'] = environ["GITHUB_DEV_CLIENT_ID"]
    app.config['GITHUB_CLIENT_SECRET'] = environ["GITHUB_DEV_CLIENT_SECRET"]

@app.route('/')
def home():
    side_projects = ["herdwise", 'pairswith', 'fling', 'tally', "smooth"]
    # TODO: add a button for logging in.
    return render_template('index.html', side_projects=side_projects)

@app.route('/login')
def login():
    return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
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
def flings(username): 
    side_projects = ["herdwise", 'pairswith', 'fling', 'tally', "smooth"]
    return render_template('all-flings.html', side_projects = side_projects)

@app.route('/fling/<flingname>')
def fling(flingname):
    side_project = {""}
    return render_template('fling.html', sideproject = side_project)
    