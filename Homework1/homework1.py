import numpy as np


def calculate_factorial(x: int) -> int:
    if x == 1:
        return 1
    else:
        return x * calculate_factorial(x - 1)


def p1(k: int) -> str:
    answer_string = ""
    for x in range(k, 0, -1):
        factorial = calculate_factorial(x)
        if x == k:
            answer_string = str(factorial)
        else:
            answer_string = answer_string + "," + str(factorial)
    return answer_string


def p2_a(x: list, y: list) -> list:
    y.sort(reverse=True)
    del y[-1]
    return y


def p2_b(x: list, y: list) -> list:
    x.reverse()
    return x


def p2_c(x: list, y: list) -> list:
    new_list = list(set(x + y))
    new_list.sort(reverse=False)
    return new_list


def p2_d(x: list, y: list) -> list:
    return [x, y]


def p3_a(x: set, y: set, z: set) -> set:
    union = x.union(y, z)
    return union


def p3_b(x: set, y: set, z: set) -> set:
    intersection = x.intersection(y, z)
    return intersection


def p3_c(x: set, y: set, z: set) -> set:
    elements_in_x_only = x.difference(y.union(z))
    elements_in_y_only = y.difference(x.union(z))
    elements_in_z_only = z.difference(x.union(y))
    elements_only_in_single_set = elements_in_x_only.union(elements_in_y_only, elements_in_z_only)
    return elements_only_in_single_set


def p4_a() -> np.array:
    l, b = 5, 5
    A = np.array([[0 for j in range(0, l, 1)] for i in range(0, b, 1)])
    for i in range(0, 5, 1):
        for j in range(0, 5, 1):
            if (i == 0 or i == 4) or (j == 0 or j == 4):
                A[i][j] = 1
            elif i == 2 and j == 2:
                A[i][j] = 2
    return A


def is_there_a_knight(x: int) -> bool:
    if x == 1:
        return True
    else:
        return False


def valid_position_for_knight(i: int, j: int) -> bool:
    if (0 <= i) and (i < 5) and (0 <= j) and (j < 5):
        return True
    else:
        return False


def knight_attacking_the_white_pawn(x: np.array, i: int, j: int) -> bool:
    for row_change in [2, 1, -1, -2]:
        if row_change in [1, -1]:
            for column_change in [2, -2]:
                if valid_position_for_knight(i + row_change, j + column_change) and \
                        x[i + row_change][j + column_change] == 2:
                    return True
        elif row_change in [2, -2]:
            for column_change in [1, -1]:
                if valid_position_for_knight(i + row_change, j + column_change) and \
                        x[i + row_change][j + column_change] == 2:
                    return True


def p4_b(x: np.array) -> list:
    threaten_the_white_pawn = []
    for i in range(0, 5, 1):
        for j in range(0, 5, 1):
            if is_there_a_knight(x[i][j]) and knight_attacking_the_white_pawn(x, i, j):
                threaten_the_white_pawn.append((i, j))
    return threaten_the_white_pawn


def p5_a(x: dict) -> int:
    no_of_isolated_notes = 0
    for key in x.keys():
        if len(x[key]) == 0:
            no_of_isolated_notes += 1
    return no_of_isolated_notes


def p5_b(x: dict) -> int:
    return len(x) - p5_a(x)


def p5_c(x: dict) -> list:
    edges = []
    for starting_node in x.keys():
        for ending_node in x[starting_node]:
            if (starting_node, ending_node) in edges or (ending_node, starting_node) in edges:
                pass
            else:
                edges.append((starting_node, ending_node))
    return edges


def p5_d(x: dict) -> np.array:
    l, b = len(x), len(x)
    adj_matrix = np.array([[0 for j in range(0, l, 1)] for i in range(0, b, 1)])
    index = 0
    indexed_dict = {}
    for keys in x.keys():
        indexed_dict[keys] = index
        index += 1
    for starting_node in x.keys():
        for ending_node in x[starting_node]:
            adj_matrix[indexed_dict[starting_node]][indexed_dict[ending_node]] = 1
    return adj_matrix


class PriorityQueue(object):
    def __init__(self):
        self.market_price = {'apple': 5.0, 'banana': 4.5, 'carrot': 3.3, 'kiwi': 7.4, 'orange': 5.0, 'mango': 9.1,
                             'pineapple': 9.1}
        self.priority_queue = []

    def push(self, x):
        self.priority_queue.append((x, self.market_price[x]))
        self.priority_queue.sort(key=lambda element: element[1], reverse=True)
        return self.priority_queue

    def pop(self):
        return self.priority_queue.pop(0)[0]

    def is_empty(self):
        if len(self.priority_queue) == 0:
            return True
        else:
            return False


if __name__ == '__main__':
    print(p1(k=8))
    print('-----------------------------')
    print(p2_a(x=[], y=[1, 3, 5]))
    print(p2_b(x=[2, 4, 6], y=[]))
    print(p2_c(x=[1, 3, 5, 7], y=[1, 2, 5, 6]))
    print(p2_d(x=[1, 3, 5, 7], y=[1, 2, 5, 6]))
    print('------------------------------')
    print(p3_a(x={1, 3, 5, 7}, y={1, 2, 5, 6}, z={7, 8, 9, 1}))
    print(p3_b(x={1, 3, 5, 7}, y={1, 2, 5, 6}, z={7, 8, 9, 1}))
    print(p3_c(x={1, 3, 5, 7}, y={1, 2, 5, 6}, z={7, 8, 9, 1}))
    print('------------------------------')
    print(p4_a())
    print(p4_b(p4_a()))
    print('------------------------------')
    graph = {
        'A': ['D', 'E'],
        'B': ['E', 'F'],
        'C': ['E'],
        'D': ['A', 'E'],
        'E': ['A', 'B', 'C', 'D'],
        'F': ['B'],
        'G': []
    }
    print(p5_a(graph))
    print(p5_b(graph))
    print(p5_c(graph))
    print(p5_d(graph))
    print('------------------------------')
    pq = PriorityQueue()
    pq.push('apple')
    pq.push('kiwi')
    pq.push('orange')
    while not pq.is_empty():
        print(pq.pop())
