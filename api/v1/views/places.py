#!/usr/bin/python3
"""Module containing routes to manage places associated with cities."""

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places/', methods=['GET'])
@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user_id = data['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if 'name' not in data:
            abort(400, 'Missing name')
        new_place = Place(**data)
        new_place.city_id = city_id
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201
    except Exception as e:
        if '404 Not Found' in str(e):
            return jsonify({'error': str(e)}), 404
        else:
            return jsonify({'error': str(e)}), 400


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404, 'Place not found')
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    except Exception as e:
        if '404 Not Found' in str(e):
            return jsonify({'error': str(e)}), 404
        else:
            return jsonify({'error': str(e)}), 400
