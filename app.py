import os
import re
from datetime import datetime
from math import radians, sin, cos, sqrt
from random import randint
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from waitress import serve
import sqlite3
import boto3
import botocore
from dotenv import load_dotenv

DB_NAME_REMOTE = "tokimeki-walkers/main.db"
DB_NAME_LOCAL  = "main.db"

UPLOAD_FOLDER = "./static/uploads/"
BUCKET_NAME = "graduation-research"
BUCKET_FOLDER = "/uploads/"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

load_dotenv()
client = boto3.client("s3")

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
            try:
                dbname = DB_NAME_LOCAL
                conn = sqlite3.connect(dbname)
            except sqlite3.OperationalError:
                dbname = DB_NAME_REMOTE
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
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
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
def load_user(userid):
    return User.get_by_id(User, userid)

@app.route("/", methods=["GET"])
@login_required
def main():
    if request.method == "GET":
        if User.name:
            username=User.name
            user = User(username)
            userid = user.get_id()   
        else:
            return redirect(url_for("login"))
        
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
            conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        escaped_username =  username.replace("'", "''")
        sql1 = "select * from Locations left join Visits on Locations.id = Visits.location_id where username = '{}';".format(escaped_username)
        cur.execute(sql1)
        visits = cur.fetchall()
        sql2 = "select id from Locations;"
        cur.execute(sql2)
        locations = cur.fetchall()
        conn.row_factory = None
        cur = conn.cursor()
        sql3 = "select * from Lyrics where userid = {};".format(userid)
        cur.execute(sql3)
        lyrics = cur.fetchone()

        num_of_locations = len(locations)
        location_ids = []
        num_of_visited_locs = 0
        num_of_photos = 0
        for visit in visits:
            # print(visit["location_id"])
            if visit["location_id"] not in location_ids:
                location_ids.append(visit["location_id"])
                num_of_visited_locs += 1
                if visit["photo"] != "/static/tmp/no_image.jpg":
                    num_of_photos += 1

        num_of_lyrics = 31
        lyrics = lyrics[1:num_of_lyrics + 1]

        return render_template("index.html", username=username, num_of_locations=num_of_locations,
                num_of_visited_locs=num_of_visited_locs, num_of_photos=num_of_photos, lyrics=lyrics)

@app.route("/rally", methods=["GET"])
@login_required
def rally():
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))
        
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
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

@app.route("/post/<int:location_id>", methods=["POST"])
@login_required
def post(location_id):
    if request.method == "POST":
        if User.name:
            username = User.name
            user = User(username)
            userid = user.get_id()
        else:
            return redirect(url_for("login"))
        
        content = request.form.get("content" + str(location_id))
        if not content:
            content = ""
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
            conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()

        escaped_username =  username.replace("'", "''")
        escaped_content =  content.replace("'", "''")
        sql1 = "select * from Locations left join Visits on Locations.id = Visits.location_id where username = '{}' and location_id = '{}' order by time desc;".format(escaped_username, location_id)
        cur.execute(sql1)
        latest_visit = cur.fetchone()
        photo = latest_visit["photo"]

        sql2 = "insert into Posts (userid, content, photo) values ('{}', '{}', '{}');".format(userid, escaped_content, photo)
        cur.execute(sql2)
        conn.commit()
        cur.close()
        conn.close()
    
        return redirect(url_for("rally"))
    else:
        return redirect(url_for("login"))

@app.route("/rally/<int:location_id>", methods=["GET"])
@login_required
def detail(location_id):
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))
 
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
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

        sql3 = "select * from Locations where id != {};".format(location_id)
        cur.execute(sql3)
        locations = cur.fetchall()
        cur.close()
        conn.close()

        location["visit_count"] = len(visits)
        if visits:
            location["last_visit"] = visits[0]["time"]

        if location["visit_count"] < 1:
            message = "⚠️この聖地は未訪問です"
        else:
            message = "✅この聖地は{}回訪問済みです".format(location["visit_count"])

        for i in range(len(locations)): 
            distance = hubeny_formula(location["latitude"], location["longitude"], 
                                        locations[i]["latitude"], locations[i]["longitude"])
            locations[i]["distance"] = "{:,}".format(round(distance))

        locations.sort(key=lambda x: x["distance"])
        nearest_locations = locations[0:3]

        return render_template("detail.html", username=username, location=location, message=message, 
                                nearest_locations=nearest_locations)

