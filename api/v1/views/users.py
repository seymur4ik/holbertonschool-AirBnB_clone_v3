#!/usr/bin/python3
"""Module containing routes to manage users"""

from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a User"""
    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'email' not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')
        new_user = User(**data)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        if '404 Not Found' in str(e):
            return jsonify({'error': str(e)}), 404
        else:
            return jsonify({'error': str(e)}), 400


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    try:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        if '404 Not Found' in str(e):
            return jsonify({'error': str(e)}), 404
        else:
            return jsonify({'error': str(e)}), 400
