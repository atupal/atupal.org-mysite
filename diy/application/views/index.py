
from application import app
from flask import render_template

@app.route("/")
def index(name = None):
    return render_template('views/index.html', name=name)

@app.route("/about")
def about():
    return "about me"
