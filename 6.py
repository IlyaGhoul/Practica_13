import sqlite3

connection = sqlite3.connect('my_database.db')

cursor = connection.cursor()

try:
    cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', ('user1', 'user1@example.com'))
    cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', ('user2', 'user2@example.com'))

    cursor.execute('COMMIT')
except:
    cursor.execute('ROLLBACK')

with sqlite3.connect('my_database.db') as connection:
    cursor = connection.cursor()
    
    try:    
        with connection:
            cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', ('user3', 'user3@example.com'))
            cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', ('user4', 'user4@example.com'))

    except:
        pass

connection.commit()
connection.close()

