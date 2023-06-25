from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    if not request.json or 'title' not in request.json or 'content' not in request.json:
        abort(400)  # Bad request: title and content are required

    title = request.json['title']
    content = request.json['content']

    # Generate new post ID
    new_post_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1

    # Create new post object
    new_post = {
        'id': new_post_id,
        'title': title,
        'content': content
    }

    # append new post to list of posts
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post_index = next((index for index, post in enumerate(POSTS) if post['id'] == id), None)
    if post_index is None:
        abort(404)  # post with given id not found

    deleted_post = POSTS.pop(post_index)
    return jsonify({"message": f"Post with id {deleted_post['id']} has been deleted!"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
