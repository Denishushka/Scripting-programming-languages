import requests
import sqlite3


url = 'https://jsonplaceholder.typicode.com/posts'
response = requests.get(url)
connecttoDB = sqlite3.connect('posts.db')
db = connecttoDB.cursor()
posts = response.json()
for post in posts:
    db.execute('''
        INSERT INTO posts (id, user_id, title, body)
        VALUES (?, ?, ?, ?)
    ''', (post['id'], post['userId'], post['title'], post['body']))
connecttoDB.commit()
connecttoDB.close()
