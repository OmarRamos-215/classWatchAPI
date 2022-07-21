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

post_report_args.add_argument("classroom", type=str, help="ERROR classroom is required", required=True)
post_report_args.add_argument("reporter_badge", type=int, help="ERROR reporter_badge is required", required=True)
post_report_args.add_argument("tag", type=str, help="ERROR tag is required", required=True)
post_report_args.add_argument("reason", type=str, help="ERROR reason is required", required=True)

@app.route('/test/', methods=['GET'])
def get_test():
    return jsonify({"message":"You are connected"})

#Classrooms
@app.route('/classrooms/', methods=['GET'])
def get_classrooms():
    collection_name= database.db['classrooms']

    request= collection_name.find()
    classrooms= []
    for classroom in request:
        del classroom['_id']
        classrooms.append(classroom)
    return jsonify(classrooms)

@app.route('/classrooms/<room>/', methods=['GET'])
def get_classroom(room):
    collection_name= database.db['classrooms']

    request= collection_name.find({'classrooms.id_classroom' : room}, {'classrooms.$' : 1})
    classrooms= []
    for classroom in request:
        del classroom['_id']
        return jsonify(classroom)

#Reports
@app.route('/reports/<room>/', methods=['GET'])
def get_reports(room):
    collection_name= database.db['reports']
    request= collection_name.find({'classroom': room, 'is_active': True})
    reports= []
    for report in request:
        del report['_id']
        reports.append(report)
    return jsonify(reports)


@app.route('/reports/', methods=['POST'])
def post_report():
    collection_name= database.db['reports']
    date= datetime.now()
    args = post_report_args.parse_args()
    report_id= str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'-'+str(args['reporter_badge'])
    collection_name.insert_one({
        'report_id' : report_id,
        'classroom': args['classroom'],
        'reporter_badge': args['reporter_badge'],
        'date': date,
        'tag': args['tag'],
        'reason': args['reason'],
        'is_active': True
    })
    return jsonify(args)

@app.route('/deactivate/<report_id>/', methods=['PATCH'])
def patch_report(report_id):
    collection_name= database.db['reports']
    collection_name.update_one({'report_id' : report_id}, {'$set': {'is_active' : False}})
    return jsonify({'Message' : 'Deactivaded'})

#Tags
@app.route('/tags/', methods=['GET'])
def get_tags():
    collection_name= database.db['tags']
    request= collection_name.find()
    tags= []
    for tag in request:
        del tag['_id']
        tags.append(tag)
    return jsonify(tags)

#Users
@app.route('/users/', methods=['GET'])
def get_users():
    collection_name= database.db['users']

    request= collection_name.find()
    users= []
    for user in request:
        del user['_id']
        users.append(user)
    return jsonify(users)

@app.route('/users/<badge>/', methods=['GET'])
def get_user(badge):
    collection_name= database.db['users']
    request= collection_name.find_one({'badge' : badge})
    del request['_id']
    return jsonify(request)

if __name__== '__main__':
    app.run(load_dotenv=True, port=8080)
