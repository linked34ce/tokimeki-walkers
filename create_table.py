
import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [
    "create table Blog (id integer primary key, title varchar(50) not null, body varchar(500) not null, created_at datetime not null default current_timestamp);"
]

for sql in sqls:
    cur.execute(sql)
    
conn.commit()

cur.close()
conn.close()