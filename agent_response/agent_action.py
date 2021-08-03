from dqn.user_simulator import UserSimulator
from dqn.error_model_controller import ErrorModelController
from dqn.dqn_agent import DQNAgent
from dqn.state_tracker import StateTracker
# import pickle, argparse, json
# from dqn.user import User
# from dqn.utils import remove_empty_slots
from nlg.gen_sentence import *
# import pymongo
import requests
def get_agent_action(state_tracker,dqn_agent,user_action,done=False):
    # print('='*100)
    # print(user_action)

    ## define target
    if user_action['intent'] == 'request':
        state_tracker.reset()

    state_tracker.define_target()

    state_tracker.update_state_user(user_action)

    # print('all_slot',state_tracker.all_slot)
    # print('pattern_target',state_tracker.pattern_target)
    # print('target',state_tracker.list_input)
    # current_state = state_tracker.get_state(done)
    # print('-----get current_state')
    # print(current_state)

    state_tracker.recursion_find_best_way()
    last_action_state_traker = state_tracker.list_state_tracker[-1]
    # print('last_action_state_traker',last_action_state_traker)

    # current_state = None
    # _, agent_action = dqn_agent.get_action(current_state)
    recursion_success = state_tracker.recursion_success
    _,agent_action = dqn_agent.get_action(last_action_state_traker,recursion_success,done)

    # print('-----get agent action')
    # print(agent_action)
    # print('-----get agent action')
    state_tracker.update_state_agent(agent_action,user_action)
    # print('-----update agent action')
    # print(agent_action)
    # print('-----update agent action')
    return agent_action

def get_prob_agent_action(user_action):
    url = 'https://api-dqn.herokuapp.com/predict'
    try:
        pred = requests.post(url,json={'user_action':user_action})
        # weight for class predict
        dict_pred = pred.json()
        conf_score = dict_pred['confidence_score']
        return conf_score
    except:
        conf_score = 0
        return conf_score
