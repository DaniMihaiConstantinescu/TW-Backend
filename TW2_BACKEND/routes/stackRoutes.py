# myapp/routes/post_routes.py
from asyncio.windows_events import NULL
from flask import Blueprint, request, jsonify
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

#Store a stack in database
#Request data format:

#{"uid" : "cipriAPI", 
#        "stackId" : "2",
#        "name": "Stack 1",
#        "color": "#21AA27",
#        "content": [
#            {
#                "type": "text",
#                "title": "Title",
#                "createdAt": "2023-07-13",
#                "text": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis eligendi unde dicta quos? Delectus a facilis placeat architecto quasi praesentium minus magni, nemo molestias numquam tempore adipisci vitae dicta voluptate dolorem fugiat maxime, autem voluptates distinctio. Tenetur non rem adipisci cum voluptates maxime praesentium voluptate. Quasi hic ut sit culpa!",
#            },
#            {
#                "type": "image",
#                "title": "Image name",
#                "createdAt": "2023-07-13",
#                "text": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis eligendi unde dicta quos? Delectus a facilis placeat architecto quasi praesentium minus magni, nemo molestias numquam tempore adipisci vitae dicta voluptate dolorem fugiat maxime, autem voluptates distinctio.",
#                "url": "https://analysisfunction.civilservice.gov.uk/wp-content/uploads/2022/12/pie-bar.svg"
#            },
#            {
#                "type":"graph",
#                "title": "Graph Title",
#                "createdAt": "2023-07-13",
#                "text": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis eligendi unde dicta quos? Delectus a facilis placeat architecto quasi praesentium minus magni, nemo molestias numquam tempore adipisci vitae dicta voluptate dolorem fugiat maxime, autem voluptates distinctio.",
#                "xLabel": "Label1",
#                "yLabel": "Label2",
#                "keyFrames": [
#                  { "x": 10, "y": 20 },
#                  { "x": 30, "y": 40 },
#                  { "x": 50, "y": 70 },
#                  { "x": 70, "y": 90 },
#                  { "x": 100, "y": 110 },
#                  { "x": 120, "y": 130 },
#                  { "x": 140, "y": 170 },
#                ]
#              }
#        ]
#}
@stack_blueprint.route('/stack/add', methods=['POST'])
def addStack():
    data = request.get_json()

    uid = data['uid']
    stack_name = data['name']
    stack_color = data['color']
    stack_id = data['stackId']        #received from frontend?
    current_date = datetime.now().strftime("%Y-%m-%d")
    content_received = data['content']
    
    content = []
    #retreive data from content
    for item in content_received:
        content_item = {}

        content_item['type'] = item["type"]
        content_item['title'] = item["title"]
        content_item['createdAt'] = current_date
        content_item['text'] = item["text"];

        if item["type"] == "image":
            content_item['url'] = item['url']
        elif item["type"] == "text":
            a = 6
        elif item["type"] == "graph":
            content_item['xLabel'] = item['xLabel']
            content_item['yLabel'] = item['yLabel']
            content_item['keyFrames'] = item['keyFrames']

        content.append(content_item)

    #store data
    db.child(uid).child("stacks").child(stack_id).set({'name' : stack_name,'color' : stack_color,'content' : content})

#To be done if required
@stack_blueprint.route('/image/add', methods=['POST'])
def addImage():
    data = request.get_json()

    uid = data['uid']
    image_data = data['image']
    stack_id = image_data['stackId']
    name = image_data['name']
    description = image_data['description']
    file_link = image_data['file']
    data_type = "image"
    current_date = datetime.now().strftime("%Y-%m-%d")

    db_data = db.child(uid);
    
    #suppose the user already have at least a stack stored as he/she s present in the database
    if db_data:                                     #stack_id calculated from frontend
        user_stack = db_data.child("stacks").child(1)
        #already have the stack
        if user_stack:
            content = user_stack.child("content").get().val()
            content.append({"type" : "data_type","title" : "name","createdAt" : "current_date","text" : "description","url" : "file_link"})
            db.child("raduAPI").child("stacks").child(1).update({"content" : content})

#Return all data from a certain stack 
#   @param stackId      
#   @param userAPIKey   
@stack_blueprint.route('/all_data_from_stack/<userAPIKey>/<stackId>', methods=['GET'])
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
