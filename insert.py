import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1, 'ダイバーシティ 東京プラザ フェスティバル広場 大階段', 35.62473641001741, 139.77577529866684, '「フェスティバル広場 大階段」は、「ダイバーシティ 東京プラザ」の南側に……', 'TVアニメ1期第1話では、せつ菜が……', '/static/images/e1_setsuna.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (2, 'テレポートブリッジ', 35.62834509736082, 139.77891291795342, '「テレポートブリッジ」は、「東京テレポート駅」と……', 'TVアニメ1期第12話では、侑と歩夢が……', '/static/images/yupomu_bridge.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (3, 'ダイバーシティ 東京プラザ 東京テレポート駅ゲート', 35.62604666093716, 139.77628076815193, '「ダイバーシティ 東京プラザ」は、「東京テレポート駅」の近くにある商業施設であり……', 'TVアニメ1期のOPでは、せつ菜が……', '/static/images/op_setsuna.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (4, '出会い橋 ベンチ', 35.625380455852515, 139.77798891023804, '「出会い橋」は「センタープロムナード」上に位置する…', 'TVアニメ1期第13話では、「出会い橋」近くのベンチでしずくが…', '/static/images/shizukasu.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (5, 'ヴィーナスフォート 跡地', 35.62625254211352, 139.78058600919852, '「ヴィーナスフォート」はかつて存在した大型商業施設であり、', 'TVアニメ1期第7話では、彼方が「教会広場」で…', '/static/images/butterfly.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (6, 'パレットタウン 大観覧車 跡地', 35.627000087133936, 139.78171115627399, '「パレットタウン」の大観覧車は、2022年8月31日に営業を終了した…', 'TVアニメ2期第5話では、侑と歩夢は…', '/static/images/yupomu_wheel.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (7, 'クア・アイナ アクアシティお台場店', 35.62757065590007, 139.77240409762967, '「アクアシティお台場」にある飲食店のひとつ「クア・アイナ」は、…', 'TVアニメ2期のOPでは、ミアが店前のハンバーガーに…', '/static/images/mia_burger.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (8, 'ODAIBAゲーマーズ', 35.62970739624483, 139.77663811028083, '「ODAIBAゲーマーズ」は「デックス東京ビーチ」にあるアニメグッズのショップであり、…', 'TVアニメ1期第9話では、果林が道に迷い…', '/static/images/e9_karin.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (9, '東京ジョイポリス 入口', 35.62887412574503, 139.77552397702243, '「デックス東京ビーチ」にある屋内テーマパークである「東京ジョイポリス」は、…', 'TVアニメ1期第6話では、璃奈がソロライブを…', '/static/images/tsunagaru.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (10, '有明ガーデン 水のパレス', 35.638555582219425, 139.79296820718045, '「有明ガーデン」5Fにある噴水広場であり、…', 'TVアニメ2期第2話では、ランジュがこの場所でゲリラライブを開催し、…', '/static/images/e2_lanzhu.jpg');",
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