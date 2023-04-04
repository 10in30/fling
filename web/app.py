from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "DF1F1FDB-7D27-4E4B-984E-2970017FD210"

@app.route('/')
def home():
    side_projects = ["herdwise", 'pairswith', 'fling', 'tally', "smooth"]
    return render_template('index.html', side_projects=side_projects)