def hubeny_formula(latitude1, longitude1, latitude2, longitude2):
    SEMI_MAJOR_AXIS = 6378137
    SEMI_MINOR_AXIS = 6356752.314245
    eccentricitySquared = (SEMI_MAJOR_AXIS ** 2 - SEMI_MINOR_AXIS ** 2) / SEMI_MAJOR_AXIS ** 2

    radianLatitude1 = radians(latitude1)
    radianLatitude2 = radians(latitude2)
    radianLongitude1 = radians(longitude1)
    radianLongitude2 = radians(longitude2)

    latitudeDelta = radianLatitude2 - radianLatitude1
    longitudeDelta = radianLongitude2 - radianLongitude1
    latitudeAverage = (radianLatitude1 + radianLatitude2) / 2

    denominator = sqrt((1 - eccentricitySquared * sin(latitudeAverage) ** 2))
    radiusOfCurvatureInTheMeridian = (SEMI_MAJOR_AXIS * (1 - eccentricitySquared)) / denominator ** 3
    radiusOfCurvatureInThePrimeVertical = SEMI_MAJOR_AXIS / denominator

    distance = sqrt((latitudeDelta * radiusOfCurvatureInTheMeridian) ** 2 + (longitudeDelta * radiusOfCurvatureInThePrimeVertical * cos(latitudeAverage)) ** 2)
    return distance

@app.route("/posts/<int:page>", methods=["GET"])
@login_required
def posts(page):
    if request.method == "GET":
        if User.name:
            username = User.name
        else:
            return redirect(url_for("login"))
        
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
            conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql1 = "select * from Posts order by time desc;"
        cur.execute(sql1)
        all_posts = cur.fetchall()

        LIMIT = 20
        num_of_posts = len(all_posts)
        num_of_pages = num_of_posts // LIMIT + 1
        lower_limit = LIMIT * (page - 1)
        if page == num_of_pages:
            upper_limit = num_of_posts
        else:
            upper_limit = LIMIT * page
        posts = all_posts[lower_limit:upper_limit]

        for post in posts:
            sql3 = "select name, profile from Users where id = {};".format(post["userid"])
            cur.execute(sql3)
            poster = cur.fetchone()
            post["username"] = poster["name"]
            if poster["profile"]:
                post["profile"] = poster["profile"]
            else:
                post["profile"] = "(プロフィール未設定)"
        cur.close()
        conn.close()

        return render_template("posts.html", posts=posts, page=page, num_of_pages=num_of_pages)

@app.route("/checkinWithoutPhoto/<int:location_id>/", methods=["GET", "POST"])
@login_required
def checkinWithoutPhoto(location_id):
    if request.method == "GET":
        if User.name:
            photo = "/static/tmp/no_image.jpg"
            username=User.name
            try:
                dbname = DB_NAME_LOCAL
                conn = sqlite3.connect(dbname)
            except sqlite3.OperationalError:
                dbname = DB_NAME_REMOTE
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
@login_required
def upload(location_id):
    if request.method == "POST":
        if User.name:
            file = request.files["photo"]
            filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + secure_filename(file.filename) 
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            try:
                client.upload_file(UPLOAD_FOLDER + filename, BUCKET_NAME, BUCKET_FOLDER + filename)
            except botocore.exceptions.NoCredentialsError:
                pass
            username=User.name
            user = User(username)
            userid = user.get_id()
            try:
                dbname = DB_NAME_LOCAL
                conn = sqlite3.connect(dbname)
            except sqlite3.OperationalError:
                dbname = DB_NAME_REMOTE
                conn = sqlite3.connect(dbname)
            cur = conn.cursor()
            escaped_username =  username.replace("'", "''")
            photo = "/static/uploads/" + filename
            sql1 = "insert into Visits (username, location_id, photo) values ('{}', {}, '{}');".format(escaped_username, location_id, photo)
            cur.execute(sql1)

            sql2 = "select * from lyrics where userid = {};".format(userid)
            cur.execute(sql2)
            lyrics = cur.fetchone()
            lyrics = lyrics[1:len(lyrics)]

            escaped_username =  username.replace("'", "''")
            sql3 = "select * from Locations left join Visits on Locations.id = Visits.location_id where location_id = {} and username = '{}' order by time desc;".format(location_id, escaped_username)
            cur.execute(sql3)
            visits = cur.fetchall()
            # print(visits)

            if len(visits) < 2:
                numbers = []
                for i in range(len(lyrics)):
                    if not lyrics[i]:
                        numbers.append(i)
                # print(numbers)
                sql4 = "update Lyrics set lyric{} = 1 where userid = {};".format(numbers[randint(0, len(numbers))], userid)
                cur.execute(sql4)

            conn.commit()
            cur.close()
            conn.close()
        else:
            return redirect(url_for("login"))
    return redirect(url_for("detail", location_id=location_id))
    
