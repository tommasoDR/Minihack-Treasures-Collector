from .utils import *
import heapq
import numpy as np

"""This file implements A* algorithm for the final search of target object"""


def compute_straight_path(conditioned_game_map, start: Location, target: Location):
    """
    Compute the straight path from start to target, if it exists.

    :param conditioned_game_map: the map of the game with some fake walls
    :param start: coordinate of the starting point
    :param target: coordinate of the target point

    :return: list of Locations of the straight path
    """

    x_start, y_start = start
    x_target, y_target = target

    path = []
    if x_start == x_target:
        if y_start < y_target:
            for i in range(y_start, y_target + 1):
                if chr(conditioned_game_map[i][x_start]) in ["|", "-", "{"]:
                    return []
                path.append((x_start, i))
        else:
            for i in range(y_target, y_start + 1):
                if chr(conditioned_game_map[i][x_start]) in ["|", "-", "{"]:
                    return []
                path.insert(0, (x_start, i))
    elif y_start == y_target:
        if x_start < x_target:
            for i in range(x_start, x_target + 1):
                if chr(conditioned_game_map[y_start][i]) in ["|", "-", "{"]:
                    return []
                path.append((i, y_start))
        else:
            for i in range(x_target, x_start + 1):
                if chr(conditioned_game_map[y_start][i]) in ["|", "-", "{"]:
                    return []
                path.insert(0, (i, y_start))
    return path


def a_star(conditioned_game_map: np.ndarray, start: Location, target: Location,
           excluded: List[Location]) -> List[Location]:
    """
    :param conditioned_game_map: the map of the game with some fake walls
    :param map: the map of the game
    :param start: the starting point as a tuple
    :param target: the target point as a tuple
    :param excluded: the list of the points that cannot be visited
            
    :return: the path as a queue from start to target as a list of tuples
    """

    path = compute_straight_path(conditioned_game_map, start, target)

    if path:
        return path

    # fix the heuristic function in base of the agent's movement
    h = manhattan_distance
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
        neighbors = get_neighbors_exclude(conditioned_game_map, current_node, excluded)

        for neighbor in neighbors:
            if neighbor not in visited:
                # calculate the cost of the neighbor
                f_neighbor = h(neighbor, target) + current_g + 1
                # add the neighbor to the NOT visited list
                parent[neighbor] = current_node

                if neighbor in support.keys():
                    if current_g + 1 >= support[neighbor]:
                        continue

                support[neighbor] = current_g + 1
                heapq.heappush(not_visited, (f_neighbor, (neighbor, current_g + 1)))

    print("Target node not found!")
    return None
