import sqlite3
# Создание базы данных
connecttoDB = sqlite3.connect('posts.db')
db = connecttoDB.cursor()
# Создание таблицы
db.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        body TEXT
    )
''')
connecttoDB.commit()
connecttoDB.close()