from src.utils import *
import heapq
import numpy as np

"""this file implement A* algorithm for the final search of target object"""


def euclidean_distance(point1: Location, point2: Location) -> float:
    """
    :param point1: firs point as a tuple
    :param point2: second point as a tuple
            
    :return: the Euclidean distance between the two points
    """
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def diagonal_distance(point1: Location, point2: Location) -> float:
    """
    :param point1: firs point as a tuple
    :param point2: second point as a tuple
            
    :return: the diagonal distance between the two points
    """
    x1, y1 = point1
    x2, y2 = point2
    return max(abs(x1 - x2), abs(y1 - y2))


def a_star(map: np.ndarray, start: Location, target: Location,
           excluded: List[Location]) -> List[Location]:
    """
    :param map: the map of the game
    :param start: the starting point as a tuple
    :param target: the target point as a tuple
    :param excluded: the list of the points that cannot be visited
            
    :return: the path as a queue from start to target as a list of tuples
    """

    # fix the heuristic function in base of the agent's movement
    h = euclidean_distance
    # h = diagonal_distance

    # initialize the NOT visited list: it contains the nodes that have to be visited
    not_visited = []
    # initialize the visited list: it contains the nodes that have been visited
    visited = []
    # support list to access the values of g of the node
    support = {start: 0}

    # add the starting point to the NOT visited list (f_value,(position, g))
    heapq.heappush(not_visited, (h(start, target), (start, 0)))

    # initialize the queue that will contain the path
    parent = {start: None}

    while not_visited:
        # get the node with the lowest cost
        current_node, current_g = heapq.heappop(not_visited)[1]

        # if the current node is the target, the path is found
        if current_node == target:
            # print("target found")
            return build_path(parent, target)

        # add the current node to the visited list
        visited.append(current_node)

        # get the neighbors of the current node
        neighbors = get_neighbors(map, current_node, excluded)

        for neighbor in neighbors:
            if neighbor not in visited:
                # calculate the cost of the neighbor
                f_neighbor = h(neighbor, target) + current_g + 1
                # add the neighbor to the NOT visited list
                parent[neighbor] = current_node

                if (neighbor in support.keys()) and current_g + 1 < support[neighbor]:
                    support[neighbor] = current_g + 1
                heapq.heappush(not_visited, (f_neighbor, (neighbor, current_g + 1)))

    print("Target node not found!")
    return None
