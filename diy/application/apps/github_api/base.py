
from application import app
from flask import request
from flask import redirect
import requests
import json

@app.route('/github/oauth_pre')
def github_oauth_pre():
    return redirect('https://github.com/login/oauth/authorize?client_id=b81f26240c50dbbb325d&redirect_uri=http://atupal.org/github/oauth')
    pass

@app.route('/github/oauth')
def github_oauth():
    code = request.args.get('code', '')
    data = {
            'client_id'     : 'b81f26240c50dbbb325d',
            'client_secret' : 'f8eee7877f5102c240f4ed9779186a1aa6ff628b',
            'code'          : code
            }
    #header = {'Accept': 'application/json'}
    r = requests.post('https://github.com/login/oauth/access_token', data = data)
    #r['username'] = 'atupal'
    with (open(app.config['APPLICATION_ROOT_DIR'] + 'apps/github_api/token.dat'), 'wa').close() as fi:
        fi.write(r.text)
        pass
