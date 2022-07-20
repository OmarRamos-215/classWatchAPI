from importlib.metadata import requires
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
from flask_cors import CORS
import app.db_config as database
from datetime import datetime

app= Flask(__name__)
api= Api(app)
CORS(app)

post_report_args= reqparse.RequestParser()

post_report_args.add_argument("id", type=int, help="ERROR id value needs to be an integer", required=True)
post_report_args.add_argument("classroom", type=str, help="ERROR classroom is required", required=True)
post_report_args.add_argument("reporter", type=str, help="ERROR reporter is required", required=True)
post_report_args.add_argument("date", type=str, required=False)
post_report_args.add_argument("tag", type=str, help="ERROR tag is required", required=True)
post_report_args.add_argument("reason", type=str, help="ERROR reason is required", required=True)

@app.route('/test', methods=['GET'])
def get_test():
    return jsonify({"message":"You are connected"})

#Classrooms
@app.route('/classrooms', methods=['GET'])
def get_classrooms():
    collection_name= database.db['classrooms']

    request= collection_name.find()
    classrooms= []
    for classroom in request:
        del classroom['_id']
        classrooms.append(classroom)
    return jsonify(classrooms)

@app.route('/classrooms/<room>', methods=['GET'])
def get_classroom(room):
    collection_name= database.db['classroom2']

    request= collection_name.find({'classrooms.id_classroom' : room}, {'classrooms.$' : 1})
    classrooms= []
    for classroom in request:
        del classroom['_id']
        return jsonify(classroom)

@app.route('/users', methods=['GET'])
def get_users():
    collection_name= database.db['users']

    request= collection_name.find()
    users= []
    for user in request:
        del user['_id']
        users.append(user)
    return jsonify(users)


#Tags
@app.route('/tags/', methods=['GET'])
def get_tags():
    collection_name= database.db['tags']
    request= collection_name.find()
    tags= []
    for tag in tags:
        del tag['_id']
        tags.append(tag)
    return jsonify({'tags' : tags})

#Users
@app.route('/user/<email>', methods=['GET'])
def get_user(email):
    collection_name= database.db['users']
    request= collection_name.find({'email' : email})
    del request['_id']
    return jsonify(request)

if __name__== '__main__':
    app.run(load_dotenv=True, port=8080)
