import os
import re
from datetime import datetime
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from matplotlib import use
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import send_from_directory
import sqlite3

UPLOAD_FOLDER = "./static/uploads/"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
        username_pattern = re.compile(r'^(?!.*(\s)).*$')

        if username_pattern.match(name):
            dbname = "main.db"
            conn = sqlite3.connect(dbname)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            name = name.replace("'", "''")
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
        escaped_username =  username.replace("'", "''")
        sql1 = "select * from Locations left join Visits on Locations.id = Visits.location_id where username = '{}';".format(escaped_username)
        cur.execute(sql1)
        visits = cur.fetchall()
        sql2 = "select id from Locations"
        cur.execute(sql2)
        locations = cur.fetchall()

        num_of_locations = len(locations)
        location_id = 0
        num_of_visited_locs = 0
        num_of_photos = 0
        for visit in visits:
            if location_id != visit["location_id"]:
                location_id = visit["location_id"]
                num_of_visited_locs += 1
                if visit["photo"] != "/static/tmp/no_image.jpg":
                    num_of_photos += 1

        lyrics_percent = 17

        return render_template("index.html", username=username, num_of_locations=num_of_locations,
                num_of_visited_locs=num_of_visited_locs, num_of_photos=num_of_photos, lyrics_percent=lyrics_percent)

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
        sql1 = "select * from Locations;"
        cur.execute(sql1)
        locations = cur.fetchall()

        NO_IMG_PATH = "/static/tmp/no_image.jpg"

        for location in locations:
            escaped_username =  username.replace("'", "''")
            sql2 = "select * from Locations left join Visits on Locations.id = Visits.location_id where username = '{}' and location_id = '{}' order by time desc;".format(escaped_username, location["id"])
            cur.execute(sql2)
            visits = cur.fetchall()
            location["visit_count"] = len(visits)
            if location["visit_count"] > 0:
                location["visited"] = "✅訪問済"
            else:
                location["visited"] = "⚠️未訪問"
                location["share_button"] = " disabled"     
            if not visits:
                location["photo"] = NO_IMG_PATH
            elif not visits[0]["photo"]:
                location["photo"] = NO_IMG_PATH
            else:
                location["photo"] = visits[0]["photo"]

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
        escaped_username =  username.replace("'", "''")
        sql1 = "select * from Locations left join Visits on Locations.id = Visits.location_id where location_id = {} and username = '{}' order by time desc;".format(location_id, escaped_username)
        cur.execute(sql1)
        visits = cur.fetchall()
        sql2 = "select * from Locations where id = {}".format(location_id)
        cur.execute(sql2)
        location = cur.fetchone()
        cur.close()
        conn.close()

        location["visit_count"] = len(visits)
        if visits:
            location["last_visit"] = visits[0]["time"]
            
        if location["visit_count"] < 1:
            message = "⚠️この聖地は未訪問です"
        else:
            message = "✅この聖地は{}回訪問済みです".format(location["visit_count"])

        return render_template("detail.html", username=username, location=location, message=message)

@app.route("/checkinWithoutPhoto/<int:location_id>/")
#@login_required
def checkinWithoutPhoto(location_id):
    if request.method == "GET":
        if User.name:
            photo = "/static/tmp/no_image.jpg"
            username=User.name
            dbname = "main.db"
            conn = sqlite3.connect(dbname)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            escaped_username =  username.replace("'", "''")
            sql = "insert into Visits (username, location_id, photo) values ('{}', {}, '{}');".format(escaped_username, location_id, photo)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        else:
            return redirect(url_for("login"))
        return redirect(url_for("detail", location_id=location_id))

