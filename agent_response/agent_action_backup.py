from dqn.user_simulator import UserSimulator
from dqn.error_model_controller import ErrorModelController
from dqn.dqn_agent import DQNAgent
from dqn.state_tracker import StateTracker
# import pickle, argparse, json
# from dqn.user import User
# from dqn.utils import remove_empty_slots
from nlg.gen_sentence import *
# import pymongo
def get_agent_action(state_tracker,dqn_agent,user_action,done=False):
    print('='*100)
    print(user_action)
    state_tracker.update_state_user(user_action)
    print('-----update state user')
    print(user_action)
    print('-----update state user')
    # current_state = state_tracker.get_state(done)
    # print('-----get current_state')
    # print(current_state)
    current_state = None
    _, agent_action = dqn_agent.get_action(current_state)
    print('-----get agent action')
    print(agent_action)
    print('-----get agent action')
    state_tracker.update_state_agent(agent_action,user_action)
    print('-----update agent action')
    print(agent_action)
    print('-----update agent action')
    return agent_action
