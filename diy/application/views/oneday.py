
from application import app
from flask import render_template

@app.route("/project/oneday")
def oneday_index():
    return render_template("project/oneday.html")

@app.route("/apitest/getList")
def apitest_getList():
    return render_template("project/apitest_getList.html")

@app.route("/apitest/getLine")
def apitest_getLine():
    return render_template("project/apitest_getLine.html")

@app.route("/apitest/shakeLine")
def apitest_shakeLine():
    return render_template("project/apitest_shakeLine.html")
