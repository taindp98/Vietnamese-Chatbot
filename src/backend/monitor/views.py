from django.shortcuts import render
from .apps import *
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
import random

import pymongo

import json
from dotenv import load_dotenv

import sys
import os
import requests

sys.path.append(r"C:\Users\Admin\working\python\mine\Chatbot-University-Consultancy")

from src.core.language_understanding import UserUnderstand
from src.core.dialog_management import (
    FiniteStateMachineAgent,
    StateTracker,
)
from src.core.language_generating import ResponseGeneration

load_dotenv()
client = pymongo.MongoClient(os.getenv("MONGOLAB_URI"))
database = client.hcmut

WORKSPACE = r"./"

nlu_processor = UserUnderstand(root=os.path.join(WORKSPACE, "resources/nlu"))
nlg_processor = ResponseGeneration(root=os.path.join(WORKSPACE, "resources/nlg"))

# Create your views here.
session_tracker = dict()


def process_message(state_tracker_id, message):
    state_tracker = None

    if state_tracker_id in session_tracker.keys():
        state_tracker = session_tracker[state_tracker_id][0]
        confirm_obj = session_tracker[state_tracker_id][1]
    else:
        state_tracker = StateTracker(
            root=os.path.join(WORKSPACE, "resources/dm"), database=database
        )
        confirm_obj = None
        session_tracker[state_tracker_id] = (state_tracker, confirm_obj)

    ## 1. NLU
    user_action, new_confirm_obj = nlu_processor.process(message, state_tracker)

    if user_action["request_slots"] != {}:
        state_tracker.reset()
        confirm_obj = None

    if new_confirm_obj != None:
        confirm_obj = new_confirm_obj

    ## 2. DM
    if user_action["intent"] not in [
        "greeting",
        "fare_well",
        "thanks",
        "start",
        "not_intent"
    ]:
        fsm_agent = FiniteStateMachineAgent()

        agent_act, regex_constraint = fsm_agent.get_agent_action(
            state_tracker, user_action
        )

        session_tracker[state_tracker_id] = (state_tracker, confirm_obj)
        agent_message = nlg_processor.run(agent_act, state_tracker, confirm_obj)

    else:
        agent_act = {
            "intent": user_action["intent"],
            "request_slots": [],
            "inform_slots": [],
        }
        agent_message = nlg_processor.free_style([user_action["intent"]])

        if user_action["intent"] in ["done", "thanks"]:
            state_tracker.reset()
            session_tracker[state_tracker_id] = (state_tracker, None)
    return agent_message, agent_act


def get_new_id():
    while True:
        _id = str(random.randint(100000, 999999))
        if _id not in session_tracker.keys():
            return _id


class ConversationManagement(APIView):
    def get(self, request):
        request_content = dict(request.GET)
        userText = request_content["msg"][0]
        userId = request_content["_id"][0]
        api_url = "http://127.0.0.1:8000/conversation"
        input_data = {}
        input_data["message"] = str(userText)
        input_data["state_tracker_id"] = userId

        r = requests.post(url=api_url, json=input_data)
        print(f'response: {r}')
        chatbot_respose = r.json()
        mess_response = [
            item.replace("\n", r"").replace(r'"', r"")
            for item in chatbot_respose["message"]
        ]

        return Response({"message_list": mess_response}, status=200)

    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        input_data = json.loads(body_unicode)
        message = input_data["message"]
        if "state_tracker_id" not in input_data.keys():
            state_tracker_id = get_new_id()
        else:
            state_tracker_id = input_data["state_tracker_id"]

        current_informs = "null"

        response_dict = {
            "message": [],
            "state_tracker_id": state_tracker_id,
            "agent_action": {},
            "current_informs": {},
        }
        if not message.startswith("/"):
            agent_message, agent_action = process_message(state_tracker_id, message)
            if agent_action["intent"] in ["match_found", "inform"]:
                current_informs = session_tracker[state_tracker_id][0].current_informs

            response_dict = {
                "message": agent_message,
                "state_tracker_id": state_tracker_id,
                "agent_action": agent_action,
                "current_informs": current_informs,
            }

        return Response(response_dict, status=200)


def home(request):
    ui_src_path = os.path.join("templates", "bot.html")
    return render(request, ui_src_path)
