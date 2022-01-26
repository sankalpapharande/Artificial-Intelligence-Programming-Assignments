from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource

max_search_depth = 0
nodes_expanded = 0


## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n * n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3 * i: 3 * (i + 1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        input_configuration = self.config.copy()
        current_blank_index = input_configuration.index(0)
        if current_blank_index - self.n >= 0:
            input_configuration = self.config.copy()
            current_blank_index = input_configuration.index(0)
            new_blank_index = current_blank_index - self.n
            index_to_be_swapped = input_configuration[new_blank_index]
            input_configuration[new_blank_index] = 0
            input_configuration[current_blank_index] = index_to_be_swapped
            return PuzzleState(input_configuration, self.n, parent=self, cost=self.cost + 1, action='Up')
        else:
            return None

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        input_configuration = self.config.copy()
        current_blank_index = input_configuration.index(0)
        if current_blank_index + self.n < self.n * self.n:
            input_configuration = self.config.copy()
            current_blank_index = input_configuration.index(0)
            new_blank_index = current_blank_index + self.n
            index_to_be_swapped = input_configuration[new_blank_index]
            input_configuration[new_blank_index] = 0
            input_configuration[current_blank_index] = index_to_be_swapped
            return PuzzleState(input_configuration, self.n, parent=self, cost=self.cost + 1, action='Down')
        else:
            return None

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        input_configuration = self.config.copy()
        current_blank_index = input_configuration.index(0)
        if current_blank_index % 3 != 0:
            input_configuration = self.config.copy()
            current_blank_index = input_configuration.index(0)
            new_blank_index = current_blank_index - 1
            index_to_be_swapped = input_configuration[new_blank_index]
            input_configuration[new_blank_index] = 0
            input_configuration[current_blank_index] = index_to_be_swapped
            return PuzzleState(input_configuration, self.n, parent=self, cost=self.cost + 1, action='Left')
        else:
            return None

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        input_configuration = self.config.copy()
        current_blank_index = input_configuration.index(0)
        if (current_blank_index + 1) % 3 != 0:
            new_blank_index = current_blank_index + 1
            index_to_be_swapped = input_configuration[new_blank_index]

            input_configuration[new_blank_index] = 0
            input_configuration[current_blank_index] = index_to_be_swapped
            return PuzzleState(input_configuration, self.n, parent=self, cost=self.cost + 1, action='Right')
        else:
            return None

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
# def writeOutput(nodes_explored_till_now):
def writeOutput(state):
    ### Student Code Goes here
    global max_search_depth
    global nodes_expanded
    path_to_goal = []
    current_node = state
    f = open("output.txt", "w")

    while current_node.parent is not None:
        path_to_goal.append(current_node.action)
        current_node = current_node.parent

    cost_of_path = calculate_total_cost(state)
    f.write("path_to_goal:{}\n".format(list(reversed(path_to_goal))))
    f.write("cost_of_path:{}\n".format(cost_of_path))
    f.write("nodes_expanded: {}\n".format(nodes_expanded))
    f.write("search_depth:{}\n".format(state.cost))
    f.write("max_search_depth: {}\n".format(max_search_depth))
    f.close()

    return


def bfs_search(initial_state):
    """BFS search"""

    global max_search_depth
    global nodes_expanded

    frontier_queue = Q.Queue(maxsize=0)
    frontier_queue.put(initial_state)
    frontier = {str(initial_state)}
    nodes_explored_till_now = set()

    while frontier_queue.empty() is False:
        current_state = frontier_queue.get()
        nodes_explored_till_now.add(str(current_state.config))
        if test_goal(current_state):
            writeOutput(current_state)
            return current_state
        current_state_neighbours = current_state.expand()
        nodes_expanded += 1
        for neighbour in current_state_neighbours:
            if str(neighbour.config) not in nodes_explored_till_now and str(neighbour.config) not in frontier:
                frontier_queue.put(neighbour)
                nodes_explored_till_now.add(str(neighbour.config))
                frontier.add(str(neighbour.config))
                max_search_depth = max(max_search_depth, neighbour.cost)
    return False