@app.route("/map/<int:location_id>", methods=["GET"])
@login_required
def map(location_id):
    if request.method == "GET":
        if User.name:
            username=User.name
        else:
            return redirect(url_for("login"))
        
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
            conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql1 = "select id, name, latitude, longitude, image from Locations;"
        cur.execute(sql1)
        locations = cur.fetchall()

        if location_id < 1:
            central_location = {
                "id": 0,
                "latitude": 35.62484634835641, 
                "longitude": 139.78602418344875
            }
        else:
            sql2 = "select id, latitude, longitude from Locations where id = {};".format(location_id)
            cur.execute(sql2)
            central_location = cur.fetchone()

        cur.close()
        conn.close()

        return render_template("map.html", locations=locations, central_location = central_location)

    return redirect(url_for("login"))

@app.route("/lyrics", methods=["GET"])
@login_required
def lyrics():
    if request.method == "GET":
        if User.name:
            username=User.name
            user = User(username)
            userid = user.get_id()   
        else:
            return redirect(url_for("login"))
        
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
            conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        sql = "select * from Lyrics where userid = {};".format(userid)
        cur.execute(sql)
        lyrics = cur.fetchone()

        num_of_lyrics = 31
        lyrics = lyrics[1:num_of_lyrics + 1]
        
        return render_template("lyrics.html", lyrics=lyrics)

    return redirect(url_for("login"))

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

            try:
                dbname = DB_NAME_LOCAL
                conn = sqlite3.connect(dbname)
            except sqlite3.OperationalError:
                dbname = DB_NAME_REMOTE
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
                User.name = username

                result = "<span class='text-success'>*</span> ユーザ登録に成功しました"
                conn.commit()

                user = User(username)
                userid = user.get_id()

                sql2 = "insert into Lyrics (userid) values ({});".format(userid)
                cur.execute(sql2)
                conn.commit()

                cur.close()
                conn.close()

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
                next = request.args.get("next")
                return redirect(next or url_for("main"))
        return render_template("login.html", result=result, username=username)
    else:
        if User.name:
            return render_template("login.html", username=User.name)
        else:
            return render_template("login.html")

@app.route("/config", methods=["GET", "POST"])
@login_required
def config():
    if User.name:
        current_username = User.name
        user = User(current_username)
        userid = str(user.get_id()).zfill(5)
    else:
        return redirect(url_for("login"))

    username = current_username
    try:
        dbname = DB_NAME_LOCAL
        conn = sqlite3.connect(dbname)
    except sqlite3.OperationalError:
        dbname = DB_NAME_REMOTE
        conn = sqlite3.connect(dbname)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    escaped_username =  username.replace("'", "''")
    sql = "select profile from Users where name = '{}';".format(escaped_username)
    cur.execute(sql)
    profile = cur.fetchone()["profile"]

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

                    result = "<span class='text-success'>*</span> ユーザ名を変更しました"
                    User.name = new_username
                    user = User(new_username)
                    username = new_username

                    escaped_username =  username.replace("'", "''")
                    sql = "select profile from Users where name = '{}';".format(escaped_username)
                    cur.execute(sql)
                    profile = cur.fetchone()["profile"]

                    cur.close()
                    conn.close()

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
        return render_template("config.html", userid = userid, username=username, result=result, profile=profile)
    else:
        if not profile:
            profile = ""
        return render_template("config.html", userid = userid, username=username, profile=profile)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    User.name = None
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    # serve(app, host="0.0.0.0", port=80)
