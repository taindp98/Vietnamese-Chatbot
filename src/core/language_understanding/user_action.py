from .intent_recognize import IntentRecognition
from .entity_recognize import EntityRecognition
"""
LIST INTENT PATTERN MATCHING
'major_code',
'duration',
'location',
'public_transport',
'accommodation',
'address',
'out_come',
'group',
'tuition',
'point',
'greet',
'farewell'

LIST INTENT FASTAI
'general_career',
'general_rate',
'general_company',
'general_major'
"""
class UserUnderstand:
    def __init__(self):
        self.intent_recognizer = IntentRecognition(ai_service=None)
        self.entity_recognizer = EntityRecognition()
        self.default_intent = "not_intent"
        self.confirm_obj = None
        
        self.ignore_intent = [
            'agree',
            'disagree',
            'greeting', 
            'fare_well', 
            'other', 
            'anything', 
            'thanks', 
            'not_intent'
        ]

    def process(self, mess: str, state_tracker):
        
        user_action = {
            "intent": None,
            "inform_slots": {},
            "request_slots": {},
            "catch_intent": {
                "intent": self.default_intent,
                "confidence_score": 1.0
            },

        }

        if isinstance(mess, str):
            if not mess.startswith('/'):
                catched_intent, prob, cleaned_mess = self.intent_recognizer.predict(mess)

                user_action['catch_intent']['intent'] = catched_intent
                user_action['catch_intent']['confidence_score'] = prob

                if not catched_intent in self.ignore_intent:
                    user_action['intent'] = 'request'
                    dict_entity_inform, confirm_obj = self.entity_recognizer.find(catched_intent,cleaned_mess)
                    user_action['inform_slots'] = dict_entity_inform
                    user_action['request_slots'] = {catched_intent:'UNK'}

                elif catched_intent in ['not_intent']:
                    last_agent_action = state_tracker.history[-1]
                    if last_agent_action['intent'] != 'match_found':
                        user_inform_key = None
                        slot_inform = None
                        if len(list(last_agent_action['request_slots'].keys())) > 0:
                            user_inform_key = list(last_agent_action['request_slots'].keys())[0]

                        elif len(list(last_agent_action['inform_slots'].keys())) > 0:
                            user_inform_key = list(last_agent_action['inform_slots'].keys())[0]

                        if len(list(last_agent_action['request_slots'].keys())) > 0 or len(list(last_agent_action['inform_slots'].keys())) > 0:
                            final_intent = user_inform_key + '_inform'
                        else:
                            final_intent = 'not_intent'
                        user_action['inform_slots'],confirm_obj = self.entity_recognizer.find(final_intent,cleaned_mess)
                        user_action['intent'] = 'inform'
                        user_action['request_slots'] = {}
                    else:
                        ## avoid to crash
                        other_key_avoid_crash = 'major_name'
                        user_action['intent'] = 'inform'
                        user_action['inform_slots'] = {other_key_avoid_crash:'anything'}
                        user_action['request_slots'] = {}

                elif catched_intent in ['agree','disagree']:
                    last_agent_action = state_tracker.history[-1]

                    if last_agent_action['intent'] != 'match_found':
                        user_inform_key = None
                        slot_inform = None
                        if len(list(last_agent_action['request_slots'].keys())) > 0:
                            user_inform_key = list(last_agent_action['request_slots'].keys())[0]

                        if len(list(last_agent_action['inform_slots'].keys())) > 0:
                            user_inform_key = list(last_agent_action['inform_slots'].keys())[0]
                        if len(list(last_agent_action['request_slots'].keys())) > 0 or len(list(last_agent_action['inform_slots'].keys())) > 0:
                            final_intent = user_inform_key + '_inform'
                        else:
                            final_intent = 'not_intent'
                        user_action['intent'] = 'inform'
                        user_action['request_slots'] = {}

                        if catched_intent == 'agree':
                            user_action['inform_slots'] = dict(last_agent_action['inform_slots'].items())
                        else:
                            ## fix entity

                            dict_fix_entity,confirm_obj = self.entity_recognizer.find(final_intent,cleaned_mess)

                            if not dict_fix_entity:
                                user_action['inform_slots'] = {}
                                user_action['inform_slots'][user_inform_key] = 'anything'
                            else:
                                user_action['inform_slots'] = dict_fix_entity

                elif catched_intent == 'anything':
                    anything_key = None
                    last_agent_action = state_tracker.history[-1]
                    if len(list(last_agent_action['request_slots'].keys())) > 0:
                        anything_key = list(last_agent_action['request_slots'].keys())[0]
                    elif len(list(last_agent_action['inform_slots'].keys())) > 0:
                        anything_key = list(last_agent_action['inform_slots'].keys())[0]

                    if not anything_key:
                        anything_key = "major_name"
                    user_action['intent'] = 'inform'
                    user_action['inform_slots'] = {anything_key:'anything'}
                    user_action['request_slots'] = {}

                else:
                    user_action['intent'] = catched_intent
                    user_action['inform_slots'] = {}
                    user_action['request_slots'] = {}

            elif mess == '/start':
                user_action['intent'] = 'start'
                user_action['inform_slots'] = {}
                user_action['request_slots'] = {}
                user_action['catch_intent'] = {}
                user_action['catch_intent']['intent'] = "not_intent"
                user_action['catch_intent']['confidence_score'] = 1.0

        return user_action, confirm_obj