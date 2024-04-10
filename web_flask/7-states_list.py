#!/usr/bin/python3
"""Module that starts a Flask web application"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def showstates():
    """Method to display a HTML page with states"""
    states = storage.all(State).values()
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    # App must be listening on 0.0.0.0, port 5000
    app.run(host="0.0.0.0", port=5001)
