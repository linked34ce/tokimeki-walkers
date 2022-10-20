# !~/tokimeki-walkers/.venv/bin/python3
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime, timedelta
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
from PIL import Image
from io import BytesIO

DB_NAME_REMOTE = "tokimeki-walkers/main.db"
DB_NAME_LOCAL  = "./main.db"
UPLOAD_FOLDER = "./static/uploads/"
BUCKET_NAME = "tokimeki-walkers"
BUCKET_URL = "https://tokimeki-walkers.s3.ap-northeast-1.amazonaws.com/"
BUCKET_UPLOAD = "/uploads/"
DIR_NAME = "static/cards/"
NO_IMAGE = "no_image.jpg"
NUM_OF_LYRICS = 47

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
    id = None
    name = None
    password = None

    def __init__(self, id):
        record = None
        userid_pattern = re.compile(r'^[a-zA-Z0-9]+$')

        if userid_pattern.match(id):
            try:
                dbname = DB_NAME_LOCAL
                conn = sqlite3.connect(dbname)
            except sqlite3.OperationalError:
                dbname = DB_NAME_REMOTE
                conn = sqlite3.connect(dbname)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            sql = "select * from Users where id = '{}';".format(id)
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
            self.id = None

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
        
def dict_factory(cursor, row):
   dic = {}
   for index, column in enumerate(cursor.description):
       dic[column[0]] = row[index]
   return dic

@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route("/", methods=["GET"])
@login_required
def main():
    if request.method == "GET":
        if User.id:
            userid = User.id
            user = User(userid)
            username = user.get_name()   
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
        sql1 = "select * from Locations left join Visits on Locations.id = Visits.location_id where userid = '{}';".format(userid)
        cur.execute(sql1)
        visits = cur.fetchall()
        sql2 = "select id from Locations;"
        cur.execute(sql2)
        locations = cur.fetchall()
        conn.row_factory = None
        cur = conn.cursor()
        sql3 = "select * from Lyrics where userid = '{}';".format(userid)
        cur.execute(sql3)
        lyrics = cur.fetchone()

        num_of_locations = len(locations)
        location_ids = []
        location_ids_with_photo = []
        num_of_visited_locs = 0
        num_of_photos = 0
        for visit in visits:
            if visit["location_id"] not in location_ids:
                location_ids.append(visit["location_id"])
                num_of_visited_locs += 1
            if visit["location_id"] not in location_ids_with_photo:
                if visit["photo"] != NO_IMAGE:
                    location_ids_with_photo.append(visit["location_id"])
                    num_of_photos += 1

        lyrics = lyrics[1:NUM_OF_LYRICS + 1]

        return render_template("index.html", username=username, num_of_locations=num_of_locations,
                num_of_visited_locs=num_of_visited_locs, num_of_photos=num_of_photos, lyrics=lyrics)

@app.route("/rally", methods=["GET"])
@login_required
def rally():
    if request.method == "GET":
        if User.id:
            userid = User.id
            user = User(userid)
            username = user.get_name()
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

        for location in locations:
            sql2 = "select * from Locations left join Visits on Locations.id = Visits.location_id where userid = '{}' and location_id = '{}' order by time desc;".format(userid, location["id"])
            cur.execute(sql2)
            visits = cur.fetchall()
            location["visit_count"] = len(visits)
            if location["visit_count"] > 0:
                location["visited"] = "✅ 訪問済"
            else:
                location["visited"] = "⚠️ 未訪問"
                location["share_button"] = " disabled"     
            if not visits:
                location["photo"] = NO_IMAGE
            elif not visits[0]["photo"]:
                location["photo"] = NO_IMAGE
            else:
                location["photo"] = visits[0]["photo"]

        cur.close()
        conn.close()

        return render_template("rally.html", username=username, locations=locations)

