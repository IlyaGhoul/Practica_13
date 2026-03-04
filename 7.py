import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    is_active INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('PRAGMA table_info(Users)')
cols = {row[1] for row in cursor.fetchall()}
if 'is_active' not in cols:
    cursor.execute('ALTER TABLE Users ADD COLUMN is_active INTEGER DEFAULT 0')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON Users (username)')

cursor.execute('''
CREATE VIEW IF NOT EXISTS ActiveUsers AS
SELECT * FROM Users WHERE is_active = 1
''')

cursor.execute('''
CREATE TRIGGER IF NOT EXISTS update_created_at
AFTER INSERT ON Users
BEGIN
    UPDATE Users SET created_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
''')



query = 'SELECT * FROM Users WHERE age > ?'
cursor.execute(query, (25,))
users = cursor.fetchall()

for user in users:
    print(user)

cursor.execute('SELECT * FROM ActiveUsers')
active_users = cursor.fetchall()

for user in active_users:
    print(user)

connection.commit()
connection.close()
