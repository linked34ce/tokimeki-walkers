
import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [ 
   "create table Users (id varchar(64) primary key, session_token varchar(100) not null unique, name varchar(64) not null, password varchar(128) not null, profile varchar(1024));",
   "create table Locations (id integer primary key, name varchar(64) not null unique, latitude double not null, longitude double not null, summary varchar(1024) not null, scene varchar(1024) not null, image varchar(128) not null);",
   "create table Visits (userid varchar(64) not null, location_id int not null, photo varchar(128) not null, time datettime not null default current_timestamp);",
   "create table Posts (id integer primary key, userid varchar(64) not null, location_id int not null, content varchar(1024) not null, photo varchar(128) not null, time datetime not null default current_timestamp);",
   "create table Lyrics (userid varchar(64) primary key, lyric1 integer not null default 0, lyric2 integer not null default 0, lyric3 integer not null default 0, lyric4 integer not null default 0, lyric5 integer not null default 0, lyric6 integer not null default 0, lyric7 integer not null default 0, lyric8 integer not null default 0, lyric9 integer not null default 0, lyric10 integer not null default 0, lyric11 integer not null default 0, lyric12 integer not null default 0, lyric13 integer not null default 0, lyric14 integer not null default 0, lyric15 integer not null default 0, lyric16 integer not null default 0, lyric17 integer not null default 0, lyric18 integer not null default 0, lyric19 integer not null default 0, lyric20 integer not null default 0, lyric21 integer not null default 0, lyric22 integer not null default 0, lyric23 integer not null default 0, lyric24 integer not null default 0, lyric25 integer not null default 0, lyric26 integer not null default 0, lyric27 integer not null default 0, lyric28 integer not null default 0, lyric29 integer not null default 0, lyric30 integer not null default 0, lyric31 integer not null default 0, lyric32 integer not null default 0, lyric33 integer not null default 0, lyric34 integer not null default 0, lyric35 integer not null default 0, lyric36 integer not null default 0, lyric37 integer not null default 0, lyric38 integer not null default 0, lyric39 integer not null default 0, lyric40 integer not null default 0, lyric41 integer not null default 0, lyric42 integer not null default 0, lyric43 integer not null default 0, lyric44 integer not null default 0, lyric45 integer not null default 0, lyric46 integer not null default 0, lyric47 integer not null default 0);"
]

for sql in sqls:
    try:
        conn.execute(sql)
    except sqlite3.OperationalError:
        continue
    
conn.commit()

cur.close()
conn.close()