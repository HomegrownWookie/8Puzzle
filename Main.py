import math
import time
from operator import itemgetter

PUZZLE_TYPE = 8
MAT_SIZE = int(math.sqrt(PUZZLE_TYPE + 1))


class PriorityQueue(object):

    def __init__(self):
        self.elements = []
        self.max_elements = 0

    def get_max_elements(self):
        return self.max_elements

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, h=0, g=0, priority=0):
        self.elements.append((priority, h, g, item))
        self.elements.sort(key=itemgetter(0))
        self.max_elements = self.max_elements if self.max_elements > len(self.elements) else len(self.elements)

    def get_item(self):
        return self.elements.pop(0)


class Problem(object):

    def __init__(self, initial_state=None):
        self.initial_state = initial_state
        self.goal_state = self.get_goal()
        self.explored = []

    def goal_test(self, node):
        self.explored.append(node)
        return node == self.goal_state

    def get_level(self):
        return len(self.explored)

    def is_explored(self, node):
        return node in self.explored

    def get_current_state(self):
        return self.initial_state

    def get_goal_state(self):
        return self.goal_state

    def get_goal(self):
        goal = []
        for x in range(1, PUZZLE_TYPE + 1):
            goal.append(x)
        goal.append(-1)
        return goal

    def print_current_board(self):
        print_board(self.initial_state)


"""
Print the current state of board
"""


def print_board(mat):
    print("\nBoard:")
    print("*" * 5 * MAT_SIZE)
    for index, val in enumerate(mat):
        if (index + 1) % MAT_SIZE == 0:
            print(val if val != -1 else "x")
        else:
            print(val if val != -1 else "x", " ",)
    print("*" * 5 * MAT_SIZE)

"""
Check if move up operation is possible
"""


def can_move_up(mat):
    return True if mat.index(-1) >= MAT_SIZE else False


"""
Check if move down operation is possible
"""


def can_move_down(mat):
    return True if mat.index(-1) < PUZZLE_TYPE + 1 - MAT_SIZE else False


"""
Check if move left operation is possible
"""


def can_move_left(mat):
    return False if mat.index(-1) % MAT_SIZE == 0 else True


"""
Check if move right operation is possible
"""


def can_move_right(mat):
    return False if mat.index(-1) % MAT_SIZE == MAT_SIZE - 1 else True


"""
Performs the move up operation
"""


def move_x_up(mat):
    if can_move_up(mat):
        index = mat.index(-1)
        mat[index - MAT_SIZE], mat[index] = mat[index], mat[index - MAT_SIZE]
        return mat
    return None


"""
Performs the move down operation
"""


def move_x_down(mat):
    if can_move_down(mat):
        index = mat.index(-1)
        mat[index + MAT_SIZE], mat[index] = mat[index], mat[index + MAT_SIZE]
        return mat
    return None


"""
Performs the move left operation
"""


def move_x_left(mat):
    if can_move_left(mat):
        index = mat.index(-1)
        mat[index - 1], mat[index] = mat[index], mat[index - 1]
        return mat
    return None


"""
Performs the move right operation
"""


def move_x_right(mat):
    if can_move_right(mat):
        index = mat.index(-1)
        mat[index + 1], mat[index] = mat[index], mat[index + 1]
        return mat
    return None


"""
General search algorithm
"""


def general_search(problem, queueing_func):
    depth = 0
    nodes = PriorityQueue()
    nodes.put(problem.get_current_state())
    while not nodes.empty():
        entire_node = nodes.get_item()
        node = entire_node[3]
        if (entire_node[2] or entire_node[1]):
            print("The best state to expand with a g(n) = %d and h(n) = %d is.." % (entire_node[2], entire_node[1]),)
        print_board(node)
        if problem.goal_test(node):
            print("Goal State")
            print("To solve this problem the search algorithm expanded a total of %d nodes." % problem.get_level())
            print("The maximum number of nodes in the queue at any one time was %d." % nodes.get_max_elements())
            print("The depth of the goal node was %d" % entire_node[2])
            return node
        print("Expanding this state\n\n")
        queueing_func(nodes, expand(entire_node, problem))
        depth += 1


