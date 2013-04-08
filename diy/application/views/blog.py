
from application import app
import markdown
from flask import render_template
from flask import Markup


@app.route("/blog")
def blog():
    content = open('/home/atupal/src/git/octopress/source/_posts/2013-03-18-dropbox-intra.markdown', 'r').read()
    content = Markup(markdown.markdown(content))
    return render_template('views/blog.html', **locals())
