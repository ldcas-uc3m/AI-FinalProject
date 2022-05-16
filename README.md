# Artificial Intelligence: Final Practice
By Luis Daniel Casais Mezquida & Alberto Díaz-Pacheco Corrales, grp. 89  
Artificial Intelligence 21/22, Bachelor's Degree in Computer Science and Engineering  
Universidad Carlos III de Madrid

## Problem statement
A traffic intersection can be approached by vehicles from the North, from the East and from the West.
![Scheme](/img/scheme_1.png)

The flow of vehicles in each direction encounters a traffic light before reaching the intersection, which can be either green or red. An operator must select every 20 seconds which of the three traffic lights to turn green: the other two will automatically turn red.  
Sensors measure the level of traffic in each direction prior to the intersection. The values can be: High or Low. When the traffic light in one direction is green, the level will normally stay the same or go down, only very occasionally increasing. When the traffic light is closed, the level stays the same or rises.  
We want to design an automaton that opens the appropriate traffic light at each cycle following the optimal policy of the corresponding MDP. The target situation is that traffic in all three directions is Low. In such a situation, the automaton stops working.  
The main objective of the project is to obtain the optimal policy for the automaton.

## Input data
Historical data is available for situations where we know:
- The traffic levels at the start of the 20-second cycle
- The traffic light that remained green during that period
- The traffic levels at the end of the cycle

The historical data are in a file. Each line contains 7 values separated by ";". The first three are the traffic levels at the beginning of the 20 seconds in the order North, East, West, the fourth is the traffic light that stays green during those 20 seconds and the last three are the traffic levels at the end.  
For example, the line:
```
High;High;Low;E;High;High;High
```
indicates that we had High traffic coming in from the North and East and Low traffic from the West, the traffic light controlling incoming traffic from the East was green and within 20 seconds traffic was High in all three directions.

## Implementation
To solve this problem, we designed an automata that, given the current state of the traffic, in format `<North-traffic><East-traffic><West-traffic>` (eg, `HHL`), and the hour of the day (`0`-`23`), outputs the optimal action, that is, what traffic light to turn green (`N` for North, `E` for East and `W` for West).  
The decisions made by the automata are based on the optimal policies for each hour and state calculated by a Markov Decision Process given the original data sample (`Data.csv`).  
   
For the implementation of the solution of the problem, we developed three Python3 scripts: `model.py`, `mdp.py` and `automata.py`, plus a testing script, `test.py`.

**IMPORTANT NOTE**: This implementation requires **Python 3.6 or higher** (as we need the `random.choices()` function for `nextState()` in `test.py`)

### `model.py`
This script contains the constant variables used by the rest of the scripts, and models the MDP, the input data, the parameters, and the paths for the saved data.   
   
The MPD contains 8 states (all possible combinations of traffic), and three actions (turn each traffic light green), and the goal state is `LLL`. 
It also models the input data which, as by the statement, represents with one line the span of 20s, therefore 180 lines represent one hour, therefore there are 180 measurements (data points) in an hour.  

### `mdp.py`
This scripts contains an implementation for this specific MDP. Although we tried to make it as flexible and scalable as possible, the format of the data conditions the implementation.  
  
The script infers the probabilities for each hour, action and transition from `Data.csv` and saves them to `output/probabilities.json`, then calculates the value of each state, for each hour, using Bellman's Equations and Value Iteration and saves them to `output/values.json`, to finally calculate the optimal policies for each hour and state and save them to `output/policies.json`.  
  
We decided to save the data from each step of the MDP, even though only `output/policies.json` is needed, to aid on debugging and also provide a better insight on the data.

### `automata.py`
This contains the implementation of the automata. We also included a couple of functions to generate random data (`generateRandomInput()`) and run the automata (`runAutomata()`), to provide an example of its use.  
  
The real automata is the `decide()` function, which reads the optimal policies from the MDP and applies them to the input. In the case of reaching the goal state (`LLL`), it just cycles through the actions.

### `test.py`
This script was developed in order to test the automata, for that we generate an initial random input, ask both the automata and a dummy automata that generates random actions for an action, and choose the next state, taking that action into account, and using the infered probabilities to randomly (but with weigts) generate the next action.  
The automata with the least steps wins, and we do some iterations to find which one is better.  
  
Unfortunately, and we don't know why, this tests says that the dummy is 50-60% better than our automata, so we applied the Ostrich Algorihtm (that is, to stick one's head in the sand and pretend there is no problem) and created the [ostrich branch](https://github.com/ldcas-uc3m/AI-FinalProject/tree/ostrich).