import random


class FiniteStateMachineAgent:
    """
    The finite state machine agent that interacts with the user.
    """

    def __init__(self):
        pass

    def get_agent_action(self, state_tracker, user_action, done=False):
        if user_action["intent"] == "request":
            state_tracker.reset()

        state_tracker.define_target()

        state_tracker.update_state_user(user_action)

        state_tracker.recursion_find_best_way()
        last_action = state_tracker.list_state_tracker[-1]

        recursion_success = state_tracker.recursion_success

        agent_action_tmpl = {"intent": "", "inform_slots": {}, "request_slots": {}}
        if recursion_success:
            agent_action_tmpl["intent"] = "match_found"
        else:
            if not done:
                if random.randint(0, 1) == 0:
                    agent_action_tmpl["intent"] = "request"
                    agent_action_tmpl["request_slots"] = {last_action: "UNK"}
                else:
                    agent_action_tmpl["intent"] = "inform"
                    agent_action_tmpl["inform_slots"] = {last_action: "PLACEHOLDER"}
            else:
                agent_action_tmpl["intent"] = "done"

        agent_action = agent_action_tmpl

        state_tracker.update_state_agent(agent_action, user_action)
        regex_constraint = state_tracker.regex_constraint
        return agent_action, regex_constraint
