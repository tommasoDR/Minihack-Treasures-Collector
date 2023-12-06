import math
from enum import Enum

from src.generate_room import *
from queue import PriorityQueue
from typing import Tuple, List, NewType

Location = NewType("Location", Tuple[int, int])
Location.__doc__ = "A location in the game map."


class Direction(Enum):
    """
    A possible direction of the agent.
    """
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def allowed_moves(game_map: np.ndarray, position_element: int, excludeds: List[Tuple[int, int]]) -> bool:
    """
    :param game_map: the map of the game
    :param position_element: a tuple that contains a position on the map
    :param excludeds: the list of the points that cannot be visited

    :return: True if the position is allowed, False otherwise
    """

    x, y = position_element
    obstacles = ["-", "|"]
    return (chr(game_map[x, y]) not in obstacles) and (position_element not in excludeds)


def get_neighbors(game_map: np.ndarray, current: Tuple[int, int], excludeds: List[Tuple[int, int]]) -> List[
    Tuple[int, int]]:
    """
    :param game_map: the map of the game
    :param current: the current position as a tuple
    :param excludeds: the list of the points that cannot be visited

    :return: the list of the neighbors of the current position
    """

    x_limit, y_limit = game_map.shape
    neighbors = []
    x, y = current
    # North
    if y - 1 > 0 and allowed_moves(game_map, (x, y - 1), excludeds):
        neighbors.append((x, y - 1))
        # East
    if x + 1 < x_limit and allowed_moves(game_map, (x + 1, y), excludeds):
        neighbors.append((x + 1, y))
        # South
    if y + 1 < y_limit and allowed_moves(game_map, (x, y + 1), excludeds):
        neighbors.append((x, y + 1))
        # West
    if x - 1 > 0 and allowed_moves(game_map, (x - 1, y), excludeds):
        neighbors.append((x - 1, y))

    # North-est
    if y - 1 > 0 and x + 1 < x_limit and allowed_moves(game_map, (x + 1, y - 1), excludeds):
        neighbors.append((x + 1, y - 1))
        # North-west
    if y - 1 > 0 and x - 1 > 0 and allowed_moves(game_map, (x - 1, y - 1), excludeds):
        neighbors.append((x - 1, y - 1))
        # South-est
    if y + 1 < y_limit and x + 1 < x_limit and allowed_moves(game_map, (x + 1, y + 1), excludeds):
        neighbors.append((x + 1, y + 1))
        # South-west
    if y + 1 < y_limit and x - 1 > 0 and allowed_moves(game_map, (x - 1, y + 1), excludeds):
        neighbors.append((x - 1, y + 1))

    return neighbors


