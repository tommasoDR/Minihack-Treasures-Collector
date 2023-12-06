from typing import Tuple, List
from generate_room import read_object_file
from src.data import object_file_path
import numpy as np


def allowed_moves(game_map: np.ndarray, position_element: int, excludeds: List[Tuple[int, int]]) -> bool:

    """
    :param game_map: the map of the game
    :param position_element: a tuple that contains a position on the map
    :param excludeds: the list of the points that cannot be visited
            
    :return: True if the position is allowed, False otherwise
    """
    
    x, y = position_element
    obstacles = ["-","|"]
    return (chr(game_map[x, y]) not in obstacles) and (position_element not in excludeds)

def get_neighbors(game_map: np.ndarray, current: Tuple[int, int], excludeds: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    
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
    if y - 1 > 0 and allowed_moves(game_map, (x, y-1), excludeds):
        neighbors.append((x, y-1)) 
    # East
    if x + 1 < x_limit and allowed_moves(game_map, (x+1, y), excludeds):
        neighbors.append((x+1, y)) 
    # South
    if y + 1 < y_limit and allowed_moves(game_map, (x, y+1),  excludeds):
        neighbors.append((x, y+1)) 
    # West
    if x - 1 > 0 and allowed_moves(game_map, (x-1, y), excludeds):
        neighbors.append((x-1, y))
      
    # North-est
    if y - 1 > 0 and x + 1 < x_limit and allowed_moves(game_map, (x+1, y-1), excludeds):
        neighbors.append((x+1, y-1)) 
    # North-west
    if y - 1 > 0 and x - 1 > 0 and allowed_moves(game_map, (x-1, y-1), excludeds):
        neighbors.append((x-1, y-1)) 
    # South-est
    if y + 1 < y_limit and x + 1 < x_limit  and allowed_moves(game_map, (x+1, y+1), excludeds):
        neighbors.append((x+1, y+1)) 
    # South-west
    if y + 1 < y_limit and x - 1 > 0 and allowed_moves(game_map, (x-1, y+1),  excludeds):
        neighbors.append((x-1, y+1)) 
     
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
        path.insert(0,target)
        target = parent[target]
    return path

def get_player_location(game_map: np.ndarray, symbol : str = "@") -> Tuple[int, int]:
    
    """
    :param game_map: the map of the game
    :param symbol: the symbol of the player
    
    :return: the position of the player as a tuple
    """
    
    x, y = np.where(game_map == ord(symbol))
    return (x[0], y[0])

def get_floor_positions(state):
    
    """
    :param state: the state of the game
    
    :return: the list of the floor positions
    """

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