import _sqlite3
import sqlite3

# tworzymy połączenie z bazą sqlite zapisuje wszystko w pliku dlatego nazwijmy ten plik "data.db"
connection = _sqlite3.connect("data.db")

cursor = connection.cursor()

# create_table = "CREATE TABLE users (id int, username text, password text)"
#
# cursor.execute(create_table)

# user = (1, "admin", "admin")
# insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# cursor.execute(insert_query, user)
# connection.commit()
# connection.close()

# user = [(2, "admin", "admin"), (3, "admin", "admin")]
# insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# cursor.executemany(insert_query, user)
# connection.commit()
# connection.close()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS movies (name text, genre text)"
cursor.execute(create_table)

connection.commit()
connection.close()
