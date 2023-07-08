import random
from .utils import load_pattern, string_matching
import regex as re
import os


class ResponseGeneration:
    def __init__(self, root: str):
        self.response_gallery = dict()
        default = load_pattern(os.path.join(root, "default_response.json"))
        template = load_pattern(os.path.join(root, "template_response.json"))
        self.response_gallery.update(default)
        self.response_gallery.update(template)

    def choose_reponses(self, gallery):
        sentence = random.choice(gallery)
        return [sentence]

    def free_style(self, intent):
        return [random.choice(self.response_gallery[intent])]

    def run(self, agent_action, state_tracker, confirm_obj, is_greeting=False):
        sentence_pattern = None
        list_sentence = []

        if is_greeting:
            return self.choose_reponses(self.response_gallery["greeting"])

        agent_intent = agent_action["intent"]

        if agent_intent == "inform":
            inform_slot = list(agent_action["inform_slots"].keys())[0]
            if agent_action["inform_slots"][inform_slot] == "no_match_available":
                return self.choose_reponses(self.response_gallery["not_found"])

            sentence_pattern = random.choice(
                self.response_gallery["inform"][inform_slot]
            )

            sentence = sentence_pattern.replace(
                "*{}*".format(inform_slot),
                self.response_gallery["agent_response_object"][inform_slot],
            )

            if len(agent_action["inform_slots"][inform_slot]) > 1:
                inform_value = ",\n".join(agent_action["inform_slots"][inform_slot])
                sentence = sentence.replace(
                    "*{}_instance*".format(inform_slot), '\n"{}"'.format(inform_value)
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

            list_sentence.append(sentence)

        elif agent_intent == "request":
            request_slot = list(agent_action["request_slots"].keys())[0]
            sentence_pattern = random.choice(
                self.response_gallery["request"][request_slot]
            )
            sentence = sentence_pattern.replace(
                "*{}*".format(request_slot),
                self.response_gallery["agent_response_object"][request_slot],
            )
            list_sentence.append(sentence)

        elif agent_intent == "done":
            return self.choose_reponses(self.response_gallery["done"])

        elif agent_intent == "match_found":
            inform_slot = state_tracker.current_request_slots[0]
            if agent_action["inform_slots"]["major"] == "no_match_available":
                sentence_pattern = random.choice(
                    self.response_gallery["match_found"]["not_found"]
                )
                sentence = sentence_pattern.replace(
                    "*found_slot*",
                    self.response_gallery["agent_response_object"][inform_slot],
                )
                list_sentence.append(sentence)

            else:
                list_record_match = list(agent_action["inform_slots"].values())[0]

                list_unique_slot_in_record_match = []
                for record in list_record_match:
                    result = record[inform_slot]
                    if result not in list_unique_slot_in_record_match:
                        list_unique_slot_in_record_match.append(result)
                response_match = ""
                if confirm_obj != None:
                    for item in list_unique_slot_in_record_match:
                        check_match = string_matching(confirm_obj[inform_slot], item)
                        if check_match:
                            break
                    value_match = ""
                    if len(confirm_obj[inform_slot]) > 1:
                        if inform_slot != "point":
                            value_match = ",\n".join(
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
                            value_match = " ,\n".join(
                                [str(item) for item in confirm_obj_non_limit]
                            )
                    else:
                        value_match = str(confirm_obj[inform_slot][0])
                    if check_match:
                        if inform_slot != "point":
                            response_match = (
                                "\n\nĐúng rồi! Thông tin {0} bạn cần là {1}".format(
                                    self.response_gallery["agent_response_object"][
                                        inform_slot
                                    ],
                                    value_match,
                                )
                            )
                        else:
                            response_match = "Chúc mừng bạn! Điểm của bạn cao hơn điểm chuẩn được công bố"
                    else:
                        if inform_slot != "point":
                            response_match = (
                                "\n\nSai rồi! Thông tin {0} không phải là {1}".format(
                                    self.response_gallery["agent_response_object"][
                                        inform_slot
                                    ],
                                    value_match,
                                )
                            )
                        else:
                            response_match = (
                                "Điểm của bạn thấp hơn điểm chuẩn được công bố!"
                            )
                    list_sentence.append(response_match)
                if inform_slot != "major":
                    if len(list_unique_slot_in_record_match) == 1:
                        sentence_pattern = random.choice(
                            self.response_gallery["match_found"]["found"]
                        )
                        sentence = sentence_pattern.replace(
                            "*found_slot*",
                            self.response_gallery["agent_response_object"][inform_slot],
                        )
                        first_record = list_unique_slot_in_record_match[0]
                        if len(first_record) > 1:
                            inform_value = ",\n".join(first_record)
                            sentence = sentence.replace(
                                "*found_slot_instance*", '\n"{}"'.format(inform_value)
                            )
                        elif len(first_record) == 1:
                            inform_value = first_record[0]
                            sentence = sentence.replace(
                                "*found_slot_instance*", '"{}"'.format(inform_value)
                            )
                        else:
                            sentence = self.response_gallery["empty_slot"][0].replace(
                                "*request_slot*",
                                self.response_gallery["agent_response_object"][
                                    inform_slot
                                ],
                            )

                        list_sentence.append(sentence)

                    else:
                        for item in list_unique_slot_in_record_match:
                            # print(item)
                            sentence_pattern = random.choice(
                                self.response_gallery["match_found"]["found"]
                            )
                            sentence = sentence_pattern.replace(
                                "*found_slot*",
                                self.response_gallery["agent_response_object"][
                                    inform_slot
                                ],
                            )
                            if len(item) > 1:
                                inform_value = ",\n".join(item)
                                sentence = sentence.replace(
                                    "*found_slot_instance*",
                                    '\n"{}"'.format(inform_value),
                                )
                            elif len(item) == 1:
                                inform_value = item[0]
                                sentence = sentence.replace(
                                    "*found_slot_instance*", '"{}"'.format(inform_value)
                                )
                            else:
                                sentence = self.response_gallery["empty_slot"][
                                    0
                                ].replace(
                                    "*request_slot*",
                                    self.response_gallery["agent_response_object"][
                                        inform_slot
                                    ],
                                )

                            list_sentence.append(sentence)
                else:
                    # print('here')
                    sentence = random.choice(
                        self.response_gallery["match_found"]["found_major"]
                    )
                    list_sentence.append(sentence)

        sentence_res = [item.replace(r'"', r"") for item in list_sentence]
        return sentence_res
