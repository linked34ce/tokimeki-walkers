import os
import ssl
import re
from unittest import result
import requests
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from matplotlib import use
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
# import pytz

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

class User():
    is_authenticated = True
    is_active = True
    is_anonymous = False
    name = None
    password = None
    id = 0

    def __init__(self, name):
        record = None
        username_pattern = re.compile(r'^(?!.*(\'|\s)).*$')

        if username_pattern.match(name):
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
            self.name = record["name"]
            self.password = record["password"]
        else:
            self.name = None

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
#@login_required
def main():
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))
        
        dbname = "main.db"
        conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql = "select * from Locations left join Visits on Locations.id = Visits.location_id where username = '{}';".format(username)
        cur.execute(sql)
        locations = cur.fetchall()

        num_of_locations = len(locations)
        num_of_visited = 0
        num_of_photos = 0
        for location in locations:
            if location["visit_count"] > 0:
                num_of_visited += 1
            print(location["photo"])
            if location["photo"] != "/static/tmp/no_image.jpg":
                num_of_photos += 1

        return render_template("index.html", username=username, num_of_locations=num_of_locations, num_of_visited=num_of_visited, num_of_photos=num_of_photos)

@app.route("/rally", methods=["GET"])
#@login_required
def rally():
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))
        
        dbname = "main.db"
        conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql = "select * from Locations left join Visits on Locations.id = Visits.location_id where username = '{}';".format(username)
        cur.execute(sql)
        locations = cur.fetchall()

        for location in locations:
            if location["visit_count"] > 0:
                location["visited"] = "✅訪問済"
            else:
                location["visited"] = "⚠️未訪問"
                location["share_button"] = " disabled"

        cur.close()
        conn.close()

        return render_template("rally.html", username=username, locations=locations)

@app.route("/rally/<int:location_id>", methods=["GET"])
#@login_required
def detail(location_id):
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))
        
        dbname = "main.db"
        conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql1 = "select * from Locations inner join Visits on Locations.id = Visits.location_id where location_id = {} and username = '{}';".format(location_id, username)
        cur.execute(sql1)
        location = cur.fetchone()
        cur.close()
        conn.close()

        if location["visit_count"] < 1:
            message = "⚠️この聖地は未訪問です"
        else:
            message = "✅この聖地は{}回訪問済みです".format(location["visit_count"])

        return render_template("detail.html", username=username, location=location, message=message)

@app.route("/checkin/<int:location_id>/<int:with_photo>")
#@login_required
def checkin(location_id, with_photo):
    if request.method == "GET":
        if User.name:
            if with_photo:
                photo = "/static/tmp/divercity.jpg"
            else:
                photo = "/static/tmp/no_image.jpg"
            username=User.name
            dbname = "main.db"
            conn = sqlite3.connect(dbname)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            sql = "update Visits set photo = '{}', visit_count = visit_count + 1, last_visit = current_timestamp where username = '{}' and location_id = {};".format(photo, username, location_id)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        else:
            return redirect(url_for("login"))
        
        return redirect(url_for("detail", location_id=location_id))
    
@app.route("/map", methods=["GET"])
#@login_required
def map():
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))

        return render_template("map.html", username=username)

@app.route("/map/<int:location_id>", methods=["GET"])
#@login_required
def navigation(location_id):
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))

        return render_template("navigation.html", location_id=location_id)

@app.route("/lyrics", methods=["GET"])
#@login_required
def lyrics():
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))

        return render_template("lyrics.html", username=username)

@app.route("/create", methods=["GET", "POST"])
#@login_required
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
#@login_required
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
#@login_required
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
        username_pattern = re.compile(r'^(?!.*(\'|\s)).*$')
        password_pattern = re.compile(r'^[a-zA-Z0-9]+$')

        if not username or not password or not password_confirm:
            result += "すべての項目を入力してください"
        elif not username_pattern.match(username):
            result += "ユーザ名にシングルクオーテーション (') および空白文字は使用できません"
        elif len(password) < 8 and not password_pattern.match(password):
            result += "パスワードは8文字以上の半角英数字で入力してください"
        elif len(password) < 8:
            result += "パスワードは8文字以上で入力してください"
        elif not password_pattern.match(password):
            result += "パスワードは半角英数字で入力してください"
        elif password != password_confirm:
            result += "再入力したパスワードが一致しません"

        else:
            password_hash = generate_password_hash(password, method="sha256")

            dbname = "main.db"
            conn = sqlite3.connect(dbname)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            sql1 = "insert into Users (name, password) values ('{}', '{}');".format(username, password_hash)

            try:
                cur.execute(sql1)
            except sqlite3.IntegrityError:
                result += 'ユーザ名 "{}" はすでに使用されています'.format(username)
                username = ""
                cur.close()
                conn.close()
            else:
                sql2 = "select id from Locations;"
                cur.execute(sql2)
                locations = cur.fetchall()
        
                for location in locations:        
                    sql3 = "insert into Visits (username, location_id, photo) values ('{}', {}, '{}');".format(username, location["id"], "/static/tmp/no_image.jpg")
                    try:
                        cur.execute(sql3)
                    except sqlite3.IntegrityError:
                        pass

                conn.commit()
                cur.close()
                conn.close()

                User.name = username
                result = "<span class='text-success'>*</span> ユーザ登録に成功しました"

        return render_template("signup.html", result=result, username=username)
    else:
        return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username)
        User.name = username

        result = "<span class='text-danger'>*</span> "
        password_pattern = re.compile(r'^[a-zA-Z0-9]+$')

        if not username and not password:
            result += "ユーザ名とパスワードを入力してください"
            username = ""
        elif not username:
            result += "ユーザ名を入力してください"
            username = ""
        elif not password:
            result += "パスワードを入力してください"
        elif len(password) < 8 or not password_pattern.match(password):
            result += "パスワードは8文字以上の半角英数字です"
        elif not user.name:
            result += 'ユーザ名 "{}" は登録されていません'.format(username)
            username = ""
        elif user.password:
            if not check_password_hash(user.password, password):
                result += "パスワードに誤りがあります"
            elif user.name:
                login_user(user)
                return redirect(url_for("main"))
        return render_template("login.html", result=result, username=username)
    else:
        if User.name:
            return render_template("login.html", username=User.name)
        else:
            return render_template("login.html")

@app.route("/config", methods=["GET", "POST"])
def config():
    return "<h1>まだ何もないよ！</h1>"

@app.route("/logout")
#@login_required
def logout():
    logout_user()
    User.name = None
    return redirect(url_for("login"))