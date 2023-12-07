import math
from enum import Enum
from generate_room import *
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


def get_neighbors(game_map: np.ndarray, current: Location, excluded: List[Location]) -> List[Location]:
    """
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

    return neighbors


def build_path(parent: dict, target: Location) -> List[Location]:
    """
    build the path from the target to the start
    :param parent: the dictionary that contains the parent of each node
    :param target: the target node

    :return: the path as a list of tuples
    """

    path = []
    while target is not None:
        path.insert(0, target)
        target = parent[target]
    return path


def get_player_location(game_map: np.ndarray, symbol: str = "@") -> Location:
    """
    :param game_map: the map of the game
    :param symbol: the symbol of the player

    :return: the position of the player as a tuple
    """

    y, x = np.where(game_map == ord(symbol))
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
    for y in range(len(matrix_map)):
        for x in range(len(matrix_map[y])):
            if chr(matrix_map[y][x]) in walkable_symbols:
                floor_positions.append((x, y))
    return floor_positions


def get_direction(x_start, y_start, x_target, y_target) -> Direction:
    """
    Given two points, returns the direction to go from the first to the second.

    :param x_start: The x coordinate of the starting point
    :param y_start: The y coordinate of the starting point
    :param x_current: The x coordinate of the current point
    :param y_current: The y coordinate of the current point

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

    :param start: The starting position of the agent
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


def euclidean_distance(point1: Location, point2: Location) -> float:
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def manhattan_distance(point1: Location, point2: Location) -> int:
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def floor_visited(list: List[Location]) -> List[Location]:
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


def print_level(state):
    """
    Given a state, save an image of the level.

    :param state: the state of the game
    """
    plt.imshow(state["pixel"][:, 410:840])
    plt.savefig("level.png")
