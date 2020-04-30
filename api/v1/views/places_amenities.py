#!/usr/bin/python3
""" Lists Place objects and Amenity objects """

from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=['GET'])
def get_place_amenity(place_id=None):
    """
    Returns list of amenities objects linked to any place

    with place_id: Returns place objects
    without place_id: 404
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity_list = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        for amenity in place.amenities:
            amenity_list.append(amenity.to_dict())
    else:
        for amenity in place.amenity_id:
            amenity_list.append(storage.get(Amenity, amenity).to_dict())
    return jsonify(amenity_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a amenity from the database
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
    place.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['POST'])
def post_place_amenity(place_id=None, amenity_id=None):
    """
    Post a amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)
    if amenity is None:
        abort(404)
    if place is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append('Amenity.' + amenity_id)
    place.save()
    return jsonify(amenity.to_dict()), 201
