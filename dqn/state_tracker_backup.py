from dqn.db_query import DBQuery
import numpy as np
from dqn.utils import convert_list_to_dict
from dqn.dialogue_config import all_intents, all_slots, usersim_default_key,agent_inform_slots,agent_request_slots
import copy
import time

class StateTracker:
    """Tracks the state of the episode/conversation and prepares the state representation for the agent."""

    def __init__(self, database, constants):
        """
        The constructor of StateTracker.

        The constructor of StateTracker which creates a DB query object, creates necessary state rep. dicts, etc. and
        calls reset.

        Parameters:
            database (dict): The database with format dict(long: dict)
            constants (dict): Loaded constants in dict

        """

        self.db_helper = DBQuery(database)
        self.match_key = usersim_default_key
        self.intents_dict = convert_list_to_dict(all_intents)
        self.num_intents = len(all_intents)
        self.slots_dict = convert_list_to_dict(all_slots)
        self.num_slots = len(all_slots)
        self.max_round_num = constants['run']['max_round_num']
        self.none_state = np.zeros(self.get_state_size())
        self.reset()
        self.current_request_slots = []
    def get_state_size(self):
        """Returns the state size of the state representation used by the agent."""

        return 2 * self.num_intents + 7 * self.num_slots + 3 + self.max_round_num

    def reset(self):
        """Resets current_informs, history and round_num."""

        self.current_informs = {}
        # A list of the dialogues (dicts) by the agent and user so far in the conversation
        self.history = []
        self.round_num = 0
        self.current_request_slots = []
    def print_history(self):
        """Helper function if you want to see the current history action by action."""

        for action in self.history:
            print(action)

    # def get_state(self, done=False,user_action):
    def get_state(self, done):

        """
        Returns the state representation as a numpy array which is fed into the agent's neural network.

        The state representation contains useful information for the agent about the current state of the conversation.
        Processes by the agent to be fed into the neural network. Ripe for experimentation and optimization.

        Parameters:
            done (bool): Indicates whether this is the last dialogue in the episode/conversation. Default: False

        Returns:
            numpy.array: A numpy array of shape (state size,)

        """

        # If done then fill state with zeros
        if done:
            return self.none_state

        user_action = self.history[-1]
        print('constraint',self.current_informs)
        db_results_dict = self.db_helper.get_db_results_for_slots(self.current_informs,user_action)
        print('db match',db_results_dict)
        last_agent_action = self.history[-2] if len(self.history) > 1 else None

        # Create one-hot of intents to represent the current user action
        user_act_rep = np.zeros((self.num_intents,))
        user_act_rep[self.intents_dict[user_action['intent']]] = 1.0

        # Create bag of inform slots representation to represent the current user action
        user_inform_slots_rep = np.zeros((self.num_slots,))
        for key in user_action['inform_slots'].keys():
            user_inform_slots_rep[self.slots_dict[key]] = 1.0

        # Create bag of request slots representation to represent the current user action
        user_request_slots_rep = np.zeros((self.num_slots,))
        # for key in user_action['request_slots'].keys():
            # user_request_slots_rep[self.slots_dict[key]] = 1.0

        # print('current_request_slots new', self.current_request_slots)
        # print('current_request_slots old', user_action['request_slots'])
        for key in self.current_request_slots:
            user_request_slots_rep[self.slots_dict[key]] = 1.0
        #
        # Create bag of filled_in slots based on the current_slots
        current_slots_rep = np.zeros((self.num_slots,))
        for key in self.current_informs:
            current_slots_rep[self.slots_dict[key]] = 1.0

        # Encode last agent intent
        agent_act_rep = np.zeros((self.num_intents,))
        if last_agent_action:
            agent_act_rep[self.intents_dict[last_agent_action['intent']]] = 1.0

        # Encode last agent inform slots
        agent_inform_slots_rep = np.zeros((self.num_slots,))
        # print(last_agent_action)
        if last_agent_action:
            for key in last_agent_action['inform_slots'].keys():
                if key in agent_inform_slots:
                    agent_inform_slots_rep[self.slots_dict[key]] = 1.0

        # Encode last agent request slots
        agent_request_slots_rep = np.zeros((self.num_slots,))
        if last_agent_action:
            for key in last_agent_action['request_slots'].keys():
                if key in agent_request_slots:
                    agent_request_slots_rep[self.slots_dict[key]] = 1.0

        # Value representation of the round num
        turn_rep = np.zeros((1,)) + self.round_num / 5.

        # One-hot representation of the round num
        turn_onehot_rep = np.zeros((self.max_round_num,))
        turn_onehot_rep[self.round_num - 1] = 1.0

        # Representation of DB query results (scaled counts)
        kb_count_rep = np.zeros((self.num_slots + 1,)) + db_results_dict['matching_all_constraints'] / 100.
        for key in db_results_dict.keys():
            if key in self.slots_dict:
                kb_count_rep[self.slots_dict[key]] = db_results_dict[key] / 100.

        # Representation of DB query results (binary)
        kb_binary_rep = np.zeros((self.num_slots + 1,)) + np.sum(db_results_dict['matching_all_constraints'] > 0.)
        for key in db_results_dict.keys():
            if key in self.slots_dict:
                kb_binary_rep[self.slots_dict[key]] = np.sum(db_results_dict[key] > 0.)


        ########################
        # represent current slot has value in db result
        db_binary_slot_rep = np.zeros((self.num_slots + 1,))

        # print('>'*50,self.current_informs,user_action)
        db_results = self.db_helper.get_db_results(self.current_informs,user_action)
        # print('>'*50)
        # print('dbquery',db_results)
        # print('>'*50)
        if db_results:
            # Arbitrarily pick the first value of the dict
            key, data = list(db_results.items())[0]
            # print("size state: {} ".format(self.num_slots + 1))
            # print("first value:   {}".format(data))
            for slot, value in data.items():
                if slot in self.slots_dict and isinstance(value, list) and len(value) > 0:
                    # if slot not in self.current_request_slots:
                    db_binary_slot_rep[self.slots_dict[slot]] = 1.0


        ########################


        state_representation = np.hstack(
            [user_act_rep, user_inform_slots_rep, user_request_slots_rep, agent_act_rep, agent_inform_slots_rep,
             agent_request_slots_rep, current_slots_rep, turn_rep, turn_onehot_rep, kb_binary_rep,
             kb_count_rep]).flatten()
        # print("---------------------------------------state")
        # print(state_representation)
        # time.sleep(0.5)
        return state_representation

    def update_state_agent(self, agent_action,user_action):
        """
        Updates the dialogue history with the agent's action and augments the agent's action.

        Takes an agent action and updates the history. Also augments the agent_action param with query information and
        any other necessary information.

        Parameters:
            agent_action (dict): The agent action of format dict('intent': string, 'inform_slots': dict,
                                 'request_slots': dict) and changed to dict('intent': '', 'inform_slots': {},
                                 'request_slots': {}, 'round': int, 'speaker': 'Agent')

        chỉ query khi có có current inform khi agent action là inform
        """

        if agent_action['intent'] == 'inform':
            assert agent_action['inform_slots']
            # print('$'*50)
            # print('current_informs upd state agent',self.current_informs)
            # print('agent action',agent_action['inform_slots'])
            inform_slots = self.db_helper.fill_inform_slot(agent_action['inform_slots'], self.current_informs,user_action)
            # print('slot predict and suggest',inform_slots)
            agent_action['inform_slots'] = inform_slots
            assert agent_action['inform_slots']
            key, value = list(agent_action['inform_slots'].items())[0]  # Only one
            # print(list(agent_action['inform_slots'].items()))
            assert key != 'match_found'
            assert value != 'PLACEHOLDER', 'KEY: {}'.format(key)
            self.current_informs[key] = value

            # print('%'*50)
            # print('current_informs upd state agent',self.current_informs)
        # If intent is match_found then fill the action informs with the matches informs (if there is a match)
        elif agent_action['intent'] == 'match_found':
            assert not agent_action['inform_slots'], 'Cannot inform and have intent of match found!'

            # print('>'*50)
            # print('match_found',self.match_key,agent_action['inform_slots'])
            # print('>'*50)

            db_results = self.db_helper.get_db_results(self.current_informs,user_action)
            if db_results:
                # Arbitrarily pick the first value of the dict
                db_results_no_empty = {}
                if self.current_request_slots[0] != usersim_default_key:
                    for key, value in db_results.items():
                        if isinstance(value[self.current_request_slots[0]], list) and len(value[self.current_request_slots[0]]) > 0:
                            db_results_no_empty[key] = copy.deepcopy(value)
                if db_results_no_empty:
                    key, value = list(db_results_no_empty.items())[0]
                    value = list(db_results_no_empty.values())
                else:

                    ## lấy key đầu tiên trong list db query được
                    key, value = list(db_results.items())[0]
                    value = list(db_results.values())

                agent_action['inform_slots'] = {key: copy.deepcopy(value)}
                agent_action['inform_slots'][self.match_key] = str(key)
            else:
                agent_action['inform_slots'][self.match_key] = 'no match available'
            self.current_informs[self.match_key] = agent_action['inform_slots'][self.match_key]
        agent_action.update({'round': self.round_num, 'speaker': 'Agent'})
        self.history.append(agent_action)

    def update_state_user(self, user_action):
        """
        Updates the dialogue history with the user's action and augments the user's action.

        Takes a user action and updates the history. Also augments the user_action param with necessary information.

        Parameters:
            user_action (dict): The user action of format dict('intent': string, 'inform_slots': dict,
                                 'request_slots': dict) and changed to dict('intent': '', 'inform_slots': {},
                                 'request_slots': {}, 'round': int, 'speaker': 'User')

        """

        for key, value in user_action['inform_slots'].items():
            self.current_informs[key] = value

        for key, value in user_action['request_slots'].items():
            if key not in self.current_request_slots:
                self.current_request_slots.append(key)
        user_action.update({'round': self.round_num, 'speaker': 'User'})
        self.history.append(user_action)
        self.round_num += 1