@app.route("/post/<int:location_id>", methods=["POST"])
@login_required
def post(location_id):
    if request.method == "POST":
        if User.id:
            userid = User.id
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

        escaped_content =  content.replace("'", "''")
        sql1 = "select * from Locations left join Visits on Locations.id = Visits.location_id where userid = '{}' and location_id = '{}' order by time desc;".format(userid, location_id)
        cur.execute(sql1)
        latest_visit = cur.fetchone()
        location_id = latest_visit["location_id"]
        photo = latest_visit["photo"]

        sql2 = "insert into Posts (userid, location_id, content, photo) values ('{}', {}, '{}', '{}');".format(userid,location_id, escaped_content, photo)
        cur.execute(sql2)
        conn.commit()
        cur.close()
        conn.close()
    
        return redirect(url_for("rally"))
    else:
        return redirect(url_for("login"))

@app.route("/rally/<int:location_id>/<int:unlocked_number>", methods=["GET"])
@login_required
def detail(location_id, unlocked_number=0):
    if request.method == "GET":
        if User.id:
            userid = User.id
            user = User(userid)
            username = user.get_name()
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

        sql1 = "select * from Locations left join Visits on Locations.id = Visits.location_id where location_id = {} and userid = '{}' order by time desc;".format(location_id, userid)
        cur.execute(sql1)
        visits = cur.fetchall()
        sql3 = "select * from Locations where id = {}".format(location_id)
        cur.execute(sql3)
        location = cur.fetchone()

        sql4 = "select * from Locations where id != {};".format(location_id)
        cur.execute(sql4)
        locations = cur.fetchall()
        cur.close()
        conn.close()

        location["visit_count"] = len(visits)
        if visits:
            location["photo"] = visits[0]["photo"]
            utc_time = datetime.strptime(visits[0]["time"], "%Y-%m-%d %H:%M:%S")
            jst_time = utc_time + timedelta(hours=9)
            location["last_visit"] = jst_time

        location["visit_count_with_photo"] = 0
        for visit in visits:
            if visit["photo"] != NO_IMAGE:
                location["visit_count_with_photo"] += 1

        if location["visit_count"] < 1:
            message = "⚠️ この聖地は未訪問です"
        else:
            message = "✅ この聖地は{}回訪問済みです".format(location["visit_count"])

        for i in range(len(locations)): 
            distance = hubeny_formula(location["latitude"], location["longitude"], 
                                        locations[i]["latitude"], locations[i]["longitude"])
            locations[i]["distance"] = distance

        locations.sort(key=lambda x: x["distance"])
        nearest_locations = locations[0:3]
        for i in range(3): 
            nearest_locations[i]["distance"] = "{:,}".format(round(nearest_locations[i]["distance"]))

        return render_template("detail.html", username=username, location=location, message=message, 
                                nearest_locations=nearest_locations, unlocked_number=unlocked_number)

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
        if not User.id:
            return redirect(url_for("login"))
        
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
            conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql1 = "select Posts.id, userid, content, photo, time, location_id, name as location_name from Posts inner join Locations on Posts.location_id = Locations.id order by time desc;"
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
            utc_time = datetime.strptime(post["time"], "%Y-%m-%d %H:%M:%S")
            jst_time = utc_time + timedelta(hours=9)
            post["time"] = jst_time
            sql3 = "select id, name, profile from Users where id = '{}';".format(post["userid"])
            cur.execute(sql3)
            poster = cur.fetchone()
            post["userid"] = poster["id"]
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
        if User.id:
            userid = User.id
            photo = NO_IMAGE
            try:
                dbname = DB_NAME_LOCAL
                conn = sqlite3.connect(dbname)
            except sqlite3.OperationalError:
                dbname = DB_NAME_REMOTE
                conn = sqlite3.connect(dbname)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            sql = "insert into Visits (userid, location_id, photo) values ('{}', {}, '{}');".format(userid, location_id, photo)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            unlocked_number = 0
        else:
            return redirect(url_for("login"))
        return redirect(url_for("detail", location_id=location_id,  unlocked_number=unlocked_number))

