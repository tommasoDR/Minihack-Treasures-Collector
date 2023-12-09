import math
from enum import Enum
from matplotlib import pyplot as plt
from .generate_room import *
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
    NORTH_EAST = 4
    SOUTH_EAST = 5
    SOUTH_WEST = 6
    NORTH_WEST = 7


def allowed_moves(game_map: np.ndarray, position_element: int, excluded: List[Location]) -> bool:
    """
    :param game_map: the map of the game
    :param position_element: a tuple that contains a position on the map
    :param excluded: the list of the points that cannot be visited
    :return: True if the position is allowed, False otherwise
    """

    x, y = position_element
    obstacles = ["-", "|"]
    return (chr(game_map[y, x]) not in obstacles) and (position_element not in excluded)


def get_neighbors_exclude(game_map: np.ndarray, current: Location, excluded: List[Location]) -> List[Location]:
    """
    Create the list of the neighbors of the current position.
    A neighbor is a position that the agent

    :param game_map: the map of the game
    :param current: the current position as a tuple
    :param excluded: the list of the points that cannot be visited
    :return: the list of the neighbors of the current position
    """

    y_limit, x_limit = game_map.shape
    neighbors = []
    x, y = current
    # North
    if y - 1 > 0 and allowed_moves(game_map, (x, y - 1), excluded):
        neighbors.append((x, y - 1))
    # East
    if x + 1 < x_limit and allowed_moves(game_map, (x + 1, y), excluded):
        neighbors.append((x + 1, y))
    # South
    if y + 1 < y_limit and allowed_moves(game_map, (x, y + 1), excluded):
        neighbors.append((x, y + 1))
    # West
    if x - 1 > 0 and allowed_moves(game_map, (x - 1, y), excluded):
        neighbors.append((x - 1, y))
    """
    # North-est
    if y - 1 > 0 and x + 1 < x_limit and allowed_moves(game_map, (x + 1, y - 1), excluded):
        neighbors.append((x + 1, y - 1))
    # North-west
    if y - 1 > 0 and x - 1 > 0 and allowed_moves(game_map, (x - 1, y - 1), excluded):
        neighbors.append((x - 1, y - 1))
    # South-est
    if y + 1 < y_limit and x + 1 < x_limit and allowed_moves(game_map, (x + 1, y + 1), excluded):
        neighbors.append((x + 1, y + 1))
    # South-west
    if y + 1 < y_limit and x - 1 > 0 and allowed_moves(game_map, (x - 1, y + 1), excluded):
        neighbors.append((x - 1, y + 1))
    """
    return neighbors


def build_path(parent: dict, target: Location) -> List[Location]:
    """
    Build the path from the target to the start.

    :param parent: the dictionary that contains the parent of each node
    :param target: the target Location
    :return: the path as a list of Location
    """

    path = []
    while target is not None:
        path.insert(0, target)
        target = parent[target]
    return path


def get_player_location(game_map: np.ndarray, symbol: str = "@") -> Location:
    """
    Gets the position of the player in the game map.

    :param game_map: the map of the game
    :param symbol: the symbol of the player
    :return: a tuple that contains the position of the player in the map
    """

    y, x = np.where(game_map == ord(symbol))
    return x[0], y[0]


def get_walkable_symbols():
    (clue_objects, goal_objects) = read_object_file(object_file_path)
    clue_object_symbols = [symbol for (_, _, display_symbols, _) in clue_objects for symbol in display_symbols]
    goal_object_symbols = [object_symbol for (_, object_symbol) in goal_objects]
    walkable_symbols = clue_object_symbols + goal_object_symbols + ['.'] + ['@']
    return walkable_symbols


def get_floor_positions(game_map) -> List[Location]:
    """
    Gets the list of the floor positions in the game map.

    :param game_map: the map of the game
    :return: the list of the floor positions
    """

    floor_positions = []
    walkable_symbols = get_walkable_symbols()
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            if chr(game_map[y][x]) in walkable_symbols:
                floor_positions.append((x, y))
    return floor_positions


