from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


classes = {"amenities": "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"
           }


@app_views.route('/status')
def status_check():
    '''
    checks status of JSON
    '''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def obj_count():
    '''
    retrieves number of objects by type
    '''
    obj_count = {}
    for key, value in classes.items():
        obj_count[key] = storage.count(value)
    return jsonify(obj_count)


if __name__ == '__main__':
    pass





