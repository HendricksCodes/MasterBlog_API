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
    sort_by = request.args.get('sort')
    direction = request.args.get('direction')

    sorted_posts = POSTS.copy()

    if sort_by and sort_by in ['title', 'content']:
        sorted_posts.sort(key=lambda x: x[sort_by])

        if direction == 'desc':
            sorted_posts.reverse()

        return jsonify(sorted_posts)

    elif sort_by or direction:
        return jsonify({"error": "Invalid sort field or direction."}), 400

    else:
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


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = next((post for post in POSTS if post['id'] == id), None)
    if not post:
        abort(404)  # Not found - post with given id doesn't exist

    if not request.json:
        abort(400)  # Bad request - empty body

    new_title = request.json.get('title', post['title'])
    new_content = request.json.get('content', post['content'])

    post['title'] = new_title
    post['content'] = new_content

    updated_post = {
        'id': id,
        'title': new_title,
        'content': new_content
    }

    # Update the POSTS list with the modified post
    for index, post in enumerate(POSTS):
        if post['id'] == id:
            POSTS[index] = post
            break

    return jsonify(updated_post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    if not title_query and not content_query:
        return jsonify([])  # returns empty lift if no search terms are provided

    matching_posts = []

    for post in POSTS:
        if title_query and title_query.lower() in post['title'].lower():
            matching_posts.append(post)
        elif content_query and content_query.lower() in post['content'].lower():
            matching_posts.append(post)

    return jsonify(matching_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