def get_wall_positions(game_map) -> List[Location]:
    """
    Gets the list of the wall positions in the game map.

    :param game_map: the map of the game
    :return: the list of the wall positions
    """
    wall = ['|', '-']
    wall_positions = []
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            if chr(game_map[y][x]) in wall:
                wall_positions.append((x, y))
    return wall_positions


def get_direction(x_start, y_start, x_target, y_target) -> Direction:
    """
    Given two points, returns the direction to go from the first to the second.

    :param x_start: The x coordinate of the starting point
    :param y_start: The y coordinate of the starting point
    :param x_target: The x coordinate of the current point
    :param y_target: The y coordinate of the current point
    :return: The direction to go from the first to the second point

    :raises ValueError: If the two points are on the same line or column
    """
    if x_start == x_target:
        return Direction.NORTH if y_start > y_target else Direction.SOUTH
    elif y_start == y_target:
        return Direction.WEST if x_start > x_target else Direction.EAST
    elif x_start > x_target:
        return Direction.NORTH_WEST if y_start > y_target else Direction.SOUTH_WEST
    elif x_start < x_target:
        return Direction.NORTH_EAST if y_start > y_target else Direction.SOUTH_EAST
    else:
        raise ValueError("The two points are on the same line or column")


def actions_from_path(path: List[Location]) -> List[int]:
    """
    Given a path, returns the list of actions to perform to follow the path.

    :param path: The path to follow as a list of Location
    :return: The list of actions to perform to follow the path
    """
    actions = []
    if not path:
        return []
    x_start, y_start = path.pop(0)
    for x, y in path:
        actions.append(get_direction(x_start, y_start, x, y).value)
        x_start, y_start = x, y
    return actions


def TFFFM_distance(game_map, start: Location, target: Location) -> int:
    """
    Custom distance between two points. It is a slightly modified version of the Manhattan distance.
    It counts with more penalty a path that crosses a wall.
    By Tommaso, Francesco, Francesc, Fabrizio, Marco.

    :param game_map: the map of the game
    :param start: the starting point
    :param target: the target point
    :return: the custom (TFFM) distance between the two points
    """

    def increase_distance(symbol: str) -> int:
        """
        Increase the distance by 30 if the symbol is a wall, 1 otherwise.

        :param symbol: the symbol to check
        :return: 30 if the symbol is a wall, 1 otherwise
        """
        return 30 if symbol == '-' or symbol == '|' else 1

    distance1 = 0
    distance2 = 0
    x_start, y_start = start
    x_target, y_target = target

    x_start_or, y_start_or = start
    x_target_or, y_target_or = target

    if x_start > x_target:
        x_start, x_target = x_target, x_start
    if y_start > y_target:
        y_start, y_target = y_target, y_start

    for i in range(x_start, x_target + 1):
        t1 = chr(game_map[y_start_or][i])
        t2 = chr(game_map[y_target_or][i])
        distance1 += increase_distance(t1)
        distance2 += increase_distance(t2)

    for i in range(y_start, y_target + 1):
        t1 = chr(game_map[i][x_target_or])
        t2 = chr(game_map[i][x_start_or])
        distance1 += increase_distance(t1)
        distance2 += increase_distance(t2)

    return min(distance1, distance2)


