
from application import app
from flask import render_template

@app.route("/apitest/getList")
def apitest():
    return render_template("apitest.html")
