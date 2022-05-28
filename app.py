from flask import Flask
from flask import render_template
from datetime import datetime
import sqlite3
# import pytz

app = Flask(__name__)

def dict_factory(cursor, row):
   dic = {}
   for index, column in enumerate(cursor.description):
       dic[column[0]] = row[index]
   return dic

@app.route("/")
def blog():
    dbname = "main.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    sql = "select * from Blog;"
    cur.execute(sql)
    articles = cur.fetchall()
    return render_template("index.html", articles=articles)