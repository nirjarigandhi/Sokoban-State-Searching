from state import GameState
from state_searching import Heuristics
from state_searching import SearchAlgorithms
from state_searching import SearchProblems
from grade_helpers import load_test, verify, pseudo_simulate

COST_FUNCTIONS = [lambda pos : 0.2 ** pos[0], lambda pos : pos[0] * 2, lambda pos : pos[1] * 2]

def test(tests, tester):
  total_marks, earned_marks = 0, 0

  for test in tests:
    name, map_file, goal_func, solution = load_test(test)

    total_marks += 1

    try:
      # Run the test
      state = GameState(map_file)
      result = tester(goal_func, state, solution)
      earned = int(result)
      print("Testing: {}\t [{}/{}]".format(name, earned, 1))

      earned_marks += earned

    except NotImplementedError as e:
      print("Testing {}\t [{}]\t [0/1]".format(name, e))

  return earned_marks, total_marks

if __name__ == "__main__":
  total_marks, earned_marks = 0, 0

  print("------ Question 1 ------")
  e, t = test(["dfs/basic_1b", "dfs/basic_b", "dfs/basic_p"], lambda goal, state, solution : verify(SearchAlgorithms.depth_first_search(goal, state), solution))
  total_marks += t
  earned_marks += e

  print("\n------ Question 2 ------")
  e, t = test(["bfs/basic_1b", "bfs/basic_b", "bfs/basic_p"], lambda goal, state, solution : verify(SearchAlgorithms.breadth_first_search(goal, state), solution))
  total_marks += t
  earned_marks += e

  print("\n------ Question 3 ------")
  for i in range(len(COST_FUNCTIONS)):
    e, t = test(["ucs/multiple_paths_with_func{}".format(i + 1)],
                lambda goal, state, solution : verify(SearchAlgorithms.uniform_cost_search(goal, state, cost_fn = COST_FUNCTIONS[i]), solution))
    total_marks += t
    earned_marks += e

  print("\n------ Question 4 ------")
  # Running A Star with null heuristic is the same as running UCS so can reuse tests
  for i in range(len(COST_FUNCTIONS)):
    e, t = test(["ucs/multiple_paths_with_func{}".format(i + 1)],
                lambda goal, state, solution : verify(SearchAlgorithms.a_star_search(goal, state, cost_fn = COST_FUNCTIONS[i]), solution))
    total_marks += t
    earned_marks += e

  print("\n------ Question 5 ------")
  e, t = test(["astar/two_switches_1", "astar/two_switches_2"],
              lambda goal, state, solution :
              pseudo_simulate(SearchAlgorithms.a_star_search(goal, state, heuristic=Heuristics.two_boxes_heuristic), solution, state, goal))
  total_marks += t
  earned_marks += e

  print("\n------ Question 6 ------")
  e, t = test(["astar/no_boxes_1", "astar/no_boxes_2", "astar/no_boxes_3"],
              lambda goal, state, solution :
              pseudo_simulate(SearchAlgorithms.a_star_search(goal, state, heuristic=Heuristics.points_only_heuristic), solution, state, goal))
  total_marks += t
  earned_marks += e

  print("\n\nTotal Grade: {}/{}".format(earned_marks, total_marks))
