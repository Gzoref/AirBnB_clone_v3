from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=['GET'])
def get_city(state_id=None):
    """
    Returns list of City objects linked to any State

    with state_id: Returns a single state object
    without state_id: 404
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)
    
@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city_id(city_id):
    '''
    Get city by city id
    '''
    city = storage.get(City, city_id)
    if city_id is None:
        abort(404)
    return jsonify(city.to_dict())
    
    

@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_city(city_id=None):
    """
    Deletes a state from the database
    """
    if city_id is not None:
        state = storage.get(City, city_id)
        state.delete()
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route("states/<state_id>/cities", strict_slashes=False, methods=['POST'])
def post_city(state_id=None):
    """
    Post a city
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    city = City(**request.get_json())
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city (city_id=None):
    """ Update a state object
    """
    key = "City." + str(city_id)
    if key not in storage.all(City).keys():
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    city = storage.get(City, city_id)
    for key, value in request.get_json().items():
        if key not in ["created_at", "updated_at", "id"]:
            setattr(city, key, value)
    state.save()
    return jsonify(city.to_dict()), 200
