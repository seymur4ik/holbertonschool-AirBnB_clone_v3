#!/usr/bin/python3
"""Starting web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def display():
    """Display method"""
    states = storage.all("State").values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template("7-states_list.html", states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def display_state(id):
    """Display method"""
    state = storage.all("State").values()
    for s in state:
        if s.id == id:
            return render_template("9-states.html", state=s)

    return render_template("9-states.html", state=None)


@app.teardown_appcontext
def teardown(exc):
    """Removes the current SQLalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
