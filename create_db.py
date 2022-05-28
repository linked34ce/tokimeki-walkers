import sqlite3

dbname = "main.db"

conn = sqlite3.connect(dbname)

conn.close()