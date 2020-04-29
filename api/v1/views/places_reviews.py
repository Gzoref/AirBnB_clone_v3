#!/usr/bin/python3
""" Lists reviews """

from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review

@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id=None):
    """
    Returns list of City objects linked to any State

    with state_id: Returns a single state object
    without state_id: 404
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['GET'])
def get_review_id(review_id=None):
    '''
    Get city by city id
    '''
    review = storage.get(Review, review_id)
    if review_id is None or review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_city(review_id=None):
    """
    Deletes a review from the database
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_city(place_id=None):
    """
    Post a review
    """
    place_key = "Place." + str(state_id)
    if palce_key not in storage.all(Place).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_city(review_id=None):
    """ Update a state object
    """
    key = "Review." + str(review_id)
    if key not in storage.all(Review).keys():
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    review = storage.get(Review, review_id)
    for key, value in request.get_json().items():
        if key not in ["created_at", "updated_at", "id"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
