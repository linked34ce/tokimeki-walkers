
import sqlite3

dbname = "main.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

sqls = [ 
   "create table Users (id integer primary key, name varchar(50) not null unique, password varchar(25));"
   # "create table Locations (id integer primary key, name verchar(50) not null unique, latitude double not null, longitude double not null, summary varchar(500) not null, scene varchar(500) not null, image varchar(100) not null);",
   # "create table Visits (username varchar(50) not null, location_id int not null, photo varchar(100) not null, visit_count int not null default 0, last_visit datettime not null default current_timestamp, primary key(username, location_id));"
]

for sql in sqls:
    cur.execute(sql)
    
conn.commit()

cur.close()
conn.close()