
from application import app
from flask import  render_template

@app.route("/user/profile")
def user_profile():
    return render_template('views/user_profile.html')
