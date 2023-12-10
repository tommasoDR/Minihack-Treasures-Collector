import random

from pyswip import Prolog

from .utils import *
from .a_star import a_star
from .generate_room import generate_env, read_object_file
from IPython import display

# Trade-off between exploration and exploitation
PROB_NEAREST_UNVISITED = 1.0

# KB = Prolog()

clue_objects, goal_objects = read_object_file(object_file_path)
probabilities_map = {}

for obj in clue_objects:
    probabilities_map[obj[0]] = obj[3]


def exhaustive_exploration(
        initial_state,
        environment
):
    """
    Performs an exhaustive search of the map, visiting all the floor positions.

    :param initial_state: the state of the game when starting the exploration
    :param environment: the environment of the game
    """

    game_map = initial_state['chars']
    starting_position = get_player_location(game_map)

    # map with fake walls
    conditioned_map = precondition_game_map(game_map)
    # print_chars_level(conditioned_map)

    # I consider imaginary walls as places to visit (use game_map)
    floor_positions = get_floor_positions(game_map)
    # print_chars_level(game_map)

    # obtain floor visited (the neighbors of start)
    neighborhood = get_neighbors([starting_position])

    # delete floor visited
    floor_positions = list(filter(lambda position: position not in neighborhood, floor_positions))

    room_type = -1

    while floor_positions:

        # generate a random number between 0 and 1
        p = random.uniform(0, 1)
        if p <= PROB_NEAREST_UNVISITED:
            # nearest unvisited floor location target
            target = min(floor_positions, key=lambda position: TFFFM_distance(game_map, starting_position, position))
        else:
            # random target
            target = random.choice(floor_positions)

        x, y = target

        # target is a fake wall?
        symbol = chr(conditioned_map[y][x])

        # the target is the fake wall
        if symbol == '{':
            # the target is the closest walkable point to the fake wall target
            target = closest_wall_target(target, conditioned_map)

        # path with A* to the target location
        path = a_star(conditioned_map, starting_position, target, [])

        # delete floors visited with the path
        neighborhood = get_neighbors(path)

        # update explored floor positions (delete floor positions visited)
        floor_positions = list(filter(lambda position: position not in neighborhood, floor_positions))

        actions = actions_from_path(path)

        image = plt.imshow(initial_state["pixel"][:, 410:840])
        for action in actions:

            # take a step
            new_state, _, _, _ = environment.step(action)

            # get the new position of the player and its neighborhood
            player_location = get_player_location(new_state['chars'])
            neighborhood = get_neighbors([player_location])

            for pos in neighborhood:

                x, y = pos
                symbol = chr(new_state['chars'][y][x])

                if symbol in ["(", "*"]:
                    symbol = new_state['colors'][y][x]
                elif symbol == "?":
                    pass

                clue_object = object_map.get(symbol)

                if clue_object is not None:

                    """
                    # probabilities = probabilities_map.get(clue_object.to_string())
                    print(probabilities)

                    # call prolog
                    KB.assertz(f"clue_object({str(clue_object)}, {str(pos)}, {str(probabilities)})")
                    room_type = KB.query("room_type(Room_type)")["Room_type"]
                    target_coordinates = KB.query("target_coordinates(Room_type)")["Room_type"]
                    if room_type != -1:
                        # target = get_room_target(room_type, game_map)
                        # return exit_room(new_state, environment, target)
                        # print(game_object)
                        pass
                    """

            image.set_data(new_state['pixel'][:, 410:840])
            display.display(plt.gcf())
            display.clear_output(wait=True)

        # next loop I'll start from where I arrived
        starting_position = target


# To run: python3 -m src.explore_room
if __name__ == "__main__":
    env = generate_env()
    state = env.reset()

    exhaustive_exploration(state, env)
