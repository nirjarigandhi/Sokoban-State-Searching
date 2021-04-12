from state import *
from utils import *

# For the Below implementations we have already imported a Stack class, a Queue class and a PriorityQueue class
# to help you complete the algorithms. PLEASE DO NOT ADD OR REMOVE ANY IMPORTS.

# You will also find that the GameStateHandler class (already imported) will help perform needed operations on the
# the game states. To declare a GameStateHandler simply wrap it around a GameState like such,
# handler = GameStateHandler(GameState) where GameState will be an instance of GameState.

# Below is a list of helpful functions:
# GameStateHandler.get_successors() --> returns successors of the handled state
# GameState.get_player_position() --> returns the players position in that game state as (row, col)

class SearchAlgorithms:

  @staticmethod
  def depth_first_search(goal_fn, start_state):
    frontier = Stack()
    explored = set()
    frontier.push([start_state])
    while not frontier.empty():
        n = frontier.pop()
        curr_state = n[-1]
        goal_reached = goal_fn(curr_state)
        if goal_reached:
           return n[:-1]
        explored.add(curr_state)
        state_handler = GameStateHandler(curr_state)
        successors = state_handler.get_successors()
        for succ in successors:
          if (succ[1] not in explored):
            n[-1] = succ[0]
            temp = n.copy()
            temp.append(succ[1])
            frontier.push(temp)
    return []
    #raise NotImplementedError("Depth First Search not implemented")
  
  @staticmethod
  def breadth_first_search(goal_fn, start_state):
    frontier = Queue()
    explored = set()
    frontier.push([start_state])
    while not frontier.empty():
        n = frontier.pop()
        curr_state = n[-1]
        goal_reached = goal_fn(curr_state)
        if goal_reached:
           return n[:-1]
        explored.add(curr_state)
        state_handler = GameStateHandler(curr_state)
        successors = state_handler.get_successors()
        for succ in successors:
          if (succ[1] not in explored):
            n[-1] = succ[0]
            temp = n.copy()
            temp.append(succ[1])
            frontier.push(temp)
    return []
    #raise NotImplementedError("Breadth First Search not implemented")
  
  @staticmethod
  def uniform_cost_search(goal_fn, start_state, cost_fn = lambda pos : 1):
    frontier = PriorityQueue()
    explored = {}
    frontier.push([start_state], 0)
    curr_cost = 0
    while not frontier.isEmpty():
        n = frontier.pop()
        curr_state = n[-1]
        curr_pos = curr_state.get_player_position()
        curr_cost = cost_fn(curr_pos)
        goal_reached = goal_fn(curr_state)
        if goal_reached:
           return n[:-1]
        explored[curr_state] = curr_cost
        state_handler = GameStateHandler(curr_state)
        successors = state_handler.get_successors()
        for tup in successors:
          succ = tup[1]
          pos = succ.get_player_position()
          cost = cost_fn(pos)
          if succ not in explored or cost < explored[succ]:
            explored[succ] = cost
            n[-1] = tup[0]
            temp = n.copy()
            temp.append(succ)
            frontier.update(temp, cost)
    return []
    #raise NotImplementedError("Uniform Cost Search not implemented")
  
  @staticmethod
  def a_star_search(goal_fn, start_state, cost_fn = lambda pos : 1, heuristic = lambda state: 0):
    frontier = PriorityQueue()
    explored = {}
    frontier.push([start_state], 0)
    curr_cost = 0
    while not frontier.isEmpty():
        n = frontier.pop()
        curr_state = n[-1]
        curr_pos = curr_state.get_player_position()
        curr_cost = cost_fn(curr_pos)
        goal_reached = goal_fn(curr_state)
        if goal_reached:
           return n[:-1]
        explored[curr_state] = curr_cost
        state_handler = GameStateHandler(curr_state)
        successors = state_handler.get_successors()
        for tup in successors:
          succ = tup[1]
          pos = succ.get_player_position()
          cost = cost_fn(pos)
          if succ not in explored or cost < explored[succ]:
            explored[succ] = cost
            n[-1] = tup[0]
            temp = n.copy()
            temp.append(succ)
            h = heuristic(succ)
            frontier.update(temp, cost+h)
    return []
    #raise NotImplementedError("A Star Search not implemented")
 
