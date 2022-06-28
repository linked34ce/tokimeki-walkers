
import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [ 
   "create table Users (id integer primary key, name varchar(64) not null unique, password varchar(128) not null, profile varchar(1024));",
   "create table Locations (id integer primary key, name varchar(64) not null unique, latitude double not null, longitude double not null, summary varchar(1024) not null, scene varchar(1024) not null, image varchar(128) not null);",
   "create table Visits (username varchar(64) not null, location_id int not null, photo varchar(128) not null, time datettime not null default current_timestamp, lyric integer);",
   "create table Posts (id integer primary key, userid integer, content varchar(1024) not null, photo varchar(128) not null, time datetime not null default current_timestamp);",
   "create table Lyrics (userid integer primary key, lyric1 integer not null default 0, lyric2 integer not null default 0, lyric3 integer not null default 0, lyric4 integer not null default 0, lyric5 integer not null default 0, lyric6 integer not null default 0, lyric7 integer not null default 0, lyric8 integer not null default 0, lyric9 integer not null default 0, lyric10 integer not null default 0, lyric11 integer not null default 0, lyric12 integer not null default 0, lyric13 integer not null default 0, lyric14 integer not null default 0, lyric15 integer not null default 0, lyric16 integer not null default 0, lyric17 integer not null default 0, lyric18 integer not null default 0, lyric19 integer not null default 0, lyric20 integer not null default 0, lyric21 integer not null default 0, lyric22 integer not null default 0, lyric23 integer not null default 0, lyric24 integer not null default 0, lyric25 integer not null default 0, lyric26 integer not null default 0, lyric27 integer not null default 0, lyric28 integer not null default 0, lyric29 integer not null default 0, lyric30 integer not null default 0, lyric31 integer not null default 0, lyric32 integer not null default 0, lyric33 integer not null default 0, lyric34 integer not null default 0, lyric35 integer not null default 0, lyric36 integer not null default 0, lyric37 integer not null default 0, lyric38 integer not null default 0, lyric39 integer not null default 0, lyric40 integer not null default 0, lyric41 integer not null default 0, lyric42 integer not null default 0, lyric43 integer not null default 0, lyric44 integer not null default 0, lyric45 integer not null default 0, lyric46 integer not null default 0, lyric47 integer not null default 0, lyric48 integer not null default 0, lyric49 integer not null default 0, lyric50 integer not null default 0, lyric51 integer not null default 0, lyric52 integer not null default 0, lyric53 integer not null default 0, lyric54 integer not null default 0, lyric55 integer not null default 0, lyric56 integer not null default 0, lyric57 integer not null default 0, lyric58 integer not null default 0, lyric59 integer not null default 0, lyric60 integer not null default 0, lyric61 integer not null default 0, lyric62 integer not null default 0, lyric63 integer not null default 0, lyric64 integer not null default 0, lyric65 integer not null default 0, lyric66 integer not null default 0, lyric67 integer not null default 0, lyric68 integer not null default 0, lyric69 integer not null default 0, lyric70 integer not null default 0, lyric71 integer not null default 0, lyric72 integer not null default 0, lyric73 integer not null default 0, lyric74 integer not null default 0, lyric75 integer not null default 0, lyric76 integer not null default 0, lyric77 integer not null default 0, lyric78 integer not null default 0, lyric79 integer not null default 0, lyric80 integer not null default 0, lyric81 integer not null default 0, lyric82 integer not null default 0, lyric83 integer not null default 0, lyric84 integer not null default 0, lyric85 integer not null default 0, lyric86 integer not null default 0, lyric87 integer not null default 0, lyric88 integer not null default 0, lyric89 integer not null default 0, lyric90 integer not null default 0, lyric91 integer not null default 0, lyric92 integer not null default 0, lyric93 integer not null default 0, lyric94 integer not null default 0, lyric95 integer not null default 0, lyric96 integer not null default 0, lyric97 integer not null default 0, lyric98 integer not null default 0, lyric99 integer not null default 0, lyric100 integer not null default 0);"
]

for sql in sqls:
    try:
        conn.execute(sql)
    except sqlite3.OperationalError:
        continue
    
conn.commit()

cur.close()
conn.close()