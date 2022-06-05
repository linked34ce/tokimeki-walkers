import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1, 'ダイバーシティ 東京プラザ フェスティバル広場 大階段', 35.6247194, 139.7712958, '「フェスティバル広場 大階段」は、「ダイバーシティ 東京プラザ」の南側に……', 'TVアニメ1期第1話では、せつ菜が……', 'tmp/setsuna.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (2, 'テレポートブリッジ', 35.627783, 139.7777875, '「テレポートブリッジ」は、「東京テレポート駅」と……', 'TVアニメ1期第12話では、侑と歩夢が……', 'tmp/yupomu.jpg');"
]

for sql in sqls:
    conn.execute(sql)
        
conn.commit()

cur.close()
conn.close()