from flask import Flask, render_template, request, json, jsonify
from flask_pymongo import PyMongo
from pymongo import ReturnDocument
from bson import json_util

app = Flask(__name__)
app.secret_key = 'BfO3BrkI6XFagXhWYQ2YBg'
app.config["MONGO_URI"] = "mongodb://svetlana:cisco123@localhost:27017/Device_Configuration"
json.dumps = json_util.dumps
mongo = PyMongo(app)

#TASK 1
@app.route('/<switch_name>/interfaces.html', methods=['GET'])
def get_all_interfaces_from_switch_HTML(switch_name):
    mongo_filter = {'Switch_name':switch_name}
    result = mongo.db.Interfaces.find(mongo_filter)
    return render_template('interfaces.html', result=result, switch=switch_name)

#TASK 2
@app.route('/<switch_name>/interfaces.json', methods=['GET'])
def get_all_interfaces_from_switch_JSON(switch_name):
    mongo_filter = {'Switch_name':switch_name}
    result = mongo.db.Interfaces.find(mongo_filter)
    return jsonify(result), 200

#TASK 3
@app.route('/<switch_name>/<interface_name>/<a>/details.html',defaults={'b':'None'}, methods=['GET'])
@app.route('/<switch_name>/<interface_name>/<a>/<b>/details.html', methods=['GET'])
def get_specific_interface_HTML(switch_name, interface_name,a,b):
    if b == 'None':
        interface_name = interface_name + '/' + a
    else:
        interface_name = interface_name + '/' + a + '/' + b
    interface = ' '.join(interface_name.split('_'))
    mongo_filter = {'Switch_name':switch_name, 'Interface_Name':interface}
    result = mongo.db.Interfaces.find(mongo_filter)
    return render_template('interface_of_switch.html', result=result, switch=switch_name, interface=interface)

#TASK 4
@app.route('/<switch_name>/<interface_name>/<a>/details.json',defaults={'b':'None'}, methods=['GET'])
@app.route('/<switch_name>/<interface_name>/<a>/<b>/details.json', methods=['GET'])
def get_specific_interface_JSON(switch_name, interface_name,a,b):
    if b == 'None':
        interface_name = interface_name + '/' + a
    else:
        interface_name = interface_name + '/' + a + '/' + b
    interface = ' '.join(interface_name.split('_'))
    mongo_filter = {'Switch_name':switch_name, 'Interface_Name':interface}
    result = mongo.db.Interfaces.find(mongo_filter)
    return jsonify(result), 200

#TASK 5 and 6
@app.route('/<switch_name>/<ObjectId:_id>', methods=['PATCH'])
def patch_description(switch_name,_id):
    payload = request.get_json()
    if payload:
        result = mongo.db.Interfaces.find_one_and_update(
            {'Switch_name':switch_name,'_id':_id},
            {'$set':payload},
            return_document=ReturnDocument.AFTER
        )
        return jsonify(result), 200
    return "Error!", 500


if __name__ == '__main__':
    app.run()