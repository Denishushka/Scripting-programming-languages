import requests

url = 'https://jsonplaceholder.typicode.com/posts'

response = requests.get(url)

if response.status_code == 200:
    posts = response.json()

    even_user_posts = [post for post in posts if post['userId'] % 2 == 0]

    for post in even_user_posts:
        print(post)


new_post = {
    'title': 'Тестовый пост',
    'body': 'Это тело тестового поста',
    'userId': 1
}

response = requests.post(url, json=new_post)

if response.status_code == 201:
    created_post = response.json()
    print("Созданный пост:")
    print(created_post)

post_id = 1

updated_post = {
    'title': 'Обновлённый пост',
    'body': 'Обновленное тело поста',
    'userId': 1
}

response = requests.put(f'{url}/{post_id}', json=updated_post)

if response.status_code == 200:
    updated_post_data = response.json()
    print("Обновленный пост:")
    print(updated_post_data)