"""
Expands the current node using all the operators and returns the queue.
"""


def expand(node, problem):
    all_nodes = PriorityQueue()
    node1 = move_x_up(node[3][:])
    node2 = move_x_down(node[3][:])
    node3 = move_x_left(node[3][:])
    node4 = move_x_right(node[3][:])
    if node1 and not problem.is_explored(node1):
        all_nodes.put(node1, 0, node[2] + 1, 0)
    if node2 and not problem.is_explored(node2):
        all_nodes.put(node2, 0, node[2] + 1, 0)
    if node3 and not problem.is_explored(node3):
        all_nodes.put(node3, 0, node[2] + 1, 0)
    if node4 and not problem.is_explored(node4):
        all_nodes.put(node4, 0, node[2] + 1, 0)
    return all_nodes


"""
Queueing function for Unifrom Cost Search.
"""


def uniform_cost_search(nodes, new_nodes):
    while not new_nodes.empty():
        node = new_nodes.get_item()
        nodes.put(node[3], 0, node[2], 0)


"""
Calculates the heuristic using the misplaced tile.
"""


def calculate_misplaced(node):
    count = 0
    for i in range(PUZZLE_TYPE):
        if i + 1 != node[i]:
            count += 1
    return count


"""
Calculates the heuristic using the manhattan distance.
"""


def manhattan_distance(node):
    count = 0
    for i in range(PUZZLE_TYPE):
        index = node.index(i + 1)
        row_diff = abs((i / MAT_SIZE) - (index / MAT_SIZE))
        col_diff = abs((i % MAT_SIZE) - (index % MAT_SIZE))
        count += (row_diff + col_diff)
    index = node.index(-1)
    row_diff = abs((PUZZLE_TYPE / MAT_SIZE) - (index / MAT_SIZE))
    col_diff = abs((PUZZLE_TYPE % MAT_SIZE) - (index % MAT_SIZE))
    count += (row_diff + col_diff)
    return count


"""
Queueing function for Misplaced Tile Heuristic.
"""


def misplaced_tile_heuristic(nodes, new_nodes):
    while not new_nodes.empty():
        node = new_nodes.get_item()
        nodes.put(node[3], calculate_misplaced(node[3]), node[2], calculate_misplaced(node[3]) + node[2])


"""
Queueing function for Manhattan Distance Heuristic.
"""


def manhattan_distance_heuristic(nodes, new_nodes):
    while not new_nodes.empty():
        node = new_nodes.get_item()
        nodes.put(node[3], manhattan_distance(node[3]), node[2], manhattan_distance(node[3]) + node[2])


if __name__ == "__main__":
    print("Welcome to the awesome %d-puzzle solver." % PUZZLE_TYPE)
    print("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle.")
    choice = int(input())
    mat = []
    if choice == 1:
        mat = [3,1,2,4,-1,5,6,7,8]
    elif choice == 2:
        print("Enter elements for %d Puzzle." % PUZZLE_TYPE)
        print("NOTE: Use \"x\" for blank.\n")
        for i in range(MAT_SIZE):
            print("Enter elements for row %d" % (i + 1))
            mat.extend([-1 if x == "x" else int(x) for x in input().split()])

    problem = Problem(mat)
    print("Initial State",)
    problem.print_current_board()
    print("Goal State"),
    print_board(problem.get_goal_state())
    print("\n\n")
    print("*" * 50)
    print("Enter your choice of algorithm:\n1. Uniform Cost Search\n2. A* with the Misplaced Tile heuristic.\n"
          "3. A* with the Manhattan distance heuristic.")
    choice = int(input())
    t1 = 0
    if choice == 1:
        t1 = time.time()
        general_search(problem, uniform_cost_search)
    elif choice == 2:
        t1 = time.time()
        general_search(problem, misplaced_tile_heuristic)
    elif choice == 3:
        t1 = time.time()
        general_search(problem, manhattan_distance_heuristic)
    else:
        print("Invalid choice.")
    t2 = time.time()
    print("The algorithm took " + str((t2 - t1) * 1000) + " ms of time.")