import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1, 'ダイバーシティ 東京プラザ フェスティバル広場 大階段', 35.6247194, 139.7712958, '「フェスティバル広場 大階段」は、「ダイバーシティ 東京プラザ」の南側に……', 'TVアニメ1期第1話では、せつ菜が……', 'static/tmp/setsuna.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (2, 'テレポートブリッジ', 35.627783, 139.7777875, '「テレポートブリッジ」は、「東京テレポート駅」と……', 'TVアニメ1期第12話では、侑と歩夢が……', 'static/tmp/yupomu.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1001, '五反野駅', 35.7646419, 139.8086757, '東武スカイツリーラインの駅', 'そんなものはない', 'static/tmp/no_image.png');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1002, '宮治研究室', 35.5662249, 139.4023064, '「相模原キャンパスO棟」に位置している', 'そんなものはない', 'static/tmp/no_image.png');"
]

for sql in sqls:
    conn.execute(sql)
        
conn.commit()

cur.close()
conn.close()