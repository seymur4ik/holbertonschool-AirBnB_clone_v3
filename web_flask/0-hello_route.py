#!/usr/bin/python3
"""Starting a Flask web application"""
from flask import Flask

app = Flask(__name__)
"""object of Flask class"""


@app.route('/', strict_slashes=False)
def display():
    """method to display hello """
    return 'Hello HBNB!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
