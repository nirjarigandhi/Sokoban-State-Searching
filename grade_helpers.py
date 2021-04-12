from utils import Direction
from state import *
from state_searching import SearchProblems
from json import load

def pseudo_simulate(actions, threshold, state, goal):

  current = state.copy()
  
  for action in actions:
    handler = GameStateHandler(current)
    current = handler.get_successor(current.get_player_position(), action)
    
  return goal(current) and current.get_score() >= threshold

def direction_to_string(direction):
  if direction == Direction.STOP:
    return "stop"

  elif direction == Direction.NORTH:
    return "north"

  elif direction == Direction.SOUTH:
    return "south"

  elif direction == Direction.WEST:
    return "west"

  elif direction == Direction.EAST:
    return "east"

def convert_goal(goal):
  if goal == "switches":
    return SearchProblems.all_switches

  elif goal == "points":
    return SearchProblems.all_points

  elif goal == "no_boxes":
    return SearchProblems.no_boxes

def convert_answer(answer):
  return [direction_to_string(direction) for direction in answer]

def verify(answer, solution):
  return convert_answer(answer) == solution

def load_test(test_name):
  with open("assets/tests/{}.json".format(test_name), "r") as f:
    test = load(f)
    
  return test["test_name"], test["map"], convert_goal(test["goal"]), test["solution"]
