# Special slot values (for reference)
'PLACEHOLDER'  # For informs
'UNK'  # For requests
'anything'  # means any value works for the slot with this value
'no match available'  # When the intent of the agent is match_found yet no db match fits current constraints

#######################################
# Usersim Config
#######################################
# Used in EMC for intent error (and in user)
usersim_intents = ['inform', 'request', 'thanks', 'reject', 'done']

# The goal of the agent is to inform a match for this key
# usersim_default_key = 'activity'
# usersim_default_key = 'ticket'
usersim_default_key = 'major'

# Required to be in the first action in inform slots of the usersim if they exist in the goal inform slots
# usersim_required_init_inform_keys = ['moviename']

# usersim_required_init_inform_keys = ['name_activity']
usersim_required_init_inform_keys = ['major_name']

#######################################
# Agent Config
#######################################

# Possible inform and request slots for the agent
# agent_inform_slots = ['major_name', 'type_edu', 'career', 'subject','tuition', 'subject_group','point','major_code','year','satisfy',usersim_default_key]
agent_inform_slots = ['major_name','type_edu','subject_group','year','case','point','career','subject','tuition','major_code','criteria','object','register',usersim_default_key]
agent_request_slots = ['major_name', 'type_edu','subject_group','year','case','point']
# agent_request_slots = ['major_name','type_edu','subject_group','year','case','point','career','subject','tuition','major_code','criteria','object','register']

# Possible actions for agent
agent_actions = [
    {'intent': 'done', 'inform_slots': {}, 'request_slots': {}},  # Triggers closing of conversation
    {'intent': 'match_found', 'inform_slots': {}, 'request_slots': {}}
]
for slot in agent_inform_slots:
    # Must use intent match found to inform this, but still have to keep in agent inform slots
    if slot == usersim_default_key:
        continue
    agent_actions.append({'intent': 'inform', 'inform_slots': {slot: 'PLACEHOLDER'}, 'request_slots': {}})
for slot in agent_request_slots:
    agent_actions.append({'intent': 'request', 'inform_slots': {}, 'request_slots': {slot: 'UNK'}})

# Rule-based policy request list

rule_requests = ['major_name', 'type_edu','subject_group','year','case','point']
# rule_requests =['major_name','type_edu','point','year','career','subject','tuition','subject_group','case','major_code','criteria','object']


# These are possible inform slot keys that cannot be used to query
no_query_keys = [usersim_default_key,'_id']

#######################################
# Global config
#######################################

# These are used for both constraint check AND success check in usersim
FAIL = -1
NO_OUTCOME = 0
SUCCESS = 1
UNSUITABLE = -2

# All possible intents (for one-hot conversion in ST.get_state())
all_intents = ['inform', 'request', 'done', 'match_found', 'thanks', 'reject']

# All possible slots (for one-hot conversion in ST.get_state())
all_slots = ['major_name','type_edu','subject_group','year','case','point','career','subject','tuition','major_code','criteria','object','register',usersim_default_key]
# all_slots = ['major_name', 'type_edu', 'career', 'subject','tuition', 'subject_group','point','major_code','year','satisfy',usersim_default_key]
