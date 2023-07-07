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

client = pymongo.MongoClient("mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/hcmut?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority")
database = client.hcmut

nlu_processor = UserUnderstand()

def main(state_tracker_id, message):
    StateTracker_Container = dict()

    now = datetime.now()
    timestamp = now.timestamp()
    dict_investigate = {}
    state_tracker = None
    dict_investigate['time'] = timestamp
    dict_investigate['visit_id'] = state_tracker_id
    if message:
        start_time = time.time()

    if state_tracker_id in StateTracker_Container.keys():
        state_tracker = StateTracker_Container[state_tracker_id][0]
        confirm_obj = StateTracker_Container[state_tracker_id][1]
    else:
        state_tracker = StateTracker(database)
        confirm_obj = None
        StateTracker_Container[state_tracker_id] = (state_tracker, confirm_obj)

    ## 1. NLU
    user_action, new_confirm_obj = nlu_processor.process(message, state_tracker)

    # user_request_slot,user_inform_slot = state_tracker.update_state_user(user_action)
    dict_investigate['semantic_frame'] = {}
    dict_investigate['semantic_frame']['user'] = {}
    dict_investigate['semantic_frame']['user'] = user_action
    dict_investigate['semantic_frame']['user']['message'] = message
    dict_investigate['query_string'] = ''
    # if user_action['intent']:
    if user_action['request_slots'] != {}:
        state_tracker.reset()
        confirm_obj = None

    if new_confirm_obj != None:
        confirm_obj = new_confirm_obj

    # try:
    if user_action['intent'] not in ["greeting","other","fare_well","thanks",'start']:
        fsm_agent = FiniteStateMachineAgent()

        agent_act,regex_constraint = get_agent_action(state_tracker, fsm_agent, user_action)
        dict_investigate['query_string'] = str(regex_constraint)
        # print('========================')
        # print('agent action',agent_act)
        # print('========================')

        StateTracker_Container[state_tracker_id] = (state_tracker,confirm_obj)
        # print('state_tracker.current_request_slots[0]',state_tracker.current_request_slots[0])
        # agent_message = response_craft(agent_act, state_tracker,confirm_obj)

    else:
        # to prevent key error
        # print('day ne')
        agent_act = {'intent':user_action['intent'],'request_slots':[],'inform_slots':[]}
        # print('========================')
        # print('agent action',agent_act)
        # print('========================')
        # agent_message = [random.choice(response_to_user_free_style[user_action['intent']])]

        #nếu là done thì reset và cho confirm về None
        if user_action['intent'] in ["done","thanks"]:
            state_tracker.reset()
            StateTracker_Container[state_tracker_id] = (state_tracker,None)
    print(f"dict_investigate: {dict_investigate}")
    # dict_investigate['semantic_frame']['agent'] = {}
    # dict_investigate['semantic_frame']['agent'] = agent_act
    # dict_investigate['semantic_frame']['agent']['message'] = agent_message
    # # dict_investigate['fail_pattern'] = 'success'
    # dict_investigate['timing'] = time.time() - start_time
    
    # # mongo.db.messages.insert_one(dict_investigate)  

    # return agent_message,agent_act

if __name__ == "__main__":
    state_tracker_id = 0
    message = "cho em xin Chỉ tiêu tuyển sinh năm 2020 của khối A1 ngành điện điện tử?"
    main(state_tracker_id, message)