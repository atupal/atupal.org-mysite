
from application import app
from flask import render_template

@app.route("/project/oneday")
def oneday_index():
    return render_template("project/oneday.html")

@app.route("/apitest/getList")
def apitest():
    return render_template("apitest.html")

