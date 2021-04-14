import sqlite3
import json

DB_FILENAME = "rick_and_morty.db"
db_path = f"./{DB_FILENAME}"

con = sqlite3.connect('bla.db')
cur = con.cursor()

cur.execute('''
        CREATE TABLE IF NOT EXISTS characters
            (id INTEGER PRIMARY KEY, name TEXT, status TEXT, species TEXT, type TEXT, gender TEXT, image TEXT)
''')

page = 1
json_file = "characters.{page}.json"
while True:
    with open(json_file.format(page=page), "r") as data_file:
        characters = json.loads(data_file.read())
    data_table = [( character['id'], character['name'], character['status'], character['species'], character['type'], character['gender'], character['image']) for character in characters]
    cur.executemany('INSERT INTO characters VALUES (?,?,?,?,?,?,?)', data_table)
    con.commit()
    page += 1

print("close file")
con.close()
