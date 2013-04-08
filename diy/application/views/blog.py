
from application import app
import markdown
from flask import render_template
from flask import Markup
from flaskext.markdown import Markdown
Markdown(app)


@app.route("/blog")
def blog():
    content = open(app.config['APPLICATION_ROOT_DIR'] + 'tests/test_post.markdown', 'r').read()
    return render_template('views/blog.html', content = content)
    #content = Markup(markdown.markdown(content))
    #return render_template('views/blog.html', **locals())
