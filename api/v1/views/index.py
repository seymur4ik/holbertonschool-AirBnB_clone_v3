#!/usr/bin/python3
"""Index Module

This module defines routes to provide status and statistics information
for various objects in the application.
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
import models

classes = {"amenities": "Amenity", "cities": "City",
           "places": "Place", "reviews": "Review",
           "states": "State",  "users": "User"}


@app_views.route('/status')
def status():
    """Returns the status of the API.

    Returns:
        JSON response:
            {
                "status": "OK"
            }
    """
    return jsonify({"status":  "OK"})


@app_views.route('/stats')
def stats():
    """Retrieves statistics about the number of objects by type.

    Counts the number of objects (instances) for each model class
    defined in the 'classes' dictionary.

    Returns:
        JSON response containing the counts of objects by type:
            {
                "amenities": <count of Amenities>,
                "cities": <count of Cities>,
                "places": <count of Places>,
                "reviews": <count of Reviews>,
                "states": <count of States>,
                "users": <count of Users>
            }
    """
    counts = {}
    for cls in classes:
        counts[cls] = storage.count(classes[cls])
    return jsonify(counts)
