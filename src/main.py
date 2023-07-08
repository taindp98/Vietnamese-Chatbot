import pymongo

import random
from datetime import datetime
import time
import time
from dotenv import load_dotenv
import json
import os

from core.language_understanding import UserUnderstand
from core.dialog_management import FiniteStateMachineAgent, StateTracker, get_agent_action
from core.language_generating import free_style_responses, ResponseGeneration

client = pymongo.MongoClient("mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/hcmut?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority")
database = client.hcmut

nlu_processor = UserUnderstand()
nlg_processor = ResponseGeneration()

def main(state_tracker_id, message):
    session_tracker = dict()

    now = datetime.now()
    timestamp = now.timestamp()
    state_tracker = None
    if message:
        start_time = time.time()

    if state_tracker_id in session_tracker.keys():
        state_tracker = session_tracker[state_tracker_id][0]
        confirm_obj = session_tracker[state_tracker_id][1]
    else:
        state_tracker = StateTracker(database)
        confirm_obj = None
        session_tracker[state_tracker_id] = (state_tracker, confirm_obj)

    ## 1. NLU
    user_action, new_confirm_obj = nlu_processor.process(message, state_tracker)

    if user_action['request_slots'] != {}:
        state_tracker.reset()
        confirm_obj = None

    if new_confirm_obj != None:
        confirm_obj = new_confirm_obj

    if user_action['intent'] not in ["greeting","other","fare_well","thanks",'start']:
        fsm_agent = FiniteStateMachineAgent()

        agent_act, regex_constraint = get_agent_action(state_tracker, fsm_agent, user_action)

        session_tracker[state_tracker_id] = (state_tracker,confirm_obj)
        agent_message = nlg_processor.run(agent_act, state_tracker,confirm_obj)

    else:
        agent_act = {'intent':user_action['intent'],'request_slots':[],'inform_slots':[]}
        agent_message = [random.choice(free_style_responses[user_action['intent']])]

        if user_action['intent'] in ["done","thanks"]:
            state_tracker.reset()
            session_tracker[state_tracker_id] = (state_tracker,None)
    return agent_message,agent_act

if __name__ == "__main__":
    state_tracker_id = 0
    message = "cho em xin Chỉ tiêu tuyển sinh năm 2020 của khối A1 ngành điện điện tử?"
    response =main(state_tracker_id, message)
    print(response)