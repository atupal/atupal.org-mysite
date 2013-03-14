
from application import app

@app.route('/getmap', methods = ['GET', 'POST'])
def getmap():
    lat = request.args.get('lat', '')
    lng = request.args.get('lng', '')
    lat = float('lat')
    lng = float('lng')


