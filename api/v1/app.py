#!/usr/bin/python3
''' Runs the web app '''

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    '''
    404  route
    '''
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_app(e):
    '''
    teardown app context
    '''
    storage.close()


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
