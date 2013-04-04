
from application import app
from flask import render_template

@app.route("/")
def index(name = None):
    return render_template('views/index.html', name=name)

@app.route("/about")
def about():
    return render_template("views/about.html")

@app.route("/contact")
def contanct():
    return render_template("views/contact.html")