def build_path(parent: dict, target: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    build the path from the target to the start
    :param parent: the dictionary that contains the parent of each node
    :param target: the target node

    :retunr: the path as a list of tuples
    """

    path = []
    while target is not None:
        path.insert(0, target)
        target = parent[target]
    return path


def get_player_location(game_map: np.ndarray, symbol: str = "@") -> Tuple[int, int]:
    """
    :param game_map: the map of the game
    :param symbol: the symbol of the player

    :return: the position of the player as a tuple
    """

    x, y = np.where(game_map == ord(symbol))
    return x[0], y[0]


def get_floor_positions(state):
    """
    :param state: the state of the game

    :return: the list of the floor positions
    """

    floor_positions = []
    matrix_map = state["chars"]
    (clue_objects, goal_objects) = read_object_file(object_file_path)
    clue_object_symbols = [object_symbol for (_, object_symbol, _) in clue_objects]
    goal_object_symbols = [object_symbol for (_, object_symbol) in goal_objects]
    walkable_symbols = clue_object_symbols + goal_object_symbols + ['.']
    for i in range(len(matrix_map)):
        for j in range(len(matrix_map[i])):
            if chr(matrix_map[i][j]) in walkable_symbols:
                floor_positions.append((i, j))
    return floor_positions


def is_wall(position_element: int) -> bool:
    obstacles = "|- "
    return chr(position_element) in obstacles


def get_valid_moves(game_map: np.ndarray, current_position: Location) -> List[Location]:
    x_limit, y_limit = game_map.shape
    valid = []
    x, y = current_position
    # North
    if y - 1 > 0 and not is_wall(game_map[x, y - 1]):
        valid.append((x, y - 1))
        # East
    if x + 1 < x_limit and not is_wall(game_map[x + 1, y]):
        valid.append((x + 1, y))
        # South
    if y + 1 < y_limit and not is_wall(game_map[x, y + 1]):
        valid.append((x, y + 1))
        # West
    if x - 1 > 0 and not is_wall(game_map[x - 1, y]):
        valid.append((x - 1, y))

    return valid


def get_direction(x_start, y_start, x_current, y_current) -> Direction:
    """
    Given two points, returns the direction to go from the first to the second.

    :param x_start: The x coordinate of the starting point
    :param y_start: The y coordinate of the starting point
    :param x_current: The x coordinate of the current point
    :param y_current: The y coordinate of the current point

    :return: The direction to go from the first to the second point

    :raises ValueError: If the two points are on the same line or column
    """
    if x_start == x_current:
        return Direction.WEST if y_start > y_current else Direction.EAST
    elif y_start == y_current:
        return Direction.NORTH if x_start > x_current else Direction.SOUTH
    else:
        raise ValueError("x and y can't change at the same time. Oblique moves not allowed!")


def actions_from_path(start: Location, path: List[Location]) -> List[int]:
    """
    Given a path, returns the list of actions to perform to follow the path.

    :param start: The starting position of the agent
    :param path: The path to follow as a list of Location
    :return: The list of actions to perform to follow the path
    """
    actions = []
    x_start, y_start = start
    for x, y in path:
        actions.append(get_direction(x_start, y_start, x, y).value)
        x_start, y_start = x, y
    return actions


def euclidean_distance(point1: Location, point2: Location) -> float:
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def manhattan_distance(point1: Location, point2: Location) -> int:
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def already_visited(list: List[Location]) -> List[Location]:
    floor_already_visited = []
    for x, y in list:
        floor_already_visited.append((x, y))
        floor_already_visited.append((x - 1, y - 1))
        floor_already_visited.append((x - 1, y))
        floor_already_visited.append((x - 1, y + 1))
        floor_already_visited.append((x, y + 1))
        floor_already_visited.append((x + 1, y + 1))
        floor_already_visited.append((x + 1, y))
        floor_already_visited.append((x + 1, y - 1))
        floor_already_visited.append((x, y - 1))

    return floor_already_visited


def a_star(game_map: np.ndarray, start: Location, target: Location, h: callable) -> List[Location]:
    # initialize open and close list
    open_list = PriorityQueue()
    close_list = []
    # additional dict which maintains the nodes in the open list for an easier access and check
    support_list = {}
    starting_state_g = 0
    starting_state_h = h(start, target)
    starting_state_f = starting_state_g + starting_state_h
    open_list.put((starting_state_f, (start, starting_state_g)))
    support_list[start] = starting_state_g
    parent = {start: None}
    while not open_list.empty():
        # get the node with lowest f
        _, (current, current_cost) = open_list.get()
        # add the node to the close list
        close_list.append(current)
        if current == target:
            # print("Target found!")
            path = build_path(parent, target)
            return path
        for neighbor in get_valid_moves(game_map, current):
            # check if neighbor in close list, if so continue
            if neighbor in close_list:
                continue
            # compute neighbor g, h and f values
            neighbor_g = 1 + current_cost
            neighbor_h = h(neighbor, target)
            neighbor_f = neighbor_g + neighbor_h
            parent[neighbor] = current
            neighbor_entry = (neighbor_f, (neighbor, neighbor_g))
            # if neighbor in open_list
            if neighbor in support_list.keys():
                # if neighbor_g is greater or equal to the one in the open list, continue
                if neighbor_g >= support_list[neighbor]:
                    continue
            # add neighbor to open list and update support_list
            open_list.put(neighbor_entry)
            support_list[neighbor] = neighbor_g
    print("Target node not found!")
    return None
