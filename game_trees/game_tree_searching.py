from state import *
from utils import *
from math import inf

class GameTreeSearching:
  # You will also find that the GameStateHandler class (already imported) will help perform needed operations on the
  # the game states. To declare a GameStateHandler simply wrap it around a GameState like such,
  # handler = GameStateHandler(GameState) where GameState will be an instance of GameState.
  
  # Below is a list of helpful functions:
  # GameStateHandler.get_successors() --> returns successors of the handled state
  # GameStateHandler.get_agents() --> returns a list of the positions of the agents on the map
  # GameStateHandler.get_agent_count() --> returns the number of agents on the map
  # GameStateHandler.get_agent_actions(agent_pos) --> returns a list of the possible actions the given agent can take
  # GameStateHandler.get_successor(agent_pos, action) --> returns the successor state if the given agent took the given action 
  # GameState.get_player_position() --> returns the players position in that game state as (row, col)
  # GameState.copy() --> returns a copy
  # GameState.is_win() --> returns True if the game state is a winning state
  # GameState.is_loss() --> returns True if the game state is a losing state

  # Hint:
  # To avoid unwanted issues with recursion and state manipulation you should work with a _copy_ of the state
  # instead of the original.
  #
  # Terminal: win/loss
  # actions: get_agent_actions(agent_pos)
  # agent_pos : get_player_pos()/ get_agents()
  # utility : eval_fn(state)
  # result(pos, action)->state  : get_successor(agent_pos, action)
  # get_successor(agent_pos, action) rets 
  # How do we know if a player is min or max? Alternating
  # MIN: player or MAX: enemies
  # get_agents() returns [player_pos, enemy1_pos, ..., enemyN_pos]
  # get_agent_count includes player + enemies
  # 
  # Keep track of which agent's moves the algo is looking at
  # depth is number of player moves - bound


  @staticmethod
  def minimax_search(state, eval_fn, depth = 2):
    # Question 1, your minimax search solution goes here
    copy_state = state.copy()
    value, best_move =  GameTreeSearching.minimax_helper(copy_state, eval_fn, depth, True)
    return best_move

  @staticmethod
  def minimax_helper(state, eval_fn, depth, player_turn):
    best_move = None

    #Terminal state check
    if depth == 0 or state.is_win() or state.is_loss():
      return eval_fn(state), best_move
    
    stateHandler = GameStateHandler(state)
    agent_lst = stateHandler.get_agents()
    # player is MAX player and enemies are MIN players

    #MIN player - enenmies
    value = inf
    agents = agent_lst[1:]
    if player_turn: #MAX player
      value = -inf
      agents = [agent_lst[0]]
    
    for agent in agents:
      actions = stateHandler.get_agent_actions(agent)
      for move in actions:
        nxt_pos = stateHandler.get_successor(agent, move)
        if player_turn:
          new_depth = depth
        else:
          new_depth = depth-1
        nxt_val, nxt_move = GameTreeSearching.minimax_helper(nxt_pos, eval_fn, new_depth, not player_turn)
        if player_turn and value < nxt_val:
          value, best_move = nxt_val, move
        if (not player_turn) and value > nxt_val:
          value, best_move = nxt_val, move
    return value, best_move

  @staticmethod
  def alpha_beta_search(state, eval_fn, depth):
    # Question 2, your alpha beta pruning search solution goes here
    copy_state = state.copy()
    value, best_move =  GameTreeSearching.alpha_beta(copy_state, eval_fn, depth, True, -inf, inf)
    return best_move
  
  @staticmethod
  def alpha_beta(state, eval_fn, depth, player_turn, alpha, beta):
    best_move = None

    #Terminal state check
    if depth == 0 or state.is_win() or state.is_loss():
      return eval_fn(state), best_move
    
    stateHandler = GameStateHandler(state)
    agent_lst = stateHandler.get_agents()
    # player is MAX player and enemies are MIN players

    #MIN player - enenmies
    value = inf
    agents = agent_lst[1:]
    if player_turn: #MAX player
      value = -inf
      agents = [agent_lst[0]]
    
    for agent in agents:
      actions = stateHandler.get_agent_actions(agent)
      for move in actions:
        nxt_pos = stateHandler.get_successor(agent, move)
        if player_turn:
          new_depth = depth
        else:
          new_depth = depth-1
        nxt_val, nxt_move = GameTreeSearching.alpha_beta(nxt_pos, eval_fn, new_depth, not player_turn, alpha, beta)
        if player_turn:
          if value < nxt_val:
            value, best_move = nxt_val, move
          if value >= beta:
            return value, best_move
          alpha = max(alpha, value)
        if not player_turn:
          if value > nxt_val:
            value, best_move = nxt_val, move
          if value <= alpha:
            return value, best_move
          beta = min(beta, value)
    return value, best_move

  @staticmethod
  def expectimax_search(state, eval_fn, depth):
    # Question 3, your expectimax search solution goes here
    copy_state = state.copy()
    value, best_move =  GameTreeSearching.alpha_beta(copy_state, eval_fn, depth, True, -inf, inf)
    return best_move
  
  @staticmethod
  def expectimax_helper(state, eval_fn, depth, player_turn):
    best_move = None

    #Terminal state check
    if depth == 0 or state.is_win() or state.is_loss():
      return eval_fn(state), best_move
    
    stateHandler = GameStateHandler(state)
    agent_lst = stateHandler.get_agents()
    # player is MAX player and enemies are MIN players

    #MIN player - enenmies
    value = 0
    agents = agent_lst[1:]
    if player_turn: #MAX player
      value = -inf
      agents = [agent_lst[0]]
    
    for agent in agents:
      actions = stateHandler.get_agent_actions(agent)
      for move in actions:
        nxt_pos = stateHandler.get_successor(agent, move)
        if player_turn:
          new_depth = depth
        else:
          new_depth = depth-1
        nxt_val, nxt_move = GameTreeSearching.expectimax_helper(nxt_pos, eval_fn, new_depth, not player_turn)
        if player_turn and value < nxt_val:
          value, best_move = nxt_val, move
        if not player_turn:
          value += (1 / len(actions)) * nxt_val
    return value, best_move
