from flask import Flask, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_states(state_id=None):
    """
    Returns state objects based on path

    with state_id: Returns a single state object
    without state_id: Returns every state
    """
    new_list = []
    key = "State." + str(state_id)
    if state_id is None:
        objs = storage.all(State)
        for key, value in objs.items():
            new_list.append(value.to_dict())
    elif key in storage.all(State).keys():
        new_list.append(storage.all(State)[key].to_dict())
    else:
        abort(404)
    return jsonify(new_list)
