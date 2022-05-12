# test if our solution is optimum

from model import *
from automata import decide as automata_decide
from automata import generateRandomInput

import random
import json


RESULTS_PATH = "output/test_results.json"


def dummy_decide(state: str, hour: int):
    # unoptimized dummy automata, just output a random action
    return STATES[random.randint(0, 2)]


def test(iterations: int = 5):
    """
    Simulate the real world problem using the data, and evaluate the time it takes to
    reach the final state, LLL, comparing the automata to a dummy.
    First, generate a random input state and hour, wait for the actions from the machines,
    and use the probabilities generated from the MDP to generate the next state.
    We count the number of actions taken, and obtain the results of the iterations,
    saving them to RESULTS_PATH, with the format:
    {
        <iteration1>: {
            <automata>: {
                <path>: [
                    <state1>,
                    <state2>,
                    [...]
                ],
                <steps>: <count>
            },
            <dummy>: {
                <path>: [
                    <state1>,
                    <state2>,
                    [...]
                ],
                <steps>: <count>
            }
        }
        [...]
    }
    """

    results = {}
    for i in range(iterations):
        # control state for the automata (a) and the dummy (d)
        curr_state_a, curr_hour_a = generateRandomInput()
        curr_state_d, curr_hour_d = generateRandomInput()
        
        # main loop
        while curr_state_a != "LLL" and curr_state_d != "LLL":
            if curr_state_a != "LLL":
                pass


    # save to file
    with open(RESULTS_PATH, "w") as outfile:
        json.dump(results, outfile, indent=4, sort_keys=True)


if __name__ == "__main__":
    test()