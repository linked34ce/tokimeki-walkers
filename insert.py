import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1, 'フェスティバル広場 大階段 (ダイバーシティ 東京プラザ)', 35.62473641001741, 139.77577529866684, '「フェスティバル広場 大階段」は、「ダイバーシティ 東京プラザ」の南側に……', 'TVアニメ1期第1話では、せつ菜が……', '/static/images/e1_setsuna.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (2, 'テレポートブリッジ', 35.62830780074858, 139.77898586218663, '「テレポートブリッジ」は、「東京テレポート駅」と……', 'TVアニメ1期第12話では、侑と歩夢が……', '/static/images/yupomu.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (3, 'ダイバーシティ 東京プラザ (東京テレポート駅ゲート)', 35.62595157098818, 139.77626504706365, '「ダイバーシティ 東京プラザ」は、「東京テレポート駅」の近くにある商業施設であり……', 'TVアニメ1期のOPでは、せつ菜が……', '/static/images/op_setsuna.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1001, '五反野駅', 35.7661718455244, 139.8092444128288, '東武スカイツリーラインの駅', 'そんなものはない', '/static/images/no_image.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1002, '宮治研究室', 35.565609041475724, 139.403112914213, '「相模原キャンパスO棟」に位置している', '当然そんなものはない', '/static/images/no_image.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1003, 'テスト空間', 35.764763179856395, 139.8111013846989, 'テストテスト', 'もちろんそんなものはない', '/static/images/no_image.jpg');",
]

for sql in sqls:
    try:
        conn.execute(sql)
    except sqlite3.IntegrityError:
        continue
        
conn.commit()

cur.close()
conn.close()