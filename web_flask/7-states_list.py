#!/usr/bin/python3
"""Starting web application"""
from flask import Flask
from models import storage
from flask import render_template

from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def display():
    """Displays an HTML page"""
    states = storage.all('State').values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template("7-states_list.html", states=sorted_states)


@app.teardown_appcontext
def teardown(exc):
    """Removes the current SQLalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
