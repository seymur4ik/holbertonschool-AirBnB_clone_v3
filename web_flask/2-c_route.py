#!/usr/bin/python3
"""starting flask web app"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def display():
    """Display methodfor the route"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb_display():
    """Display methodfor the route"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_display(text):
    """Display methodfor the route"""
    return 'C {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
