
from application import app
import markdown
from flask import render_template
from flask import Markup


@app.route("/blog")
def blog():
    content = open(app.config['APPLICATION_ROOT_DIR'] + 'tests/test_post.markdown', 'r').read()
    content = Markup(markdown.markdown(content))
    return render_template('views/blog.html', **locals())
