#!/usr/bin/python3
"""Module containing routes to manage states"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'],
                 strict_slashes=False)
def get_states():
    """Retrieves a list of all State objects"""
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by its id"""
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    return jsonify(the_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    storage.delete(the_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Creates a new State"""
    try:
        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')
        if 'name' not in data:
            abort(400, description='Missing name')

        new_state = State(name=data['name'])
        storage.new(new_state)
        storage.save()

        return jsonify(new_state.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def updates_state(state_id):
    """Updates a State object"""
    try:
        data = request.get_json()
        the_state = storage.get(State, state_id)
        if the_state is None:
            abort(404)
        if not data:
            abort(400, description='Not a JSON')
        if 'name' not in data:
            abort(400, description='Missing name')
        the_state.name = data['name']
        storage.save()
        return jsonify(the_state.to_dict()), 200
    except Exception as e:
        if '404 Not Found' in str(e):
            return jsonify({'error': str(e)}), 404
        else:
            return jsonify({'error': str(e)}), 400
