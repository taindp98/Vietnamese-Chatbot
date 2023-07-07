import pymongo
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime
import time
import os
import time
from dotenv import load_dotenv
import json

from core.language_understanding import IntentRecognition, UserUnderstand

from core.dialog_management import FiniteStateMachineAgent, StateTracker

from core.dialog_management.agent_action import get_agent_action,get_prob_agent_action
from core.nlg.gen_sentence import response_craft
from core.nlg.default_response import response_to_user_free_style
from core.nlg.constants_response import *

load_dotenv()

app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGOLAB_URI')


mongo = PyMongo(app)

CONSTANTS_FILE_PATH = './dqn/constants.json'
with open(CONSTANTS_FILE_PATH) as f:
    constants = json.load(f)
client = pymongo.MongoClient(os.getenv('MONGOLAB_URI'))
database = client.hcmut

# khoi tao app
app = Flask(__name__)
CORS(app)
StateTracker_Container = dict()
app.config["MONGO_URI"] = os.environ.get('MONGOLAB_URI')
mongo = PyMongo(app)

def msg(code, mess=None):
    if code == 200 and mess is None:
        return jsonify({"code": 200, "value": True})
    else:
        return jsonify({"code": code, "message": mess}), code

def get_new_id():
    while (True):
        _id = str(random.randint(100000, 999999))
        if _id not in StateTracker_Container.keys():
            return _id




# @app.route('/')
# def index():
#     return """<h1>HCMUT Assitant</h1>"""

@app.errorhandler(404)
def url_error(e):
    # print("---------------------")
    return msg(404,'URL ERROR')

@app.errorhandler(500)
def server_error(e):
    return msg(500, "SERVER ERROR")

@app.route('/api/', methods=['POST'])
def post_api():
    input_data = request.get_json(force=True)
    # print(input_data)
    if "message" not in input_data.keys():
        return msg(400, "Message cannot be None")
    else:
        message = input_data["message"]
        result,probability,mess_clean = catch_intent(message)
        # probability = probability.tolist()
    return jsonify({"code": 200, "message": result, "probability": probability})

@app.route('/api/convers-manager', methods=['POST'])
def post_api_cse_assistant():
    input_data = request.json
    now = datetime.now()
    timestamp = now.timestamp()
    # date_time = now.strftime("%m%d%Y%H%M%S")
    ## modify avoid crash
    try:

        if "message" not in input_data.keys():
            return msg(400, "Message cannot be None")
        else:
            message = input_data["message"]
        # print("-------------------------message")
        # print(message)
        if "state_tracker_id" not in input_data.keys():
            state_tracker_id = get_new_id()
        else:
            state_tracker_id = input_data["state_tracker_id"]

        # print('state_tracker_id ',state_tracker_id)
        # print('receive_message ',message)
        # print('StateTracker_Container',StateTracker_Container)
        # K.clear_session()
        current_informs = 'null'
        if not message.startswith('/'):
            agent_message , agent_action = process_conversation_POST(state_tracker_id, message)
            if agent_action['intent'] in ["match_found","inform"]:
                current_informs = StateTracker_Container[state_tracker_id][0].current_informs
            # K.clear_session()

            # print('agent_message',agent_message)

            res_dict = {}
            res_dict["code"] = 200
            res_dict["message"] = agent_message
            res_dict["state_tracker_id"] = state_tracker_id

            res_dict['agent_action'] = agent_action
            res_dict['current_informs'] = current_informs

            # print('======================')
            # print('current_informs',current_informs)
            # print(res_dict)
            # return jsonify({"code": 200, "message": agent_message,"state_tracker_id":state_tracker_id,"agent_action":agent_action,"current_informs":current_informs})
            return jsonify(res_dict)
        else:
            res_dict = {}
            res_dict["code"] = 200
            res_dict["message"] = []
            res_dict["state_tracker_id"] = state_tracker_id

            res_dict['agent_action'] = {}
            res_dict['current_informs'] = {}
            return jsonify(res_dict)

    except Exception as e:
        # print('')
        mongo.db.investigate.insert_one({
            'time':timestamp,
            'error':str(e)
            })
        print('>'*20)
        print(str(e))
        res_dict = {}
        res_dict["code"] = 500
        res_dict["message"] = [random.choice(DONT_UNDERSTAND)]
        res_dict["state_tracker_id"] = state_tracker_id

        res_dict['agent_action'] = {}
        res_dict['current_informs'] = {}
        return jsonify(res_dict)

@app.route('/api/cse-assistant-conversation-manager/reset-state-tracker', methods=['POST'])
def post_api_cse_assistant_reset_state_tracker():
    input_data = request.json

    if "state_tracker_id" not in input_data.keys():
        return msg(400, "Message cannot be None")
    else:
        state_tracker_id = input_data["state_tracker_id"]
    # print("-------------------------state_tracker_id")
    # print(state_tracker_id)
    # # if "state_tracker_id" not in input_data.keys():
    # #     state_tracker_id = get_new_id()
    # # else:
    # #     state_tracker_id = input_data["state_tracker_id"]
    # print(StateTracker_Container)
    # K.clear_session()

    if state_tracker_id in StateTracker_Container:
        state_tracker = StateTracker_Container[state_tracker_id][0]
        state_tracker.reset()
        StateTracker_Container[state_tracker_id] = (state_tracker,None)
        message = "success"
        code = 200
    else:
        message = "fail"
        code = 404
    # K.clear_session()
    return jsonify({"code": code, "message": message,"state_tracker_id":state_tracker_id})



@app.route("/api/LT-conversation-manager/messages", methods=['POST'])
def user_profile():
    input_data = request.json
    # print(input_data)
    if "message" not in input_data.keys():
        return msg(400, "Message cannot be None")
    if "intent" not in input_data.keys():
        return msg(400, "Intent cannot be None")
    user_id = input_data["user_id"]
    message = input_data["message"]
    intent = input_data["intent"]
    is_correct = input_data["is_correct"]

    # check mongo insert cloud
    # mongo.db.messages.insert_one(
        # {"user_id": user_id, "message": message, "intent": intent, "is_correct": is_correct})

    return jsonify({"code": 200, "message": "insert successed!"})

@app.route('/api/LT-conversation-manager/classify-message', methods=['POST'])
def post_api_classify_message():
    input_data = request.get_json(force=True)
    # print(input_data)
    if "message" not in input_data.keys():
        return msg(400, "Message cannot be None")
    else:
        message = input_data["message"]
        result,probability,mess_clean = catch_intent(message)
    return jsonify({"is_question": check_question(message), "intent": result})


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0',port=6969,debug=True)