def euclidean_distance(point1: Location, point2: Location) -> float:
    """
    Computes the Euclidean distance between two points.

    :param point1: the first point as a tuple (x1, y1)
    :param point2: the second point as a tuple (x2, y2)
    :return: the Euclidean distance between the two points
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def manhattan_distance(point1: Location, point2: Location) -> int:
    """
    Computes the Manhattan distance between two points.

    :param point1: the first point as a tuple (x1, y1)
    :param point2: the second point as a tuple (x2, y2)
    :return: an integer representing the Manhattan
    """
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def diagonal_distance(point1: Location, point2: Location) -> float:
    """
    Computes the diagonal distance between two points.

    :param point1: the first point as a tuple (x1, y1)
    :param point2: the second point as a tuple (x2, y2)
    :return: the diagonal distance between the two points
    """
    x1, y1 = point1
    x2, y2 = point2
    return max(abs(x1 - x2), abs(y1 - y2))


def get_neighbors(list: List[Location]) -> List[Location]:
    """
    Given a list of points, returns the list of the neighbor points, based on the agent FOV.

    :param list: a list of points as a list of tuples
    :return: the list of the neighbor points as a list of tuples
    """
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


def precondition_game_map(game_map):
    """
    Given a game map, returns a map with fake walls, to let the agent explore better the map.

    :param game_map: the map of the game
    :return: the map of the game with fake walls
    """
    wall_position = get_wall_positions(game_map)
    y_limit, x_limit = game_map.shape
    wall = ['|', '-', '{']
    conditioned_map = np.copy(game_map)
    for x, y in wall_position:
        if y + 2 < y_limit and chr(conditioned_map[y + 1][x]) not in wall and chr(
                conditioned_map[y + 2][x]) not in wall:
            if check_path(conditioned_map, (x, y + 1)):
                conditioned_map[y + 1][x] = ord('{')
        if x + 2 < x_limit and chr(conditioned_map[y][x + 1]) not in wall and chr(
                conditioned_map[y][x + 2]) not in wall:
            if check_path(conditioned_map, (x + 1, y)):
                conditioned_map[y][x + 1] = ord('{')
        if y - 2 >= 0 and chr(conditioned_map[y - 1][x]) not in wall and chr(conditioned_map[y - 2][x]) not in wall:
            if check_path(conditioned_map, (x, y - 1)):
                conditioned_map[y - 1][x] = ord('{')
        if x - 2 >= 0 and chr(conditioned_map[y][x - 1]) not in wall and chr(conditioned_map[y][x - 2]) not in wall:
            if check_path(conditioned_map, (x - 1, y)):
                conditioned_map[y][x - 1] = ord('{')

    return conditioned_map


def closest_wall_target(target, conditioned_map):
    """
    Given a target, returns the closest walkable point to the target.

    :param target: the target point
    :param conditioned_map: the map of the game with fake walls
    :return:
    """
    walkable_symbols = get_walkable_symbols()
    neighbors = get_neighbors([target])
    for point in neighbors:
        x, y = point
        symbol = chr(conditioned_map[y][x])
        if symbol in walkable_symbols:
            return point


def check_path(game_map, position: Location) -> bool:
    """
    Checks if for some walkable adjacent location to position, there exists another adjacent location (to
    both of them) that is walkable.

    :param game_map: the map of the game
    :param position: the position to check
    :return: True if the property holds, False otherwise
    """
    x, y = position
    y_limit, x_limit = game_map.shape
    walkable_symbols = get_walkable_symbols()
    if y + 1 < y_limit and x + 1 < x_limit and chr(game_map[y + 1][x]) in walkable_symbols and chr(
            game_map[y][x + 1]) in walkable_symbols:
        if chr(game_map[y + 1][x + 1]) not in walkable_symbols:
            return False
    if y + 1 < y_limit and x - 1 >= 0 and chr(game_map[y + 1][x]) in walkable_symbols and chr(
            game_map[y][x - 1]) in walkable_symbols:
        if chr(game_map[y + 1][x - 1]) not in walkable_symbols:
            return False
    if y - 1 >= 0 and x + 1 < x_limit and chr(game_map[y - 1][x]) in walkable_symbols and chr(
            game_map[y][x + 1]) in walkable_symbols:
        if chr(game_map[y - 1][x + 1]) not in walkable_symbols:
            return False
    if y - 1 >= 0 and x - 1 >= 0 and chr(game_map[y - 1][x]) in walkable_symbols and chr(
            game_map[y][x - 1]) in walkable_symbols:
        if chr(game_map[y - 1][x - 1]) not in walkable_symbols:
            return False
    return True


def print_level(state):
    """
    Given a state, displays and saves an image of the level.

    :param state: the state of the game
    """
    plt.imshow(state["pixel"][:, 410:840])
    plt.savefig("level.png")


def print_chars_level(game_map):
    """
    Given a game map, displays its characters.

    :param game_map: the map of the game
    """
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            print(chr(game_map[y][x]), end='')
        print()
