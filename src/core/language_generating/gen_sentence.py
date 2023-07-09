import random
from .utils import load_pattern, string_matching
import os


class ResponseGeneration:
    def __init__(self, root: str):
        self.response_gallery = dict()
        default = load_pattern(os.path.join(root, "default_response.json"))
        template = load_pattern(os.path.join(root, "template_response.json"))
        constants = load_pattern(os.path.join(root, "constants.json"))

        self.match_key = constants["match_key"]
        self.response_gallery.update(default)
        self.response_gallery.update(template)

    def choose_responses(self, gallery):
        sentence = random.choice(gallery)
        return [sentence]

    def free_style(self, intent):
        return [random.choice(self.response_gallery[intent])]

    def response_inform(self, agent_action):
        sentence_pattern = None
        inform_slot = list(agent_action["inform_slots"].keys())[0]
        if agent_action["inform_slots"][inform_slot] == "no_match_available":
            return self.choose_responses(self.response_gallery["not_found"])

        sentence_pattern = random.choice(self.response_gallery["inform"][inform_slot])

        sentence = sentence_pattern.replace(
            "*{}*".format(inform_slot),
            self.response_gallery["agent_response_object"][inform_slot],
        )

        if len(agent_action["inform_slots"][inform_slot]) > 1:
            inform_value = ", ".join(agent_action["inform_slots"][inform_slot])
            sentence = sentence.replace(
                "*{}_instance*".format(inform_slot), ' "{}"'.format(inform_value)
            )

        elif len(agent_action["inform_slots"][inform_slot]) == 1:
            inform_value = agent_action["inform_slots"][inform_slot][0]
            sentence = sentence.replace(
                "*{}_instance*".format(inform_slot), '"{}"'.format(inform_value)
            )
        else:
            sentence_pattern = random.choice(self.response_gallery["empty_slot"])
            sentence = sentence_pattern.replace(
                "*request_slot*",
                self.response_gallery["agent_response_object"][inform_slot],
            )

        return [sentence]

    def response_request(self, agent_action):
        sentence_pattern = None
        request_slot = list(agent_action["request_slots"].keys())[0]
        sentence_pattern = random.choice(self.response_gallery["request"][request_slot])
        sentence = sentence_pattern.replace(
            "*{}*".format(request_slot),
            self.response_gallery["agent_response_object"][request_slot],
        )
        return [sentence]

    def _merge_found_results(self, inform_slot, found_result):
        sentence_pattern = random.choice(
            self.response_gallery["match_found"]["found"]
        )
        sentence = sentence_pattern.replace(
            "*found_slot*",
            self.response_gallery["agent_response_object"][inform_slot],
        )
        if len(found_result) > 1:
            inform_value = ", ".join(found_result)
            sentence = sentence.replace(
                "*found_slot_instance*", ' "{}"'.format(inform_value)
            )
        elif len(found_result) == 1:
            inform_value = found_result[0]
            sentence = sentence.replace(
                "*found_slot_instance*", '"{}"'.format(inform_value)
            )
        else:
            sentence = self.response_gallery["empty_slot"][0].replace(
                "*request_slot*",
                self.response_gallery["agent_response_object"][inform_slot],
            )
        return sentence

    def response_match_found(self, state_tracker, agent_action, confirm_obj):
        sentence_pattern = None
        inform_slot = state_tracker.current_request_slots[0]
        list_responses = []
        if agent_action["inform_slots"][self.match_key] == "no_match_available":
            sentence_pattern = random.choice(
                self.response_gallery["match_found"]["not_found"]
            )
            sentence = sentence_pattern.replace(
                "*found_slot*",
                self.response_gallery["agent_response_object"][inform_slot],
            )
            list_responses.append(sentence)

        else:
            # match found
            list_record_match = list(agent_action["inform_slots"].values())[0]

            list_matched_slot = []
            for record in list_record_match:
                result = record[inform_slot]
                if result not in list_matched_slot:
                    list_matched_slot.append(result)
            response_match = ""
            if confirm_obj:
                for item in list_matched_slot:
                    check_match = string_matching(
                        confirm_obj[inform_slot], item
                    )
                    if check_match:
                        break
                
                value_match = ""
                if len(confirm_obj[inform_slot]) > 1:
                    if inform_slot != "point":
                        value_match = ", ".join(
                            [str(item) for item in confirm_obj[inform_slot]]
                        )
                    else:
                        confirm_obj_non_limit = []
                        for item in confirm_obj[inform_slot]:
                            if (
                                item != float(0)
                                and item != float(100)
                                and item != float(1000)
                            ):
                                confirm_obj_non_limit.append(item)
                        value_match = ", ".join(
                            [str(item) for item in confirm_obj_non_limit]
                        )
                else:
                    value_match = str(confirm_obj[inform_slot][0])
                if check_match:
                    if inform_slot != "point":
                        response_match = (
                            self.response_gallery["match_found"]["agree"][0]
                            .replace(
                                "*arg1*",
                                self.response_gallery["agent_response_object"][
                                    inform_slot
                                ],
                            )
                            .replace("*arg2*", value_match)
                        )
                    else:
                        response_match = self.response_gallery["match_found"][
                            "point_congrats"
                        ][0]
                else:
                    if inform_slot != "point":
                        response_match = (
                            self.response_gallery["match_found"]["disagree"][0]
                            .replace(
                                "*arg1*",
                                self.response_gallery["agent_response_object"][
                                    inform_slot
                                ],
                            )
                            .replace("*arg2*", value_match)
                        )
                    else:
                        response_match = self.response_gallery["match_found"][
                            "point_condolences"
                        ][0]

                list_responses.append(response_match)

            if inform_slot != self.match_key:
                if len(list_matched_slot) == 1:
                    sentence = self._merge_found_results(
                        inform_slot, list_matched_slot[0]
                    )
                    list_responses.append(sentence)
                else:
                    for item in list_matched_slot:
                        sentence = self._merge_found_results(
                            inform_slot, item
                        )
                        list_responses.append(sentence)
            else:
                sentence = random.choice(
                    self.response_gallery["match_found"]["found_major"]
                )
                list_responses.append(sentence)
        return list_responses

    def run(self, agent_action, state_tracker, confirm_obj, is_greeting=False):
        if is_greeting:
            return self.choose_responses(self.response_gallery["greeting"])

        agent_intent = agent_action["intent"]

        if agent_intent == "inform":
            responses = self.response_inform(agent_action)

        elif agent_intent == "request":
            responses = self.response_request(agent_action)

        elif agent_intent == "done":
            responses = self.choose_responses(self.response_gallery["done"])

        elif agent_intent == "match_found":
            responses = self.response_match_found(
                state_tracker=state_tracker,
                agent_action=agent_action,
                confirm_obj=confirm_obj,
            )

        sentence_res = [item.replace(r'"', r"") for item in responses]
        print(f"sentence_res: {sentence_res}")
        return sentence_res
