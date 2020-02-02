import _sqlite3

connection = _sqlite3.connect("data.db")

cursor = connection.cursor()

select_query = "SELECT * FROM users"
result = cursor.execute(select_query)
for user in result:
    print(user)

connection.close()