def createHTML(filename):
    html = "<html lang='ja'><head><meta charset='utf-8'>"
    html += "<meta name='twitter:title' content='TOKIMEKI Walkers'>"
    html += "<meta name='og:description' content='聖地巡礼を支援するARフォトスタンプラリーシステム'>"
    html += "<meta name='twitter:card' content='summary_large_image'>"
    html += "<meta name='og:image' content='{}'>".format(BUCKET_URL + BUCKET_UPLOAD + filename)
    html += "</head><script>window.addEventListener('onload', location.href = '/');</script></html>"
    return html

@app.route("/upload/<int:location_id>", methods=["POST"])
@login_required
def upload(location_id):
    if request.method == "POST":
        if User.id:
            file = request.files["photo"]
            filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            with open(UPLOAD_FOLDER + filename, 'rb') as inputfile:
                im = Image.open(inputfile)
                im_io = BytesIO()
                im.save(im_io, 'JPEG', quality=30)
            with open(UPLOAD_FOLDER + filename, mode='wb') as outputfile:
                outputfile.write(im_io.getvalue()) 
            try:
                client.upload_file(UPLOAD_FOLDER + filename, BUCKET_NAME, BUCKET_UPLOAD + filename, 
                ExtraArgs={"ContentType": "image/jpeg", "ACL": "public-read"})
                with open(DIR_NAME + filename + ".html", mode="w") as f:
                    f.write(createHTML(filename))
            except botocore.exceptions.NoCredentialsError:
                pass
            os.remove(UPLOAD_FOLDER + filename)

            userid = User.id
            try:
                dbname = DB_NAME_LOCAL
                conn = sqlite3.connect(dbname)
            except sqlite3.OperationalError:
                dbname = DB_NAME_REMOTE
                conn = sqlite3.connect(dbname)
            cur = conn.cursor()
            sql1 = "insert into Visits (userid, location_id, photo) values ('{}', {}, '{}');".format(userid, location_id, filename)
            cur.execute(sql1)

            sql2 = "select * from Locations left join Visits on Locations.id = Visits.location_id where location_id = {} and userid = '{}' and photo != '{}' order by time desc;".format(location_id, userid, NO_IMAGE)
            cur.execute(sql2)
            visits_with_photo = cur.fetchall()

            sql3 = "select * from lyrics where userid = '{}';".format(userid)
            cur.execute(sql3)
            lyrics = cur.fetchone()
            unlocked_number = 0

            if len(visits_with_photo) < 2:
                numbers = []
                for i in range(1, NUM_OF_LYRICS + 1):
                    if not lyrics[i]:
                        numbers.append(i)
                if len(numbers) > 0:
                    unlocked_number = numbers[randint(0, len(numbers) - 1)]
                    sql4 = "update Lyrics set lyric{} = 1 where userid = '{}';".format(unlocked_number, userid)
                    cur.execute(sql4)

            conn.commit()
            cur.close()
            conn.close()
        else:
            return redirect(url_for("login"))
    return redirect(url_for("detail", location_id=location_id, unlocked_number=unlocked_number))
    
