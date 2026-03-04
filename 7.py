import sqlite3

connection = sqlite3.connect('my_database.db')

cursor = connection.cursor()

query = 'SELECT * FROM Users WHERE age > ?'
cursor.execute(query, (25,))
users = cursor.fetchall()

for user in users:
    print(user)

connection.commit()
connection.close()

