# test if our solution is optimum

from model import *
from mdp import runMDP
from automata import decide as automata_decide
from automata import generateRandomInput

import random
import json


RESULTS_PATH = "output/test_results.json"


def dummy_decide(state: str, hour: int):
    # unoptimized dummy automata, just output a random action
    return random.choice(ACTIONS)


def nextState(hour: int, init_state: str, action: str, probabilities: dict):
    """
    Taking an state, hour, and an action, calculates the next state using the probabilities on the
    parameter probabilities (expecting the format of probabilities.json).
    """

    # build choices
    choices = []
    weights = []
    for transition in probabilities[str(hour)][action]:
        if transition[:3] == init_state:
            choices.append(transition[5:])
            weights.append(probabilities[str(hour)][action][transition])

    # roll probabilities
    state = random.choices(choices, weights)[0]  # for some weird reason this function returns a list

    return state


def test(iterations: int = 100):
    """
    Simulate the real world problem using the data, and evaluate the time it takes to
    reach the final state, LLL, comparing the automata to a dummy.
    First, generate a random input state and hour, wait for the actions from the machines,
    and use the probabilities generated from the MDP to generate the next state.
    We count the number of actions taken, and obtain the results of the iterations,
    saving them to RESULTS_PATH, with the format:
    {
        <iteration1>: {
            "automata": {
                "path": [
                    <state1>,
                    <state2>,
                    [...]
                ],
                "steps": <count>
            },
            "dummy": {
                "path": [
                    <state1>,
                    <state2>,
                    [...]
                ],
                "steps": <count>
            }
        }
        [...]
    }
    """

    score = {"automata": 0, "dummy": 0}  # global score
    results = {}  # paths and steps of each automata

    for i in range(iterations):

        data = {
            "automata": {
                "path": [],
                "steps": 0
            },
            "dummy": {
                "path": [],
                "steps": 0
            }   
        }

        # control state for the automata (a) and the dummy (d)
        curr_state_a, curr_hour = generateRandomInput()
        curr_state_d = curr_state_a

        # save init states
        data["automata"]["path"].append(curr_state_a)

        time = 0  # passed time (1 unit represents 20s)

        # load data from MDP model
        with open(POLICIES_PATH, 'r') as file:
            policies = json.load(file)
        with open(PROBABILITIES_PATH, 'r') as file:
            probabilities = json.load(file)
        
        # main loop
        while (curr_state_a != "LLL") or (curr_state_d != "LLL"):
            
            # calculate next state for automata
            if curr_state_a != "LLL":
                action_a = automata_decide(curr_state_a, curr_hour, policies)  # decide action
                curr_state_a = nextState(curr_hour, curr_state_a, action_a, probabilities)  # update state
                data["automata"]["path"].append(curr_state_a)  # save state
                data["automata"]["steps"] += 1  # update count

            # calculate next state for dummy
            if curr_state_d != "LLL":
                action_d = dummy_decide(curr_state_d, curr_hour)
                curr_state_d = nextState(curr_hour, curr_state_d, action_d, probabilities)
                data["dummy"]["path"].append(curr_state_d)
                data["dummy"]["steps"] += 1

            # update time
            time += 1
            if time >= TIME_UNIT:
                time = 0
                curr_hour += 1
                if curr_hour >= HOURS:
                    curr_hour = 0
    
        # save iteration
        results[i] = data

        # results
        # print("Iteration:", i)
        if data["automata"]["steps"] < data["dummy"]["steps"]:  # automata wins
            score["automata"] += 1
            # print("Automata wins!:", data["automata"]["steps"], "vs", data["dummy"]["steps"])

        elif data["automata"]["steps"] > data["dummy"]["steps"]:  # dummy wins
            score["dummy"] += 1
            # print("Dummy wins!:", data["dummy"]["steps"], "vs", data["automata"]["steps"])

        # else:
        #     print("It's a tie, steps:", data["automata"]["steps"])

    # save to file
    with open(RESULTS_PATH, "w") as outfile:
        json.dump(results, outfile, indent=4, sort_keys=True)
    
    # print final score
    print("Global score: Automata", score["automata"], "-", score["dummy"], "Dummy")
    print("Automata efficiency over dummy:", ((score["automata"]/score["dummy"]) - 1) * 100, "\b%")


if __name__ == "__main__":
    runMDP()
    test()