@app.route("/map/<int:location_id>", methods=["GET"])
@login_required
def map(location_id):
    if request.method == "GET":
        if not User.id:
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
                "latitude": 35.636930005936414, 
                "longitude": 139.77782556878714
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
        if User.id:
            userid = User.id
        else:
            return redirect(url_for("login"))
        
        try:
            dbname = DB_NAME_LOCAL
            conn = sqlite3.connect(dbname)
        except sqlite3.OperationalError:
            dbname = DB_NAME_REMOTE
            conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        sql = "select * from Lyrics where userid = '{}';".format(userid)
        cur.execute(sql)
        lyrics = cur.fetchone()

        lyrics = lyrics[1:NUM_OF_LYRICS + 1]
        
        return render_template("lyrics.html", lyrics=lyrics)

    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        userid = request.form.get("userid")
        password = request.form.get("password")
        password_confirm = request.form.get("password-confirm")

        result = "<span class='text-danger'>*</span> "
        userid_pattern = re.compile(r'^[a-zA-Z0-9]+$')
        password_pattern = re.compile(r'^[a-zA-Z0-9]+$')

        if not userid or not password or not password_confirm:
            result += "すべての項目を入力してください"
        elif not userid_pattern.match(userid):
            result += "ユーザIDは半角英数字で入力してください"
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
            sql1 = "insert into Users (id, name, password, profile) values ('{}', '{}', '{}', '');".format(userid, userid, password_hash)

            try:
                cur.execute(sql1)
            except sqlite3.IntegrityError:
                result += 'ユーザID "{}" はすでに使用されています'.format(userid)
                userid = ""
                cur.close()
                conn.close()
            else:
                User.id = userid

                result = "<span class='text-success'>*</span> ユーザ登録に成功しました"
                conn.commit()

                sql2 = "insert into Lyrics (userid) values ('{}');".format(userid)
                cur.execute(sql2)
                conn.commit()

                cur.close()
                conn.close()

        return render_template("signup.html", result=result, userid=userid)
    else:
        return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userid = request.form.get("userid")
        password = request.form.get("password")
        user = User(userid)
        User.id = userid

        result = "<span class='text-danger'>*</span> "
        password_pattern = re.compile(r'^[a-zA-Z0-9]+$')

        if not userid and not password:
            result += "ユーザIDとパスワードを入力してください"
            userid = ""
        elif not userid:
            result += "ユーザIDを入力してください"
            userid = ""
        elif not password:
            result += "パスワードを入力してください"
        elif len(password) < 8 or not password_pattern.match(password):
            result += "パスワードは8文字以上の半角英数字です"
        elif not user.id:
            result += 'ユーザID "{}" は登録されていません'.format(userid)
            userid = ""
        elif user.password:
            if not check_password_hash(user.password, password):
                result += "パスワードに誤りがあります"
            elif user.id:
                login_user(user)
                next = request.args.get("next")
                return redirect(next or url_for("main"))
        return render_template("login.html", result=result, userid=userid)
    else:
        if User.id:
            return render_template("login.html", userid=User.id)
        else:
            return render_template("login.html")

@app.route("/config", methods=["GET", "POST"])
@login_required
def config():
    if User.id:
        userid = User.id
        user = User(userid)
        current_username = user.get_name()
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

    sql = "select profile from Users where id = '{}';".format(userid)
    cur.execute(sql)
    profile = cur.fetchone()["profile"]

    if request.method == "POST":
        result = "<span class='text-danger'>*</span> "
        if request.form.get("username"):
            new_username = request.form.get("username")
            username_pattern = re.compile(r'^(?!.*(\s)).*$')
            if not new_username:
                new_username = ""
            escaped_new_username =  new_username.replace("'", "''")
            profile = request.form.get("profile")

            sql = "update Users set name = '{}' where id = '{}';".format(escaped_new_username, userid)

            if not username_pattern.match(new_username):
                result += "表示名に空白文字は使用できません"
    
            else:
                cur.execute(sql)
                conn.commit()

                result = "<span class='text-success'>*</span> 表示名を変更しました"
                User.name = new_username
                current_username = new_username

            sql = "select profile from Users where id = '{}';".format(userid)
            cur.execute(sql)
            profile = cur.fetchone()["profile"]  
            cur.close()
            conn.close()

        else:
            profile = request.form.get("profile")
            if not profile:
                profile = ""
            escaped_profile = profile.replace("'", "''")
            sql = "update Users set profile = '{}' where id = '{}';".format(escaped_profile, userid)
            cur.execute(sql)
            conn.commit()
            result = "<span class='text-success'>*</span> プロフィールを変更しました"
            cur.close()
            conn.close()
        return render_template("config.html", userid=userid, username=current_username, result=result, profile=profile)
    else:
        if not profile:
            profile = ""
        return render_template("config.html", userid=userid, username=current_username, profile=profile)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    User.id = None
    return redirect(url_for("login"))

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=80, debug=True, threaded=True)
    serve(app, host="0.0.0.0", port=80, threads=5)
