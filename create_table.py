
import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [ 
   "create table Users (id integer primary key, name varchar(64) not null unique, password varchar(128) not null, profile varchar(1024));",
   "create table Locations (id integer primary key, name verchar(64) not null unique, latitude double not null, longitude double not null, summary varchar(1024) not null, scene varchar(1024) not null, image varchar(128) not null);",
   "create table Visits (username varchar(64) not null, location_id int not null, photo varchar(128) not null, time datettime not null default current_timestamp);",
   "create table Posts (id integer primary key, userid integer, content varchar(1024) not null, photo varchar(128) not null, time datetime not null default current_timestamp);"
]

for sql in sqls:
    try:
        conn.execute(sql)
    except sqlite3.OperationalError:
        continue
    
conn.commit()

cur.close()
conn.close()