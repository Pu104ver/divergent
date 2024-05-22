from flask import Flask, jsonify, abort, make_response
from flasgger import Swagger
import json
from typing import Tuple, Dict, Any

app = Flask(__name__)
swagger = Swagger(app)

def data_loader() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Функция загружает данные из json файлов и преобразует их в dict.
    Функция не должна нарушать изначальную структуру данных.
    """
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)['posts']
        with open('data/comments.json', 'r', encoding='utf-8') as f:
            comments = json.load(f)['comments']
    except FileNotFoundError as e:
        abort(500, description=f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        abort(500, description=f"Error decoding JSON: {e.msg}")
    except Exception as e:
        abort(500, description=f"Unexpected error: {str(e)}")
    return posts, comments

@app.route("/")
def get_posts() -> jsonify:
    """
    Получение всех постов.

    ---
    responses:
      200:
        description: Успешный ответ
        schema:
          id: Posts
          properties:
            posts:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Идентификатор поста
                  title:
                    type: string
                    description: Заголовок поста
                  body:
                    type: string
                    description: Тело поста
                  author:
                    type: string
                    description: Автор поста
                  created_at:
                    type: string
                    description: Время создания поста
                  comments_count:
                    type: integer
                    description: Количество комментариев к посту
            total_results:
              type: integer
              description: Общее количество постов
    """
    try:
        posts, comments = data_loader()
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
    # Подсчет комментариев для каждого поста
    comments_count = {post['id']: 0 for post in posts}
    for comment in comments:
        post_id = comment['post_id']
        if post_id in comments_count:
            comments_count[post_id] += 1
    
    # Формирование ответа
    posts_with_comments = []
    for post in posts:
        post_with_comments = {
            'id': post['id'],
            'title': post['title'],
            'body': post['body'],
            'author': post['author'],
            'created_at': post['created_at'],
            'comments_count': comments_count[post['id']]
        }
        posts_with_comments.append(post_with_comments)
    
    output = {
        'posts': posts_with_comments,
        'total_results': len(posts_with_comments)
    }
    return jsonify(output)

@app.route("/posts/<int:post_id>")
def get_post(post_id: int) -> jsonify:
    """
    Получение информации о конкретном посте по его идентификатору.

    ---
    parameters:
      - name: post_id
        in: path
        type: integer
        required: true
        description: Идентификатор поста
    responses:
      200:
        description: Успешный ответ
        schema:
          id: Post
          properties:
            id:
              type: integer
              description: Идентификатор поста
            title:
              type: string
              description: Заголовок поста
            body:
              type: string
              description: Тело поста
            author:
              type: string
              description: Автор поста
            created_at:
              type: string
              description: Время создания поста
            comments:
              type: array
              items:
                type: object
                properties:
                  user:
                    type: string
                    description: Автор комментария
                  post_id:
                    type: integer
                    description: Идентификатор поста, к которому относится комментарий
                  comment:
                    type: string
                    description: Текст комментария
                  created_at:
                    type: string
                    description: Время создания комментария
      404:
        description: Пост не найден
    """
    try:
        posts, comments = data_loader()
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

    post = next((post for post in posts if post['id'] == post_id), None)
    if post is None:
        abort(404, description="Post not found")
    
    # Формирование списка комментариев для поста
    post_comments = [
        {
            'user': comment['user'],
            'post_id': comment['post_id'],
            'comment': comment['comment'],
            'created_at': comment['created_at']
        }
        for comment in comments if comment['post_id'] == post_id
    ]
        
    # Формирование ответа
    post_with_comments: Dict[str, Any] = {
        'id': post['id'],
        'title': post['title'],
        'body': post['body'],
        'author': post['author'],
        'created_at': post['created_at'],
        'comments': post_comments
    }
    return jsonify(post_with_comments)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found", "message": error.description}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({"error": "Internal Server Error", "message": error.description}), 500)

if __name__ == "__main__":
    app.run(debug=True)
