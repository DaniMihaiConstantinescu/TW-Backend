# myapp/routes/post_routes.py
from asyncio.windows_events import NULL
from flask import Blueprint, request, jsonify, make_response
from datetime import datetime

import random
from pyasn1_modules.rfc5208 import ub_country_name_numeric_length
from datetime import datetime

stack_blueprint = Blueprint('post', __name__)

import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyCp7TW9Ff85IOzgW-kGcvhn5fpgLFaxcEM",
  "authDomain": "tactical-unison-363709.firebaseapp.com",
  "databaseURL": "https://tactical-unison-363709-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "tactical-unison-363709",
  "storageBucket": "tactical-unison-363709.appspot.com",
  "messagingSenderId": "96593883473",
  "appId": "1:96593883473:web:535ca940c36486cb68e370"
};


firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

@stack_blueprint.route('/stack/getid', methods=['GET'])
def generateId():
    new_id = generate_incremental_id()
    return jsonify({"id": new_id})

@stack_blueprint.route('/stack/<userAPIKey>/<name>/<color>', methods = ['GET'])
def createStackFromFrontEnd(userAPIKey, name, color):
    uid = userAPIKey
    stack_id = generate_incremental_id()
    stack_name = name
    stack_color = color  
    stack_createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nodes = []

    db.child(uid).child("stacks").child(stack_id).set({'id': stack_id, 'name' : stack_name, 'color' : stack_color, 'nodes' : nodes})
    
    # response_data = {'status': 'success', 'stack_id': stack_id}
    # return make_response(jsonify(response_data), 200)


@stack_blueprint.route('/stack/add', methods=['POST'])
def addStack():
    data = request.get_json()

    uid = data['userAPIKey']
    stack_id = data['id']
    stack_name = data['name']
    stack_color = data['color']
    stack_createdAt = data['createdAt']
    nodes = data['nodes']

    db.child(uid).child("stacks").child(stack_id).set({'id': stack_id, 'name': stack_name, 'color': stack_color, 'nodes': nodes})

    response_data = {'status': 'success', 'stack_id': stack_id}
    return make_response(jsonify(response_data), 200)

@stack_blueprint.route('/stack/new', methods=['POST'])
def addNewStack():
    data = request.get_json()

    uid = data['userAPIKey']
    stack_id = generate_incremental_id()
    stack_name = data['name']
    stack_color = data['color']   
    stack_createdAt = data['createdAt']
    nodes = data['nodes']


    db.child(uid).child("stacks").child(stack_id).set({'id': stack_id, 'name' : stack_name, 'color' : stack_color, 'nodes' : nodes})
    
    response_data = {'status': 'success', 'stack_id': stack_id}
    return make_response(jsonify(response_data), 200)

@stack_blueprint.route('/stack/count/<userAPIKey>', methods=['GET'])
def getStacksCount(userAPIKey):
    user_stacks = db.child(userAPIKey).child("stacks").get().val()

    if user_stacks is not None:
        number_of_stacks = len(user_stacks)
        return jsonify({'stacksNumber': number_of_stacks})
    else:
        return jsonify({'stacksNumber': 0}) 

@stack_blueprint.route('/stack/<userAPIKey>/<stackId>', methods=['POST'])
def addNodeToStack(userAPIKey, stackId):
    data = request.get_json()   
    
    stack_ref = db.child(userAPIKey).child("stacks").child(stackId)
    nodes_ref = stack_ref.child("nodes")
    existing_nodes = nodes_ref.get().val()
    
    if existing_nodes is None:
        existing_nodes = {}

    new_node_id = str(len(existing_nodes))
    db.child(userAPIKey).child("stacks").child(stackId).child("nodes").child(new_node_id).set(data)

    response_data = {'status': 'success'}
    return make_response(jsonify(response_data), 200)



#Return all data from a certain stack 
#   @param stackId      
#   @param userAPIKey   
@stack_blueprint.route('/stack/<userAPIKey>/<stackId>', methods=['GET'])
def getAllDataFromStack(userAPIKey, stackId):
    return jsonify(db.child(userAPIKey).child("stacks").child(stackId).get().val())

#Return all stacks for a user 
#   @param userAPIKey
@stack_blueprint.route('/all_stacks/<userAPIKey>', methods=['GET'])
def getAllStacks(userAPIKey):
    return jsonify(db.child(userAPIKey).get().val())

#Dummy
@stack_blueprint.route('/stack/<id>', methods=['GET'])
def get_stack(id):
    return jsonify({'message': id})


def generate_incremental_id():
    # Retrieve the current maximum ID from the database
    max_id = db.child('max_id').get().val() or 0
    
    # Increment the ID
    new_id = max_id + 1

    # Update the max_id in the database for the next use
    db.child('max_id').set(new_id)

    return new_id
