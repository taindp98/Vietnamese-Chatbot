import random
from .utils import load_pattern

class FiniteStateMachineAgent:
    """The finite state machine agent that interacts with the user."""

    def __init__(self):

        constants = load_pattern("./core/dialog_management/resources/constants.json")
        agent_inform_slots = constants['agent_inform_slots']
        agent_request_slots = constants['agent_request_slots']
        rule_requests = constants['rule_requests']

        agent_actions = [
            {
                'intent': 'done', 'inform_slots': {}, 'request_slots': {}
            }, 
            {
                'intent': 'match_found', 'inform_slots': {}, 'request_slots': {}
            }
        ]
        for slot in agent_inform_slots:
            # Must use intent match found to inform this, but still have to keep in agent inform slots
            if slot == "major":
                continue
            agent_actions.append(
                {
                    'intent': 'inform', 'inform_slots': {slot: 'PLACEHOLDER'}, 'request_slots': {}
                }
            )
        for slot in agent_request_slots:
            agent_actions.append(
                {'intent': 'request', 'inform_slots': {}, 'request_slots': {slot: 'UNK'}}
            )
        
        self.possible_actions = agent_actions
        self.num_actions = len(agent_actions)
        self.rule_request_set = rule_requests
        self.reset()

    def reset(self):
        """Resets the rule-based variables."""

        self.rule_current_slot_index = 0
        self.rule_phase = 'not done'

    def get_action(self, last_action_state_traker, recursion_success, done):
        index = 0
        slot = last_action_state_traker
        if recursion_success:
            rule_response = {'intent': 'match_found', 'inform_slots': {}, 'request_slots': {}}
        else:
            if not done:
                if random.randint(0,1) == 0:
                    rule_response = {'intent': 'request', 'inform_slots': {}, 'request_slots': {slot: 'UNK'}}
                else:
                    rule_response = {'intent': 'inform', 'inform_slots': {slot:'PLACEHOLDER'}, 'request_slots': {}}
            else:
                rule_response = {'intent': 'done', 'inform_slots': {}, 'request_slots': {}}
        return index, rule_response

    def _map_action_to_index(self, response):
        """
        Maps an action to an index from possible actions.

        Parameters:
            response (dict)

        Returns:
            int
        """

        for (i, action) in enumerate(self.possible_actions):
            if response == action:
                return i
        raise ValueError('Response: {} not found in possible actions'.format(response))