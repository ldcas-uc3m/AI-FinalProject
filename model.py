# constant variables for the model of the MDP

# Parameters
ITERATIONS = 69
COST = 1

# Paths
CSV_PATH = "./Data.csv"
"""
The format of the CSV file is:
Initial traffic level N;Initial traffic level E;Initial traffic level W;Green traffic light;Final traffic level N;Final traffic level E;Final traffic level W

"""
PROBABILITIES_PATH = "./output/probabilities.json"
VALUES_PATH = "./output/values.json"
POLICIES_PATH = "./output/policies.json"

# Model
# states are defined as <N traffic level><E traffic level><W traffic level>
STATES = ("HHH", "HHL", "HLL", "LLL", "LHH", "LLH", "LHL", "HLH")
ACTIONS = ("N", "E", "W")

TIME_UNIT = 180  # number of measures per unit of time
HOURS = 24  # number of units of time