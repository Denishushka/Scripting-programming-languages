import sqlite3


connecttoDB = sqlite3.connect('posts.db')
db = connecttoDB.cursor()
def get_posts_by_user(user_id):
    db.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
    return db.fetchall()

# Получаем посты пользователя с нужным user_id 
user_id = 1
user_posts = get_posts_by_user(user_id)

# Выводим посты
print('Список постов пользователя с user-id = ' , user_id)
for post in user_posts:
    print('id:' ,post[1])
    print('title:' ,post[2])
    print('body:' ,post[3],'\n')
connecttoDB.close()