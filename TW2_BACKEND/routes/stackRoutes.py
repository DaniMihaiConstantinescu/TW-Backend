# myapp/routes/post_routes.py
from flask import Blueprint, request, jsonify

stack_blueprint = Blueprint('post', __name__)


@stack_blueprint.route('/stack/add', methods=['POST'])
def addStack():
    data = request.get_json()

    if 'title' in data:
        title = data['title']
        return jsonify({'message': f'Post created with title: {title}'}), 201
    else:
        return jsonify({'error': 'Title not found in the request data'}), 400


@stack_blueprint.route('/stack/<id>', methods=['GET'])
def get_stack(id):
    return jsonify({'message': id})
