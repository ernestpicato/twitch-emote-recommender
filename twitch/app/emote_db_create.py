import csv
import sqlite3

conn = sqlite3.connect('emotes.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS emotes""")
cur.execute("""CREATE TABLE emotes
            (name text, emote text, url text)""")

with open('../../emotes.csv', 'r') as f:
    reader = csv.reader(f.readlines()[1:])  # exclude header line
    cur.executemany("""INSERT INTO emotes VALUES (?,?,?)""",
                    (row for row in reader))
conn.commit()
conn.close()
