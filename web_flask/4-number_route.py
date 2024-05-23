#!/usr/bin/python3
"""Starting flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def display():
    """Displays Hello HBNB"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb_display():
    """Displays HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_display(text):
    """Displays C followed with text"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def python_display(text="is cool"):
    """Displays Python followed with text"""
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def num_display(n):
    """Displays is a number if integer is passed"""
    return '{} is a number'.format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
