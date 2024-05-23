#!/usr/bin/python3
"""Starting web application"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """404 Error handler """
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown(exc):
    """Closing current session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
