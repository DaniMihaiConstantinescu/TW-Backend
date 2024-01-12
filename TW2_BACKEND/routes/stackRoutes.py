# myapp/routes/post_routes.py
from asyncio.windows_events import NULL
from flask import Blueprint, request, jsonify, make_response
from datetime import datetime

import random


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


@stack_blueprint.route('/stack/add', methods=['POST'])
def addStack():
    data = request.get_json()

    uid = data['userAPIKey']
    stack_id = generate_incremental_id()
    stack_name = data['name']
    stack_color = data['color']   
    stack_createdAt = data['createdAt']
    nodes = data['nodes']

    #store data
    db.child(uid).child("stacks").child(stack_id).set({'id': stack_id, 'name' : stack_name, 'color' : stack_color, 'nodes' : nodes})

     # Return a valid response
    response_data = {'status': 'success', 'stack_id': stack_id}
    return make_response(jsonify(response_data), 200)


@stack_blueprint.route('/stack/<userAPIKey>/<stackId>', methods=['POST'])
def addNodeToStack(userAPIKey, stackId):
    data = request.get_json()

    uid = userAPIKey
    stack_id = stackId
    
    # Reference to the 'stacks' child for the specific user and stack
    stack_ref = db.reference(f'{uid}/stacks/{stack_id}')

    # Push the new node data to the 'nodes' child under a unique key
    stack_ref.child("nodes").push(data).key

    # Return a valid response
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

# Return number of users stacks
@stack_blueprint.route('/stack/<userAPIKey>', methods=['GET'])
def getStacksNumber(userAPIKey):
    user_stacks = db.child(userAPIKey).child("stacks").get().val()

    if user_stacks is not None:
        number_of_stacks = len(user_stacks)
        return jsonify({'stacksNumber': number_of_stacks})
    else:
        return jsonify({'stacksNumber': 0})


def generate_incremental_id():
    # Retrieve the current maximum ID from the database
    max_id = db.child('max_id').get().val() or 0
    
    # Increment the ID
    new_id = max_id + 1

    # Update the max_id in the database for the next use
    db.child('max_id').set(new_id)

    return new_id
