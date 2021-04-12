from state import *

class Heuristics:

  # We have included above two common heuristics, manhattan distance and euclidean distance so feel free to use
  # either if needed.
  #
  # Helpful functions:
  # GameState.get_boxes() --> returns a list of (row, col) positions representing where the boxes are on the map
  # GameState.get_switches() --> returns a dictionary where the keys are the locations of the switches as (row, col) and the value
  #                              being True if the switch is on and False if off.
  # GameState.get_player_position() --> returns the current position of the player in the form (row, col)
  # GameState.get_remaining_points() --> returns a list of the positions of the remaining armory points of the map in the form (row, col) 
  
  @staticmethod
  def manhattan_heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

  @staticmethod
  def euclidean_heuristic(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
 
  @staticmethod
  def two_boxes_heuristic(state):
    box1, box2 = state.get_boxes()
    switches = state.get_switches()
    pos = state.get_player_position()

    keys = []
    for key in switches:
      keys.append(key)
    
    key1, key2 = keys[0], keys[1]

    if switches[key1] and switches[key2]:
      return 0
    
    d_box1 = abs(box1[0] - pos[0]) + abs(box1[1] - pos[1])
    d_box2 = abs(box2[0] - pos[0]) + abs(box2[1] - pos[1])

    h = 0
    if switches[key1] or switches[key2]:
      if key1 == box1: #box1 is on switch1, only need distance from switch2 to box2
        h += d_box2
        h += abs(box2[0] - key2[0]) + abs(box2[1] - key2[1])
      elif key1 == box2: #box2 is on switch1, only need distance from switch2 to box1
        h += d_box1
        h += abs(box1[0] - key2[0]) + abs(box1[1] - key2[1])
      elif key2 == box1:
        h += d_box2
        h += abs(box2[0] - key1[0]) + abs(box2[1] - key1[1])
      else:
        h += d_box1
        h += abs(box1[0] - key1[0]) + abs(box1[1] - key1[1])
    
    else:

      if d_box1 < d_box2:
        h = d_box1
        closest_b = box1
        furthest_b = box2
      else:
        h = d_box2
        closest_b = box2
        furthest_b = box1
      
      d_switch1 = abs(closest_b[0] - key1[0]) + abs(closest_b[1] - key1[1])
      d_switch2 = abs(closest_b[0] - key2[0]) + abs(closest_b[1] - key2[1])

    
      if d_switch1 <= d_switch2:
        h += d_switch1
        closest_s =  key1
        furthest_s = key2
      else:
        h += d_switch2
        closest_s =  key2
        furthest_s = key1
      
      # to other box
      h += abs(closest_s[0] - furthest_b[0]) + abs(closest_s[1] - furthest_b[1])
      h += abs(furthest_s[0] - furthest_b[0]) + abs(furthest_s[1] - furthest_b[1])
    
    return h

  @staticmethod
  def points_only_heuristic(state):
    # Question 6, your solution for the points only heuristic will go here.
    # Return a heuristic value (an integer) representing the heuristic cost of the given state.
    switches = state.get_switches()
    pos = state.get_player_position()

    for k in switches:
      key = k
      if switches[key]:
        return 0
    
    if state.player_has_boots():
        return abs(key[0] - pos[0]) + abs(key[1] - pos[1])
    
    armories = state.get_remaining_points()
    need = 5 - state.get_obtained_points()
    h = 0
    for i in range(need):
      m = -1
      for armory in armories:
        dis = abs(armory[0] - pos[0]) + abs(armory[1] - pos[1])
        if dis < m or m < 0:
          m = dis
          temp = armory
      h += m
      pos = temp
      
    return h + abs(key[0] - pos[0]) + abs(key[1] - pos[1])
