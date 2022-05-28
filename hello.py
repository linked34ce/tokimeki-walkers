from flask import Flask
from flask import render_template

app = Flask(__name__)

items =[
    "item1", "item2",  "item3", 
    "item4",  "item5", "item6"
]

dicts = [
    {"name1": "Miura", "name2": "Junya"},
    {"name1": "Tanaka", "name2": "Taro"}
]

@app.route("/")
def hello_world():
    return render_template("hello.html", name="World", items=items, dicts=dicts)

@app.route("/<name>")
def hello_user(name):
    return render_template("hello.html", name=name, items=items, dicts=dicts)