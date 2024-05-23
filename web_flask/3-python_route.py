#!/usr/bin/python3
"""starting flask web app"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def display():
    """Display method"""
    return 'Hello HBNB'


@app.route('/hbnb', strict_slashes=False)
def hbnb_display():
    """Display method for route"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_display(text):
    """Display method for the route"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def python_display(text='is cool'):
    """Display method for the route"""
    return 'Python {}'.format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
