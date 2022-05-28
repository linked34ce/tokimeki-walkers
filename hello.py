from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("hello.html", name="World")

@app.route("/<name>")
def hello_user(name):
    return render_template("hello.html", name=name)