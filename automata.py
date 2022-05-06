from mdp import POLICIES_PATH, ACTIONS

import json
import time
import random


CYCLE = 20  # time between decisions


def generateInput():
    """
    Generates the input for the automata: [state, hour]
    """

    state = ""
    for i in range(3):
        if bool(random.randint(0, 1)):
            state += "H"
        else:
            state += "L"

    hour = random.randint(0, 23)
    
    return state, hour


def decide(state, hour, data):
    """
    Given an input state and hour, and the optimal policies data from the MPD,
    decides the best action.
    In case state is LLL (undefined, as it's goal state), it cycles through the
    actions.
    """
    global i

    if state == "LLL":  # do an action on a cycle
        action = ACTIONS[i]

        # update cycle
        i += 1
        if i >= len(ACTIONS):
            i = 0
    else:
        action = data[hour][state]

    return action


def run():
    """
    Run the automata. Outputs to the console the action for the generated data.
    """
    
    # load data from MDP model
    data = json.loads(POLICIES_PATH)

    i = 0  # count current cycle of rotating lights
    while True:
        state, hour = generateInput()
        action = decide(state, hour, data)

        print("Action:", action)

        time.sleep(CYCLE)


if __name__ == "__main__":
    run()