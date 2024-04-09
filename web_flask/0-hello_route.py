#!/usr/bin/python3
"""Module that starts a Flask web application"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """Method that display “Hello HBNB!”"""
    return "Hello HBNB!"


if __name__ == "__main__":
    # App must be listening on 0.0.0.0, port 5000
    app.run(host="0.0.0.0", port=5000)
