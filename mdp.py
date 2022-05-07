import csv
import json

# Parameters
ITERATIONS = 69
COST = 1

# Paths
CSV_PATH = "./data.csv"
"""
The format of the CSV file is:
Initial traffic level N;Initial traffic level E;Initial traffic level W;Green traffic light;Final traffic level N;Final traffic level E;Final traffic level W

"""
PROBABILITIES_PATH = "./output/probabilities.json"
VALUES_PATH = "./output/values.json"
POLICIES_PATH = "./output/policies.json"

# Model
# states are defined as <N traffic level><E traffic level><W traffic level>
STATES = ["HHH", "HHL", "HLL", "LLL", "LHH", "LLH", "LHL", "HLH"]
ACTIONS = ["N", "E", "W"]

TIME_UNIT = 180  # number of measures per unit of time


def infer():
    """
    Get probabilities for each action and each transition, for each day, using data from CSV_PATH,
    and save it as a JSON file to PROBABILITIES_PATH.
    The format of the JSON is:
    {
        <hour> : {
            <action>: {
                <state0>-><state1>: <probability>,
                [...]
            },
            [...]
        },
        [...]
    }
    """

    # TODO: take FUCKING TIME into account

    json_data = {}
    count = []  # to count the number of times an action has appeared
    for elem in ACTIONS:  # just to make it fit any model, put one 0 per action
        count.append(0)
    
    # For infering the probabilities of each action for each transition, we must count
    # the times that transition (with that action) happens in the data, and divide it by
    # all the times that action has appeared.

    # read file
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        next(reader, None)  # skip the headers

        for row in reader:
            # read row
            init_state = row[0][0] + row[1][0] + row[2][0]  # get first letter of each word to match (eg: HHL)
            action = row[3]
            final_state = row[4][0] + row[5][0] + row[6][0]

            if init_state not in STATES or final_state not in STATES or action not in ACTIONS:
                continue

            # initialize if it's new
            if action not in json_data:
                json_data[action] = {init_state + "->" + final_state : 0}
            elif init_state + "->" + final_state not in json_data[action]:
                json_data[action][init_state + "->" + final_state] = 0
            
            # update the count for that transition, within that action
            json_data[action][init_state + "->" + final_state] += 1

            # update the count for that action
            for i in range(len(ACTIONS)):
                if action == ACTIONS[i]:
                    count[i] += 1
    
    # now we finish calculating the probabilities
    for action in json_data:
        for transition in json_data[action]:

            for i in range(len(ACTIONS)):
                if action == ACTIONS[i]:
                    json_data[action][transition] /= count[i]

    # check probabilities are correct
    sum = {}
    for action in ACTIONS:  # initialize sum for each action
        sum[action] = 0
    for action in json_data:
        for transition in json_data[action]:

            for i in range(len(ACTIONS)):
                if action == ACTIONS[i]:
                    sum[action] += json_data[action][transition]
    print("Sum of probabilities for each action (should be close to 1):", sum)

    # save to file
    with open(PROBABILITIES_PATH, "w") as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)
             


def calculateValues():
    """
    Use Bellman's equations, value iteration, and the probabilities from PROBABILITIES_PATH to
    calculate the value of each action, and save it to VALUES_PATH.
    The format for the JSON is:
    {
        <hour> : {
            <state>: <cost>,
            [...]
        },
        [...]
    }
    """
    json_val = {}

    with open(PROBABILITIES_PATH, 'r') as probabilities:
        prob_json = json.load(probabilities)
        
    for hour in prob_json:
        json_val[hour] = {}
        for act in prob_json[hour]:
            for stat in prob_json[hour][act]:
                if stat[0:3] not in json_val[hour]:
                    json_val[hour][stat[0:3]] = 0

    for hour in json_val:
        for i in range(ITERATIONS):
            for stat in json_val[hour]:
                values=[COST,COST,COST]
                for act in ACTIONS:
                    for stat_p in prob_json[hour][act]:
                        if stat_p[0:3] == stat:
                            if act == "N":
                                val_n = prob_json[hour][act][stat_p] * json_val[hour][stat_p[5:]]
                                values[0] = values[0] + val_n
                            if act == "E":
                                val_n = prob_json[hour][act][stat_p] * json_val[hour][stat_p[5:]]
                                values[1] = values[1] + val_n
                            if act == "W":
                                val_n = prob_json[hour][act][stat_p] * json_val[hour][stat_p[5:]]
                                values[2] = values[2] + val_n

                json_val[hour][stat] = min(values)

    # save to file
    with open(VALUES_PATH, "w") as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)


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

    json_opt = {}

    with open(PROBABILITIES_PATH, 'r') as probabilities:
        prob_json = json.load(probabilities)

    with open(VALUES_PATH, 'r') as values:
        val_json = json.load(values)


    for hour in val_json:
        json_opt[hour] = {}
        for stat in val_json[hour]:
            json_opt[hour][stat] = 0

    for hour in json_opt:
        for stat in json_opt[hour]:
            values=[COST,COST,COST]
            for act in ACTIONS:
                for stat_p in prob_json[hour][act]:
                    if stat_p[0:3] == stat:
                        if act == "N":
                            val_n = prob_json[hour][act][stat_p] * json_val[hour][stat_p[5:]]
                            values[0] = values[0] + val_n
                        if act == "E":
                            val_n = prob_json[hour][act][stat_p] * json_val[hour][stat_p[5:]]
                            values[1] = values[1] + val_n
                        if act == "W":
                            val_n = prob_json[hour][act][stat_p] * json_val[hour][stat_p[5:]]
                            values[2] = values[2] + val_n

            json_opt[hour][stat] = ACTIONS[values.index(min(values))]

    # save to file
    with open(POLICIES_PATH, "w") as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)


    pass


if __name__ == "__main__":
    infer()
    calculateValues()
    optimalPolicies()