@app.route("/upload/<int:location_id>", methods=["POST"])
#@login_required
def upload(location_id):
    if request.method == "POST":
        if User.name:
            file = request.files["photo"]
            filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + secure_filename(file.filename) 
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            username=User.name
            dbname = "main.db"
            conn = sqlite3.connect(dbname)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            escaped_username =  username.replace("'", "''")
            photo = "/static/uploads/" + filename
            sql = "insert into Visits (username, location_id, photo) values ('{}', {}, '{}');".format(escaped_username, location_id, photo)
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

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password-confirm")

        result = "<span class='text-danger'>*</span> "
        username_pattern = re.compile(r'^(?!.*(\s)).*$')
        password_pattern = re.compile(r'^[a-zA-Z0-9]+$')

        if not username or not password or not password_confirm:
            result += "すべての項目を入力してください"
        elif not username_pattern.match(username):
            result += "ユーザ名に空白文字は使用できません"
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
            escaped_username =  username.replace("'", "''")
            sql1 = "insert into Users (name, password) values ('{}', '{}');".format(escaped_username, password_hash)

            try:
                cur.execute(sql1)
            except sqlite3.IntegrityError:
                escaped_username =  username.replace("'", "\'")
                result += 'ユーザ名 "{}" はすでに使用されています'.format(escaped_username)
                username = ""
                cur.close()
                conn.close()
            else:
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
            escaped_username =  username.replace("'", "\'")
            result += 'ユーザ名 "{}" は登録されていません'.format(escaped_username)
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
#@login_required
def config():
    if User.name:
        current_username = User.name
        user = User(current_username)
        user_id = str(user.get_id()).zfill(5)
    else:
        return redirect(url_for("login"))

    username = current_username
    dbname = "main.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    escaped_username =  username.replace("'", "''")
    sql = "select profile from Users where name = '{}';".format(escaped_username)
    cur.execute(sql)
    profile = cur.fetchone()[0]

    if request.method == "POST":
        if request.form.get("username"):
            new_username = request.form.get("username")
            result = "<span class='text-danger'>*</span> "
            username_pattern = re.compile(r'^(?!.*(\s)).*$')

            escaped_current_username =  current_username.replace("'", "''")
            escaped_new_username =  new_username.replace("'", "''")
            profile = request.form.get("profile")
            if not profile:
                profile = ""

            sqls = [
                "update Users set name = '{}' where name = '{}';".format(escaped_new_username, escaped_current_username),
                "update Visits set username = '{}' where username = '{}';".format(escaped_new_username, escaped_current_username)
            ]

            if not new_username or not username_pattern.match(new_username):
                result += "ユーザ名に空白文字は使用できません"
            else:
                try:
                    for sql in sqls:
                        cur.execute(sql)
                except sqlite3.IntegrityError:
                    escaped_new_username =  new_username.replace("'", "\'")
                    result += 'ユーザ名 "{}" はすでに使用されています'.format(escaped_new_username)
                    cur.close()
                    conn.close()
                else:
                    conn.commit()
                    cur.close()
                    conn.close()

                    result = "<span class='text-success'>*</span> ユーザ名を変更しました"
                    User.name = new_username
                    user = User(new_username)
                    username = new_username
        elif request.form.get("profile"):
            profile = request.form.get("profile")
            escaped_profile = profile.replace("'", "''")
            escaped_current_username =  current_username.replace("'", "''")

            sql = "update Users set profile = '{}' where name = '{}';".format(escaped_profile, escaped_current_username)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            result = "<span class='text-success'>*</span> プロフィールを変更しました"
        elif not request.form.get("profile"):
            escaped_current_username =  current_username.replace("'", "''")
            sql = "update Users set profile = null where name = '{}';".format(escaped_current_username)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            profile = ""
            result = "<span class='text-success'>*</span> プロフィールを変更しました"
        return render_template("config.html", user_id = user_id, username=username, result=result, profile=profile)
    else:
        if not profile:
            profile = ""
        return render_template("config.html", user_id = user_id, username=username, profile=profile)

@app.route("/logout")
#@login_required
def logout():
    logout_user()
    User.name = None
    return redirect(url_for("login"))