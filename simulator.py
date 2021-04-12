from utils import GFrame
from sokoban import *
from utils import *
from time import sleep
from threading import Thread

class Simulator():

  def __init__(self, map="sim_test", wait_time=1):
    self._map = map
    self._wait_time = wait_time
    
  def _setup(self):
    self._frame = GFrame("Sokoban Simulator")
    self._game = Sokoban(30, self._map, True)
    self._frame.display(self._game)

  def swap_map(self, map):
    self._map = map

  def swap_wait_time(self, wait_time):
    self._wait_time = wait_time

  def _simulate(self, actions):
    print("#------------STARTING SIMULATION------------#")

    # Simulate the given actions every "speed" seconds
    for action in actions:
      sleep(self._wait_time)
      print("Move: ", action)
      self._game.move_enemies()
      self._game.move_player(action)

    print("#------------SIMULATION FINISHED------------#")

    self._game.set_done(True)

  def _simulate_agent(self, agent):
    print("#------------STARTING SIMULATION------------#")

    # Simulate the given actions every "speed" seconds
    while self._game.get_state().get_mouse_locations():
      sleep(self._wait_time)
      action = agent.request_action(self._game.get_state())
      print("Move: ", action)
      self._game.move_player(action)
      self._game.move_enemies()
      
    self._game.set_done(True)

    print("#------------SIMULATION FINISHED------------#")

  def _simulate_listening_agent(self, agent):
    print("#------------STARTING SIMULATION------------#")

    # Simulate the given actions every "speed" seconds
    while self._game.get_state().get_mouse_locations():
      sleep(self._wait_time)
      agent.listen(self._game.get_state())
      action = agent.request_action(self._game.get_state())
      print("Move: ", action)
      self._game.move_player(action)
      self._game.move_enemies()

    self._game.set_done(True)
      
    print("#------------SIMULATION FINISHED------------#")

  def _simulate_prediction_agent(self, agent):
    print("#------------STARTING SIMULATION------------#")

    # Simulate the given actions every "speed" seconds
    remaining_mice = self._game.get_state().get_mouse_locations()

    while remaining_mice:
      sleep(self._wait_time)
      agent.predict(self._game.get_state())
      action = agent.request_action(self._game.get_state())
      print("Move: ", action)
      self._game.move_player(action)
      self._game.move_enemies()
      
    print("#------------SIMULATION FINISHED------------#")

    self._game.set_done(True)
    
  def simulate(self, actions):
    self._setup()
    
    # Setup the simulation in its own thread
    simulation_thread = Thread(target=self._simulate, args = (actions, ), daemon=True)
    simulation_thread.start()
    
    # Run the game and frame
    self._frame.run()

  def simulate_agent(self, agent):
    self._setup()
    
    # Setup the simulation in its own thread
    simulation_thread = Thread(target=self._simulate_agent, args = (agent, ), daemon=True)
    simulation_thread.start()
    
    # Run the game and frame
    self._frame.run()

  def simulate_generic(self, agent):
    self._setup()

    # Setup the simulation in its own thread
    simulation_thread = Thread(target=self._simulate_agent, args = (agent, ), daemon=True)
    simulation_thread.start()
    
    # Run the game and frame
    self._frame.run()

  def simulate_listening_agent(self, agent):
    self._setup()
    
    # Setup the simulation in its own thread
    simulation_thread = Thread(target=self._simulate_listening_agent, args = (agent, ), daemon=True)
    simulation_thread.start()
    
    # Run the game and frame
    self._frame.run()

  def simulate_prediction_agent(self, agent):
    self._setup()
    
    # Setup the simulation in its own thread
    simulation_thread = Thread(target=self._simulate_prediction_agent, args = (agent, ), daemon=True)
    simulation_thread.start()
    
    # Run the game and frame
    self._frame.run()
