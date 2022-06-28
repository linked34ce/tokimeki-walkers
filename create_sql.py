result = "create table Lyrics (userid integer primary key"

for i in range(1, 101):
    result +=  ", lyric{} integer not null default 0".format(i)

result += ");"

print(result)