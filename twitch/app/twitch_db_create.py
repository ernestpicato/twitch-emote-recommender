import csv
import sqlite3

conn = sqlite3.connect('twitch.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS twitch""")
cur.execute("""CREATE TABLE twitch
            (id integer, name text, url text, rec1 text, rec2 text, rec3 text, rec4 text, rec5 text, rec6 text, rec7 text, rec8 text,rec9 text, rec10 text)""")

with open('../../twitch.csv', 'r') as f:
    reader = csv.reader(f.readlines()[1:])  # exclude header line
    cur.executemany("""INSERT INTO twitch VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (row for row in reader))
conn.commit()
conn.close()
