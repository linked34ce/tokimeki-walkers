# -*- coding: utf-8 -*-

import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (1, '有明西ふ頭公園 霧の噴水広場', 35.627207058157886, 139.79434564243581, '　有明西ふ頭公園は、東京ビッグサイトや有明客船ターミナルに隣接する細長い海上公園です。海岸部では、年間を通して釣りを楽しむことができます。<br>　公園の中心に位置する霧の噴水広場は石柱のようなオブジェが特徴的ですが、ここ数年は誰も霧が出たのを見たことがないようです。', '　1期OPの歌い出しで、かすみとしずくが登場する場所です。下から飛び出してきて、手を繋ぎながらポーズを取る2人の姿が印象的です。<br><br><span class=\"fst-italic\">　\"青空 雨あがり 希望の風吹いて\"</span>', 'season1_opening_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (2, 'TFTビル東館 2階', 35.630495664875234, 139.79107817472897, '　TFTビルは、1996年に東京ファッションタウン株式会社が開業したビルです。しかし大幅な赤字が続いたため、2000年には当ビルの業務は株式会社東京ビッグサイトに委託されました。<br>　現在ではオフィスやホールの貸し出しだけでなく、レストランやクリニックが集う複合施設となっています。', '　1期OPにて歩夢が登場する場所です。この時の歩夢の笑顔は、まさに開花宣言です。背景には作中で虹ヶ咲学園駅として登場するゆりかもめ 東京ビッグサイト駅が見えます。<br>　またこの付近にあるプロント ワンザ有明店は、2期12話にて劇伴『未来ハーモニー with YOU』が流れ、侑と歩夢、そしてランジュの3人が駆け出すシーンに登場しています。<br><br><span class=\"fst-italic\">　\"予感の中 踏みだすよ 最初の一歩\"</span>', 'season1_opening_scene02.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (3, 'セブン-イレブン ROYAL東京ビッグサイト店', 35.62957322139265, 139.79340752996296, '', '', 'season1_opening_scene03.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (4, 'ダイバーシティ東京 プラザ 東京テレポート駅ゲート', 35.62604666093716, 139.77628076815193, '', '', 'season1_opening_scene04.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (5, '旧パレットタウン 北側入口', 35.62625254211352, 139.78058600919852, '', '', 'season1_opening_scene05.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (6, 'ウエストプロムナード 滝の広場 ROUND STRUCTURE', 35.61881491414985, 139.77857824711532, '', '', 'season1_opening_scene06.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (7, '東京ジョイポリス 入口', 35.62887412574503, 139.77552397702243, '', '', 'season1_opening_scene07.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (8, '水の広場公園 東側エリア 虹のベンチ', 35.62972710733615, 139.79168347468269, '', '', 'season2_opening_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (9, 'ヒルトン東京お台場 エントランス付近通路', 35.62668655343901, 139.77156013321218, '', '', 'season2_opening_scene02.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (10, '青海南ふ頭公園 壁泉', 35.616427534101256, 139.7818233998068, '', '', 'season2_opening_scene03.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (11, 'クア・アイナ アクアシティお台場店', 35.62757726701679, 139.77241717910024, '', '', 'season2_opening_scene04.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (12, '豊洲六丁目公園', 35.646717801770045, 139.79251675982312, '', '', 'season2_opening_scene05.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (13, '新豊洲Brilliaランニングスタジアム 入口', 35.64857326462276, 139.78633649040245, '', '', 'season2_opening_scene06.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (14, 'グランドニッコー東京 台場 ヴェルエクール', 35.6258696480714, 139.77210079510047, '', '', 'season2_opening_scene07.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (15, '晴海トリトン 花のテラス', 35.657925984569566, 139.78224916497845, '', '', 'season2_opening_scene08.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (16, '有明ガーデン ウェルカムデッキ', 35.63747191390529, 139.79266771957623, '', '', 'season2_opening_scene09.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (17, 'アクアシティお台場 カフェ ラ・ボエム付近通路', 35.628345593759455, 139.77419416917553, '', '', 'season2_opening_scene10.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (18, '海浜公園入口交差点', 35.63045481906742, 139.77923867586776, '', '', 'season2_opening_scene11.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (19, '東京都観光汽船 豊洲船着場', 35.65524889937721, 139.79130221274397, '', '', 'season2_opening_scene12.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (20, 'ダイバーシティ東京 プラザ フェスティバル広場 大階段', 35.62473641001741, 139.77577529866684, '', '', 'season1_episode01_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (21, '東雲キャナルコートCODAN 17号棟 階段', 35.64722040153612, 139.80363093673336, '', '', 'season1_episode01_scene02.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (22, '潮風公園 十三号地公園記念碑', 35.62448149473435, 139.76855057738013, '', '', 'season1_episode02_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (23, '東京ビッグサイト 西展示棟 屋上展示場 ベンチ', 35.62919205043969, 139.79457784766458, '', '', 'season1_episode03_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (24, 'レインボープロムナード サウスルート P28 橋脚', 35.63473578688042, 139.76984719296104, '', '', 'season1_episode04_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (25, '日本科学未来館 チケットブース', 35.61988445509895, 139.77699655191037, '', '', 'season1_episode05_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (26, 'ブリリア有明シティタワー エントランス付近交差点', 35.63606538564646, 139.7835424336705, '', '', 'season1_episode06_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (27, 'イーストプロムナード やぐら橋', 35.630680522099695, 139.7933480753246, '', '', 'season1_episode07_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (28, '水の広場公園 東側エリア カスケード広場', 35.628583151605284, 139.78645529277304, '', '', 'season1_episode08_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (29, 'ODAIBAゲーマーズ', 35.62974893441139, 139.77667112965884, '', '', 'season1_episode09_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (30, '東京ビッグサイト 庭園', 35.63114115870027, 139.79450657730985, '', '', 'season1_episode10_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (31, '都営バス 東雲一丁目 東京テレポート駅前方面', 35.64677018983122, 139.8016213410817, '', '', 'season1_episode11_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (32, '有明客船ターミナル 連絡橋', 35.62976429159761, 139.79266508679885, '', '', 'season1_episode12_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (33, 'センタープロムナード テレポートブリッジ', 35.62830090968482, 139.7789249838268, '', '', 'season1_episode12_scene02.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (34, 'センタープロムナード 出会い橋 ベンチ', 35.62538060216976, 139.77798457634054, '', '', 'season1_episode13_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (35, '東京ビッグサイト 東展示棟 ガレリア', 35.632306436601084, 139.79865666482866, '', '', 'season2_episode01_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (36, '有明ガーデン 水のパレス', 35.63859083448497, 139.7929466383539, '', '', 'season2_episode02_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (37, '東雲公園', 35.64343896746866, 139.79831746983552, '', '', 'season2_episode02_scene02.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (38, '東京国際クルーズターミナル 送迎デッキ', 35.61708186933497, 139.7713148966425, '', '', 'season2_episode03_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (39, 'ウエストプロムナード  東京国際交流館前ベンチ', 35.621222829569874, 139.77690475971895, '', '', 'season2_episode04_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (40, 'ダイワロイネットホテル 東京有明 国際展示場駅側階段', 35.63420722252246, 139.79253276872237, '', '', 'season2_episode05_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (41, '東京ビッグサイト 西展示棟 屋上展示場 雲のオブジェ', 35.628832768821674, 139.7937575144821, '', '', 'season2_episode06_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (42, 'シーフォートスクエア センターコート', 35.62380344678849, 139.7512512453381, '', '', 'season2_episode07_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (43, '東京ビッグサイト 会議棟 電光掲示板下階段', 35.63024907173829, 139.7941468589009, '', '', 'season2_episode08_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (44, 'お台場海浜公園 西側エリア 芝生広場', 35.62724222455328, 139.77076665787138, '', '', 'season2_episode09_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (45, '東京ビッグサイト 西展示棟 アトリウム', 35.62905944738038, 139.7945661920029, '', '', 'season2_episode10_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (46, '東京観光汽船 お台場海浜公園船着場', 35.62924440870841, 139.77385850043026, '', '', 'season2_episode11_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (47, 'ダイバーシティ東京 オフィスタワー エントランス', 35.62500091895647, 139.776984712412, '', '', 'season2_episode11_scene02.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (48, 'お台場海浜公園 おだいばビーチ', 35.6309282376182, 139.7767641071071, '', '', 'season2_episode12_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (49, '青海南ふ頭公園  展望広場 デザインウォール', 35.61501783216955, 139.77640804146432, '', '', 'season2_episode13_scene01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (50, 'ゆりかもめ 東京ビックサイト駅 ホーム', 35.630282750677054, 139.791430529139, '', '', 'other01.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (51, 'レインボープロムナード 台場口 南北ルート分岐点', 35.635861870812505, 139.77502515910098, '', '', 'other02.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (52, '豊洲ぐるり公園', 35.641092292836454, 139.77756911175618, '', '', 'other03.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (53, 'お台場海浜公園 展望デッキ', 35.627699882191145, 139.7715381026066, '', '', 'other04.jpg');",
    "insert into Locations (id, name, latitude, longitude, summary, scene, image) values (54, 'お台場海浜公園 自由の女神像', 35.6277257618083, 139.77189461779116, '', '', 'other05.jpg');"
]

for sql in sqls:
    try:
        conn.execute(sql)
    except sqlite3.IntegrityError:
        continue
        
conn.commit()

cur.close()
conn.close()