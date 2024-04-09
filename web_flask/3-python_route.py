#!/usr/bin/python3
"""Module that starts a Flask web application"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def HelloHB():
    """Method that display “Hello HBNB!”"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def HB():
    """Method that display “HBNB”"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def CText(text):
    """Method that display “C ” followed by given text"""
    return "C {}".format(text.replace("_", " "))


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python/", defaults={"text": "is cool"})
def PythonText(text):
    """Method that display “Python ” followed by given text"""
    return "Python {}".format(text.replace("_", " "))


if __name__ == "__main__":
    # App must be listening on 0.0.0.0, port 5000
    app.run(host="0.0.0.0", port=5000)
