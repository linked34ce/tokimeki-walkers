import os
import re
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
# from flask_bootstrap import Bootstrap
# from datetime import datetime
# import pytz

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

# bootstrap = Bootstrap(app)

class User():
    is_authenticated = True
    is_active = True
    is_anonymous = False
    name = None
    password = None
    id = 0

    def __init__(self, name):
        self.name = name

        dbname = "main.db"
        conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql = "select * from Users where name = '{}';".format(name)
        cur.execute(sql)
        record = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if record:
            self.id = record["id"]
            self.password = record["password"]

    def get_id(self):
        return self.id

    def get_by_id(self, id):
        dbname = "main.db"
        conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql = "select * from Users where id = {};".format(id)
        cur.execute(sql)
        record = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return User(record["name"])
        
def dict_factory(cursor, row):
   dic = {}
   for index, column in enumerate(cursor.description):
       dic[column[0]] = row[index]
   return dic

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(User, user_id)

@app.route("/", methods=["GET"])
@login_required
def main():
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))

        return render_template("index.html", username=username)

@app.route("/rally", methods=["GET"])
@login_required
def rally():
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))

        return render_template("rally.html", username=username)

@app.route("/rally/<int:location_id>", methods=["GET"])
@login_required
def detail(location_id):
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))

        return render_template("detail.html", location_id=location_id)

@app.route("/map", methods=["GET"])
@login_required
def map():
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))

        return render_template("map.html", username=username)

@app.route("/map/<int:location_id>", methods=["GET"])
@login_required
def navigation(location_id):
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))

        return render_template("navigation.html", location_id=location_id)

@app.route("/lyrics", methods=["GET"])
@login_required
def lyrics():
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))

        return render_template("lyrics.html", username=username)

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title")

        body = request.form.get("body")
        dbname = "main.db"
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        sql = "insert into Blog (title, body) values ('{}', '{}');".format(title, body)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("main"))
    else:
        return render_template("create.html")

@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    dbname = "main.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")

        sql = "update Blog set title = '{}', body = '{}' where id = {};".format(title, body, id)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("main"))
    else:
        sql = "select * from Blog  where id = {};".format(id)
        cur.execute(sql)
        article = cur.fetchone()
        cur.close()
        conn.close()

        return render_template("update.html", article=article)

@app.route("/delete/<int:id>", methods=["GET"])
@login_required
def delete(id):
    dbname = "main.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    sql = "delete from Blog where id = {};".format(id)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("main"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password-confirm")

        result = "<span class='text-danger'>*</span> "
        pattern = re.compile(r'^[a-zA-Z0-9]+$')

        if not username or not password or not password_confirm:
            result += "すべての項目を入力してください"
        elif len(password) < 8 and not pattern.match(password):
            result += "パスワードは8文字以上の半角英数字で入力してください"
        elif len(password) < 8:
            result += "パスワードは8文字以上で入力してください"
        elif not pattern.match(password):
            result += "パスワードは半角英数字で入力してください"
        elif password != password_confirm:
            result += "再入力したパスワードが一致しません"

        else:
            password_hash = generate_password_hash(password, method="sha256")

            dbname = "main.db"
            conn = sqlite3.connect(dbname)
            cur = conn.cursor()
            sql = "insert into Users (name, password) values ('{}', '{}');".format(username, password_hash)

            try:
                cur.execute(sql)
            except sqlite3.IntegrityError:
                result += "そのユーザ名はすでに使用されています"
                conn.commit()
                cur.close()
                conn.close()
            else:
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for("login"))

        return render_template("signup.html", result=result)
    else:
        return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username)
        User.name = username

        if user.id > 0 and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main"))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))