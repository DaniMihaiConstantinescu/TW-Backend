# myapp/routes/post_routes.py
from flask import Blueprint, request, jsonify

post_blueprint = Blueprint('post', __name__)


@post_blueprint.route('/stack/add', methods=['POST'])
def addStack():
    data = request.get_json()

    if 'title' in data:
        title = data['title']
        return jsonify({'message': f'Post created with title: {title}'}), 201
    else:
        return jsonify({'error': 'Title not found in the request data'}), 400


@post_blueprint.route('/stack', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello'})
