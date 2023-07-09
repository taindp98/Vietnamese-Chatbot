from .db_query import DBQuery
from .utils import convert_list_to_dict, load_pattern
import copy
import random
import pandas as pd
import itertools
import os


class StateTracker:
    """Tracks the state of the episode/conversation and prepares the state representation for the agent."""

    def __init__(self, root: str, database):
        """
        The constructor of StateTracker which creates a DB query object,
        creates necessary state rep. dicts, etc. and calls reset.

        Parameters:
            database (dict): The database with format dict(long: dict)
        """
        constants = load_pattern(os.path.join(root, "constants.json"))
        self.map_order_entity = load_pattern(os.path.join(root, "map_fsm.json"))
        self.history = []
        self.db_helper = DBQuery(root=root, database=database)
        self.match_key = constants["match_key"]
        self.intents_dict = convert_list_to_dict(constants["all_intents"])
        self.num_intents = len(constants["all_intents"])
        self.slots_dict = convert_list_to_dict(constants["all_slots"])
        self.num_slots = len(constants["all_slots"])
        self.reset()
        self.current_request_slots = []

        self.list_state_tracker = ["initial"]
        self.list_request = []
        self.list_input = []
        self.list_target = []
        self.all_slot = []
        self.pattern_target = []
        self.recursion_success = False

        self.flag_update_agent = False
        self.flag_update_user = False

        self.regex_constraint = {}

    def reset(self):
        """
        Resets current_informs, history and round_num.
        """

        self.current_informs = {}
        self.history = []
        self.round_num = 0
        self.current_request_slots = []

        self.list_state_tracker = ["initial"]
        self.list_request = []
        self.list_input = []
        self.list_target = []
        self.all_slot = []
        self.pattern_target = []
        self.recursion_success = False

    def print_history(self):
        """Helper function if you want to see the current history action by action."""

        for action in self.history:
            print(action)

    def update_state_agent(self, agent_action, user_action):
        """
        Updates the dialogue history with the agent's action and augments the agent's action.
        Takes an agent action and updates the history. 
        Also augments the agent_action param with query information and
        any other necessary information.

        Parameters:
            agent_action (dict):
                The agent action of format dict('intent': string, 'inform_slots': dict,
                'request_slots': dict) and changed to dict('intent': '', 'inform_slots': {},
                'request_slots': {}, 'round': int, 'speaker': 'Agent')

        """
        # print('current_informs --> constraints',self.current_informs)
        # print('agent action',agent_action['inform_slots'])
        db_results_dict = self.db_helper.get_db_results_for_slots(
            self.current_informs, user_action
        )

        if agent_action["intent"] == "inform":
            assert agent_action["inform_slots"]
            inform_slots = self.db_helper.fill_inform_slot(
                agent_action["inform_slots"], self.current_informs, user_action
            )
            agent_action["inform_slots"] = inform_slots
            assert agent_action["inform_slots"]
            key, value = list(agent_action["inform_slots"].items())[0]  # Only one
            assert key != "match_found"
            assert value != "PLACEHOLDER", "KEY: {}".format(key)
            self.current_informs[key] = value

        elif agent_action["intent"] == "match_found":
            assert not agent_action[
                "inform_slots"
            ], "Cannot inform and have intent of match found!"

            db_results = self.db_helper.get_db_results(
                self.current_informs, user_action
            )
            self.regex_constraint = self.db_helper.regex_constraint
            if db_results:
                db_results_no_empty = {}
                if self.current_request_slots[0] != self.match_key:
                    for key, value in db_results.items():
                        if (
                            isinstance(value[self.current_request_slots[0]], list)
                            and len(value[self.current_request_slots[0]]) > 0
                        ):
                            db_results_no_empty[key] = copy.deepcopy(value)
                if db_results_no_empty:
                    key, value = list(db_results_no_empty.items())[0]
                    value = list(db_results_no_empty.values())
                else:
                    key, value = list(db_results.items())[0]
                    value = list(db_results.values())

                agent_action["inform_slots"] = {key: copy.deepcopy(value)}
                agent_action["inform_slots"][self.match_key] = str(key)
            else:
                agent_action["inform_slots"][self.match_key] = "no_match_available"
            self.current_informs[self.match_key] = agent_action["inform_slots"][
                self.match_key
            ]
        agent_action.update({"round": self.round_num, "speaker": "Agent"})
        self.flag_update_agent = False
        self.history.append(agent_action)

        self.flag_update_agent = True

    def update_state_user(self, user_action):
        """
        Updates the dialogue history with the user's
        action and augments the user's action.

        Takes a user action and updates the history.
        Also augments the user_action param with necessary information.

        Parameters:
            user_action (dict): 
            The user action of format dict('intent': string, 'inform_slots': dict,
            'request_slots': dict) and changed to dict('intent': '', 'inform_slots': {},
            'request_slots': {}, 'round': int, 'speaker': 'User')
        """

        for key, value in user_action["inform_slots"].items():
            self.current_informs[key] = value

        for key, value in user_action["request_slots"].items():
            if key not in self.current_request_slots:
                self.current_request_slots.append(key)
        user_action.update({"round": self.round_num, "speaker": "User"})
        self.flag_update_user = False
        self.history.append(user_action)
        if self.round_num == 0 or user_action["intent"] == "request":
            self.all_slot = self.current_request_slots + list(
                self.current_informs.keys()
            )
            self.pattern_target = (
                self.all_slot
                + self.map_order_entity[self.current_request_slots[0]].copy()
            )
            self.list_state_tracker += self.all_slot
        self.round_num += 1
        self.flag_update_user = True

    def define_target(self):
        list_define_target = []

        for key in list(self.map_order_entity.keys()):
            if key != "all_slot":
                list_slot = self.map_order_entity[key]
                list_permute = list(itertools.permutations(list_slot))
                list_permute_fix = [
                    ["initial", key] + list(item) for item in list_permute
                ]

                for sublist_permute in list_permute_fix:
                    for idx, slot in enumerate(sublist_permute):
                        dict_target = {}
                        if idx < len(sublist_permute) - 2:
                            dict_target["request"] = key
                            dict_target["input"] = sublist_permute[idx : idx + 2]
                            dict_target["target"] = sublist_permute[idx + 2]

                            if dict_target not in list_define_target:
                                list_define_target.append(dict_target)
        df_define_target = pd.DataFrame(list_define_target)
        self.list_request = list(df_define_target["request"])
        self.list_input = list(df_define_target["input"])
        self.list_target = list(df_define_target["target"])

    def recursion_find_best_way(self, diversity=False):
        for item in self.list_state_tracker:
            if item != "initial" and item in self.pattern_target:
                self.pattern_target.remove(item)

        if len(self.pattern_target) == 0:
            # print('recursion sucess')
            self.recursion_success = True
            return True
        if diversity:
            for idx in range(len(self.list_state_tracker)):
                if idx < len(self.list_state_tracker) - 1:
                    window = self.list_state_tracker[idx : idx + 2]

                    ## add list choice
                    list_choice_action = []

                    for idx, sublist in enumerate(self.list_input):
                        if (
                            window == sublist
                            and self.current_request_slots[0] == self.list_request[idx]
                        ):
                            target_match = self.list_target[idx]

                            list_choice_action.append(target_match)

                    if list_choice_action:
                        choice_action = random.choice(list_choice_action)
                        while choice_action in self.list_state_tracker:
                            choice_action = random.choice(list_choice_action)

                        self.list_state_tracker.append(choice_action)
                        return True
        else:
            for idx in range(len(self.list_state_tracker)):
                if idx < len(self.list_state_tracker) - 1:
                    window = self.list_state_tracker[idx : idx + 2]

                    for idx, sublist in enumerate(self.list_input):
                        if (
                            window == sublist
                            and self.current_request_slots[0] == self.list_request[idx]
                        ):
                            target_match = self.list_target[idx]
                            ## update state tracker
                            if target_match not in self.list_state_tracker:
                                self.list_state_tracker.append(target_match)
                                return True
        # recursion
        self.recursion_find_best_way()
