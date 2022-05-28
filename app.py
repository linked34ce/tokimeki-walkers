from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3
# import pytz

app = Flask(__name__)

def dict_factory(cursor, row):
   dic = {}
   for index, column in enumerate(cursor.description):
       dic[column[0]] = row[index]
   return dic

@app.route("/", methods=["GET"])
def blog():
    if request.method == "GET":
        dbname = "main.db"
        conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory

        cur = conn.cursor()
        sql = "select * from Blog;"
        cur.execute(sql)
        articles = cur.fetchall()
        cur.close()

        conn.close()

        return render_template("index.html", articles=articles)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")

        dbname = "main.db"
        conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory

        cur = conn.cursor()
        sql = "insert into Blog (title, body) values ('{}', '{}');".format(title, body)
        cur.execute(sql)
        cur.close()

        conn.commit()
        conn.close()

        return redirect("/")
    else:
        return render_template("create.html")
