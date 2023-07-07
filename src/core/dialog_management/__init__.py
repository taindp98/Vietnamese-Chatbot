from .fsm_agent import FiniteStateMachineAgent
from .state_tracker import StateTracker

def get_agent_action(state_tracker, fsm_agent, user_action, done=False):
    
    if user_action['intent'] == 'request':
        state_tracker.reset()

    state_tracker.define_target()

    state_tracker.update_state_user(user_action)

    state_tracker.recursion_find_best_way()
    last_action_state_traker = state_tracker.list_state_tracker[-1]
    
    recursion_success = state_tracker.recursion_success
    _,agent_action = fsm_agent.get_action(last_action_state_traker,recursion_success,done)
    state_tracker.update_state_agent(agent_action,user_action)
    regex_constraint = state_tracker.regex_constraint
    return agent_action,regex_constraint