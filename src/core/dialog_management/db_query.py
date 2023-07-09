from collections import defaultdict
import copy
import re
import os

from .utils import load_pattern

class DBQuery:
    """Queries the database for the state tracker."""

    def __init__(self, root: str, database):
        """
        The constructor for DBQuery.

        Parameters:
            database (dict): The database in the format dict(long: dict)
        """

        self.database = database
        self.cached_db_slot = defaultdict(dict)
        self.cached_db = defaultdict(dict)
        constants = load_pattern(os.path.join(root, "constants.json"))
        self.match_key = constants["match_key"]
        self.no_query = [self.match_key, "_id"]
        self.regex_constraint = {}

    def fill_inform_slot(self, inform_slot_to_fill, current_inform_slots, user_action):
        """
        Given the current informs/constraints fill the informs that need to be filled with values from the database.

        Searches through the database to fill the inform slots with PLACEHOLDER with values that work given the current
        constraints of the current episode.

        Parameters:
            inform_slot_to_fill (dict): Inform slots to fill with values
            current_inform_slots (dict): Current inform slots with values 
            from the StateTracker

        Returns:
            dict: inform_slot_to_fill filled with values
        """

        # For this simple system only one inform slot should ever passed in
        assert len(inform_slot_to_fill) == 1

        key = list(inform_slot_to_fill.keys())[0]

        current_informs = copy.deepcopy(current_inform_slots)
        current_informs.pop(key, None)

        db_results = self.get_db_results(current_informs, user_action)
        filled_inform = {}
        values_dict = self._count_slot_values(key, db_results)
        if key == self.match_key:
            filled_inform[key] = list(db_results)[0]
        elif values_dict:
            filled_inform[key] = list(max(values_dict, key=values_dict.get))

        else:
            filled_inform[key] = "no_match_available"

        return filled_inform

    def _count_slot_values(self, key, db_subdict):
        """
        Return a dict of the different values and occurrences of each,
        given a key, from a sub-dict of database

        Parameters:
            key (string): The key to be counted
            db_subdict (dict): A sub-dict of the database

        Returns:
            dict: The values and their occurrences given the key
        """

        slot_values = defaultdict(int)  # init to 0
        # print(slot_values)
        for id in db_subdict.keys():
            current_option_dict = db_subdict[id]
            # If there is a match
            if key in current_option_dict.keys():
                slot_value = current_option_dict[key]
                # print(slot_value)
                if any(isinstance(i, list) for i in slot_value):
                    slot_value = [
                        value for sub_list in slot_value for value in sub_list
                    ]

                tp_slot_value = tuple(slot_value)
                slot_values[tp_slot_value] += 1
        return slot_values

    def check_match_sublist_and_substring(self, list_children, list_parent):
        count_match = 0
        for children_value in list_children:
            for parent_value in list_parent:
                if children_value in parent_value:
                    count_match += 1
                    break
        if count_match == len(list_children):
            return True
        return False

    def convert_to_regex_constraint(self, key, values):
        or_list = []
        final_list = []
        or_dict = {}
        if key != "point":
            print(values)
            if len(values) > 1:
                for value in values:
                    all_dict = {}
                    all_dict[key] = {"$all": [re.compile(value)]}
                    or_list.append(all_dict)
                or_dict["$or"] = or_list
                final_list.append(or_dict)
            else:
                all_dict = {}
                all_dict[key] = {"$all": [re.compile(values[0])]}
                final_list.append(all_dict)
        else:
            all_dict = {}
            all_dict["point"] = {"$gte": values[0], "$lte": values[1]}
            final_list.append(all_dict)
        return final_list[0]

    def convert_constraint(self, constraints):
        """
        input dict for each slot {entity_slot:[entity_mess]}
        return câu query mongodb
        form of query string: { "$and": [{entity_slot:{"$all":[re.compile("entity_mess")]}},{},{}] }
        """

        list_and_out = []
        list_and_in = []
        regex_constraint_dict = {}
        for keys, values in constraints.items():
            if keys != "point":
                if not type(values) is list:
                    values = []
                for value in values:
                    list_and_in.append(
                        {
                            "$or": [
                                {keys: {"$all": [re.compile(".*{0}.*".format(value))]}}
                            ]
                        }
                    )
            else:
                if len(values) > 1:
                    list_and_in.append(
                        {"point": {"$gte": values[0], "$lte": values[1]}}
                    )
        if list_and_in:
            list_and_out.append({"$and": list_and_in})
        if list_and_out:
            regex_constraint_dict = {"$and": list_and_out}
        return regex_constraint_dict

    def get_db_results(self, constraints, user_action):
        """
        Get all items in the database that fit the current constraints.

        Looks at each item in the database and if its slots contain all constraints
        and their values match then the item
        is added to the return dict.

        Parameters:
            constraints (dict): The current informs

        Returns:
            dict: The available items in the database
        """

        new_constraints = {
            k: v
            for k, v in constraints.items()
            if k not in self.no_query and v is not "anything"
        }
        tuple_new_constraint = copy.deepcopy(new_constraints)
        inform_items = {k: tuple(v) for k, v in tuple_new_constraint.items()}.items()
        inform_items = frozenset(inform_items)

        cache_return = self.cached_db[inform_items]

        if cache_return == None:
            return {}
        if cache_return:
            return cache_return

        available_options = {}

        self.regex_constraint = self.convert_constraint(new_constraints)
        results = self.database.general.find(self.regex_constraint)
        for result in results:
            result["_id"] = str(result["_id"])
            available_options.update({result["_id"]: result})
            self.cached_db[inform_items].update({result["_id"]: result})

        if not available_options:
            self.cached_db[inform_items] = None

        return available_options

    def get_db_results_for_slots(self, current_informs, user_action):
        """
        Counts occurrences of each current inform slot (key and value)
        in the database items.

        For each item in the database and each current inform slot if
        that slot is in the database item (matches key
        and value) then increment the count for that key by 1.

        Parameters:
            current_informs (dict): The current informs/constraints

        Returns:
            dict: Each key in current_informs with the count of the number
            of matches for that key
        """

        tuple_current_informs = copy.deepcopy(current_informs)
        inform_items = {k: tuple(v) for k, v in tuple_current_informs.items()}.items()
        inform_items = frozenset(inform_items)
        cache_return = self.cached_db_slot[inform_items]

        temp_current_informs = copy.deepcopy(current_informs)
        if cache_return:
            return cache_return

        # Init all key values with 0
        db_results = {key: 0 for key in current_informs.keys()}
        db_results["matching_all_constraints"] = 0

        for CI_key, CI_value in current_informs.items():
            # Skip if a no query item and all_slots_match stays true
            if CI_key in self.no_query:
                continue
            if CI_value == "anything":
                db_results[CI_key] = self.database.general.count()
                # db_results[CI_key] += 1
                del temp_current_informs[CI_key]
                continue

            db_results[CI_key] = self.database.general.count(
                self.convert_constraint({CI_key: CI_value})
            )

        db_results["matching_all_constraints"] = self.database.general.count(
            self.convert_constraint(temp_current_informs)
        )

        self.cached_db_slot[inform_items].update(db_results)
        assert self.cached_db_slot[inform_items] == db_results
        return db_results
