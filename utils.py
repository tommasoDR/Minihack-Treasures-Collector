import numpy as np
import math
from generate_room import*
from queue import PriorityQueue
from typing import Tuple, List

def get_player_location(game_map: np.ndarray, symbol : str = "@") -> Tuple[int, int]:
    x, y = np.where(game_map == ord(symbol))
    return (x[0], y[0])

def is_wall(position_element: int) -> bool:
    obstacles = "|- "
    return chr(position_element) in obstacles

def get_valid_moves(game_map: np.ndarray, current_position: Tuple[int, int]) -> List[Tuple[int, int]]:
    x_limit, y_limit = game_map.shape
    valid = []
    x, y = current_position    
    # North
    if y - 1 > 0 and not is_wall(game_map[x, y-1]):
        valid.append((x, y-1)) 
    # East
    if x + 1 < x_limit and not is_wall(game_map[x+1, y]):
        valid.append((x+1, y)) 
    # South
    if y + 1 < y_limit and not is_wall(game_map[x, y+1]):
        valid.append((x, y+1)) 
    # West
    if x - 1 > 0 and not is_wall(game_map[x-1, y]):
        valid.append((x-1, y))

    return valid

def actions_from_path(start: Tuple[int, int], path: List[Tuple[int, int]]) -> List[int]:
    action_map = {
        "N": 0,
        "E": 1,
        "S": 2,
        "W": 3
    }
    actions = []
    x_s, y_s = start
    for (x, y) in path:
        if x_s == x:
            if y_s > y:
                actions.append(action_map["W"])
            else: actions.append(action_map["E"])
        elif y_s == y:
            if x_s > x:
                actions.append(action_map["N"])
            else: actions.append(action_map["S"])
        else:
            raise Exception("x and y can't change at the same time. oblique moves not allowed!")
        x_s = x
        y_s = y
    
    return actions

def euclidean_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def manhattan_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def get_floor_positions(state):
    floor_positions = []
    matrix_map = state["chars"]
    (clue_objects, goal_objects) = read_object_file(object_file_path)
    clue_object_symbols = [object_symbol for (_, object_symbol,_) in clue_objects]
    goal_object_symbols = [object_symbol for (_, object_symbol) in goal_objects]
    walkable_symbols = clue_object_symbols + goal_object_symbols + ['.']
    for i in range(len(matrix_map)):
        for j in range(len(matrix_map[i])):
            if chr(matrix_map[i][j]) in walkable_symbols:
                floor_positions.append((i,j))
    return floor_positions

# given a path it returns all the points to be considered visited
def already_visited(list: List[Tuple[int, int]]): 
    floor_already_visited = []
    for tuple in list: 
        x, y = tuple
        floor_already_visited.append((x, y))
        floor_already_visited.append((x-1, y-1))
        floor_already_visited.append((x-1, y))
        floor_already_visited.append((x-1, y+1))
        floor_already_visited.append((x, y+1))
        floor_already_visited.append((x+1, y+1))
        floor_already_visited.append((x+1, y))
        floor_already_visited.append((x+1, y-1))
        floor_already_visited.append((x, y-1))
    
    return floor_already_visited

def build_path(parent: dict, target: Tuple[int, int]) -> List[Tuple[int, int]]:
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    path.reverse()
    return path

def a_star(game_map: np.ndarray, start: Tuple[int, int], target: Tuple[int, int], h: callable) -> List[Tuple[int, int]]:
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
            print("Target found!")
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
