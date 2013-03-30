
from application import app
from flask import render_template

@app.route("/about")
def about():
    return "About me"

