import csv
import os
import json

# Parameters
ITERATIONS = 69
COST = 1

# Paths
CSV_PATH = "./Data.csv"
PROBABILITIES_PATH = "./probabilities.json"
VALUES_PATH = "./values.json"
POLICIES_PATH = "policies.json"

# Model
states = ["HHH", "HHL", "HLL", "LLL", "LHH", "LLH", "LHL", "HLH"]
actions = ["N", "W", "E"]


def infer():
    """
    Get probabilities for each action and each transition, using data from CSV_PATH,
    and save it as a JSON file to PROBABILITIES_PATH.
    The format of the JSON is:
    {
        <action>: {
            <state0>.<state1>: <probability>,
            [...]
        },
        [...]
    }
    """
    pass


def calculateValues():
    """
    Use Bellman's equations, value iteration, and the probabilities from PROBABILITIES_PATH to
    calculate the value of each action, and save it to VALUES_PATH.
    The format for the JSON is:
    {
        <action>: <cost>,
        [...]
    }
    """
    pass


def optimalPolicies():
    """
    Using the values from VALUES_PATH, calculate the optimal policy for each state,
    and save it to POLICIES_PATH.
    The format for the JSON is:
    {
        <state>: <action>,
        [...]
    }
    """
    pass


if __name__ == "__main__":
    infer()
    calculateValues()
    optimalPolicies()