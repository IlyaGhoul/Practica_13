import sqlite3

connection = sqlite3.connect('my_database.db')

cursor = connection.cursor()

query = 'SELECT * FROM Users WHERE age > ?'
cursor.execute(query, (25,))
users = cursor.fetchall()

for user in users:
    print(user)

cursor.execute('CREATE VIEW ActiveUsers AS SELECT * FROM Users WHERE is_active = 1')

cursor.execute('SELECT * FROM ActiveUsers')
active_users = cursor.fetchall()

for user in active_users:
    print(user)

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
               id INTEGER PRIMARY KEY,
               username TEXT NOT NULL,
               email TEXT NOT NULL,
               age INTEGER,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
               ''')

cursor.execute('''
CREATE TRIGGER IF NOT EXISTS update_created_at
               AFTER INSERT Users
               BEGIN
               UPDATE Users SET created_at = CURRENT_TIMESTAMP WHERE
               id = NEW.id;
               END;
               ''')

cursor.execute('CREATE INDEX idx_username ON Users (username)')

connection.commit()
connection.close()

