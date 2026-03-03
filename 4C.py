import sqlite3

connection = sqlite3.connect('my_database.db')

cursor = connection.cursor()

cursor.execute('SELECT COUNT(*) FROM Users')


total_users = cursor.fetchall()[0]

print('Общее количество пользователей:', total_users)

cursor.execute('SELECT SUM(age) FROM Users')
total_age = cursor.fetchall()[0]

print('Общая сумма возрастов пользователей:', total_age)

cursor.execute('SELECT AVG(age) FROM Users')
avg_age = cursor.fetchall()[0]

print('Средний возраст пользователей:', avg_age)

cursor.execute('SELECT MIN(age) FROM Users')
min_age = cursor.fetchall()[0]

print('Минимальный возраст пользователей:', min_age)

cursor.execute('SELECT MAX(age) FROM Users')
max_age = cursor.fetchall()[0]

print('Максимальный возраст пользователей:', max_age)

connection.commit()
connection.close()