def dfs_search(initial_state):
    """DFS search"""
    global max_search_depth
    global nodes_expanded

    frontier_stack = Q.LifoQueue(maxsize=0)
    frontier_stack.put(initial_state)
    frontier = {str(initial_state.config)}
    nodes_explored_till_now = set()

    while frontier_stack.empty() is False:
        current_state = frontier_stack.get()
        nodes_explored_till_now.add(str(current_state.config))
        if test_goal(current_state):
            writeOutput(current_state)
            return current_state

        current_state_neighbours = list(reversed(current_state.expand()))
        nodes_expanded += 1

        for neighbour in current_state_neighbours:
            if str(neighbour.config) not in nodes_explored_till_now and str(neighbour.config) not in frontier:
                frontier_stack.put(neighbour)
                frontier.add(str(neighbour.config))
                nodes_explored_till_now.add(str(neighbour.config))
                max_search_depth = max(max_search_depth, neighbour.cost)

    return False


def A_star_search(initial_state):
    """A * search"""
    global max_search_depth
    global nodes_expanded

    frontier_heap = Q.PriorityQueue()
    initial_state_config = str(initial_state.config)
    key = manhattan_heuristic(initial_state) + int(initial_state.cost)
    value = initial_state
    heap_sequence = 0
    frontier_heap.put((key,  heap_sequence, initial_state_config, value))
    heap_sequence += 1
    frontier = {str(initial_state.config)}
    cost_records = {initial_state_config: key}
    nodes_explored_till_now = set()

    while frontier_heap.empty() is False:
        current_state = frontier_heap.get()[3]
        nodes_explored_till_now.add(str(current_state.config))

        if test_goal(current_state):
            writeOutput(current_state)
            return current_state
        current_state_neighbours = current_state.expand()
        nodes_expanded += 1

        for neighbour in current_state_neighbours:
            neighbour_cost = manhattan_heuristic(neighbour) + int(neighbour.cost)
            if str(neighbour.config) not in nodes_explored_till_now and str(neighbour.config) not in frontier:
                frontier_heap.put((neighbour_cost, heap_sequence,  str(neighbour.config), neighbour))
                heap_sequence += 1
                cost_records[str(neighbour.config)] = neighbour_cost
                frontier.add(str(neighbour.config))
                nodes_explored_till_now.add(str(neighbour.config))
                max_search_depth = max(max_search_depth, neighbour.cost)

            elif str(neighbour.config) in nodes_explored_till_now and str(neighbour.config) in frontier:
                latest_cost = neighbour_cost
                key_in_priority_key = cost_records[str(neighbour.config)]
                if latest_cost < key_in_priority_key:
                    cost_records[str(neighbour.config)] = latest_cost
                    frontier_heap.put((latest_cost, heap_sequence, str(neighbour.config), neighbour))
                    heap_sequence += 1

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    cost_of_path = 0
    current_node = state
    while current_node.parent is not None:
        cost_of_path = cost_of_path + 1
        current_node = current_node.parent

    return cost_of_path


def manhattan_heuristic(state):
    estimated_cost = 0
    board_size = int(math.sqrt(len(state.config)))
    for i in range(1, len(state.config)):
        estimated_cost += calculate_manhattan_dist(i, state.config[i], board_size)
    return estimated_cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    index_of_value_in_goal_state = GOAL_STATE.index(value)

    x_goal = index_of_value_in_goal_state % n
    y_goal = index_of_value_in_goal_state // n

    x_tile = idx % n
    y_tile = idx // n

    manhattan = abs(x_tile - x_goal) + abs(y_tile - y_goal)
    return manhattan


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    if puzzle_state.config == GOAL_STATE:
        return True
    else:
        return False


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()

    global GOAL_STATE
    GOAL_STATE = []
    for i in range(0, board_size * board_size):
        GOAL_STATE.append(i)
    GOAL_STATE = list(map(int, GOAL_STATE))

    if search_mode == "bfs":
        bfs_search(hard_state)
    elif search_mode == "dfs":
        dfs_search(hard_state)
    elif search_mode == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    f = open("output.txt", "a")
    f.write("running_time: {}\n".format(end_time - start_time))
    f.write("max_ram_usage: {}\n".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024*1024)))



if __name__ == '__main__':
    main()
