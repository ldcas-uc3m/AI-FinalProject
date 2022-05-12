from model import *

import json
import time
import random


CYCLE = 20  # time between decisions
i = 0  # current iteration of cycle (when LLL)


def generateRandomInput():
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


def decide(state: str, hour: int, data: dict):
    """
    Given an input state and hour, and the optimal policies data from the MPD,
    decides the best action.
    In case state is LLL (undefined, as it's goal state), it cycles through the
    actions.
    """
    global i

    if hour < 0 or hour > 23 or state not in STATES:
        print(hour, state)
        raise "Invalid Parameters"

    if state == "LLL":  # do an action on a cycle
        action = ACTIONS[i]

        # update cycle
        i += 1
        if i >= len(ACTIONS):
            i = 0
    else:
        action = data[str(hour)][state]

    return action


def runAutomata():
    """
    Run the automata. Outputs to the console and to LOGS_PATH the action for the generated data.
    """
    
    # load data from MDP model
    with open(POLICIES_PATH, 'r') as policies:
        data = json.load(policies)

    i = 0  # count current cycle of rotating lights
    while True:
        state, hour = generateRandomInput()
        action = decide(state, hour, data)

        # log data
        with open(LOGS_PATH, "a") as log_file:
            log_file.write("State: " + state + ", Hour: " + str(hour) + ", Action: " + action)

        print("State:", state, "\b, Hour:", hour, "\b, Action:", action)

        time.sleep(CYCLE)


if __name__ == "__main__":
    runAutomata()