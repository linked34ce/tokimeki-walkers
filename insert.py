import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [
    "insert into Blog (id, title, body) values (1, '記事タイトル1', '内容1');",
    "insert into Blog (id, title, body) values (2, '記事タイトル2', '内容2');",
]

for sql in sqls:
    conn.execute(sql)
        
conn.commit()

cur.close()
conn.close()