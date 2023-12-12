import random

from .utils import *
from .a_star import a_star
from .generate_room import generate_env, read_object_file
from IPython import display

# Trade-off between exploration and exploitation
PROB_NEAREST_UNVISITED = 1.0


def exhaustive_exploration(
        initial_state,
        environment
):
    """
    Performs an exhaustive search of the map, visiting all the floor positions.

    :param initial_state: the state of the game when starting the exploration
    :param environment: the environment of the game
    """

    clue_objects, goal_objects = read_object_file(object_file_path)
    probabilities_map = {}

    for obj in clue_objects:
        probabilities_map[obj[0]] = obj[4]

    obj_seen = {}

    room_probabilities = [1] * num_rooms

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
                color = ""
                if symbol in ["(", "*", "["]:
                    color = str(new_state['colors'][y][x])

                # print(symbol, color)

                obj = object_map.get((symbol, str(color)))

                if obj is not None:

                    # print(obj._class.name_)

                    # print(obj)

                    # Check if coordinates are already present in obj_seen dictionary
                    if (x, y) in obj_seen.keys():
                        # print("Coordinates already present in obj_seen dictionary")
                        continue

                        # Add coordinates to obj_seen dictionary
                    obj_seen[(x, y)] = obj

                    # print(obj_seen)

                    # Extract probabilities of the object
                    probabilities = probabilities_map.get(obj.to_string())
                    if probabilities is None:
                        continue

                    # print(obj.to_string())

                    # Multiply the probabilities of the object (each referred to the respective room) with each of
                    # the probabilities relating to the rooms
                    for i in range(len(room_probabilities)):
                        room_probabilities[i] *= probabilities[i]

                    # Normalize the probabilities
                    multiplier = 1 / sum(room_probabilities)
                    # print("Multiplier: " + str(multiplier))
                    normalized_probabilities = [multiplier * p for p in room_probabilities]

                    #print("Normalized probabilities: " + str(normalized_probabilities))

                    # If the probability of a room is greater than 0.95, then the target is the exit of that room
                    for i in range(len(normalized_probabilities)):
                        if normalized_probabilities[i] >= 0.95:
                            #print("We are in room " + str(i))
                            return i
            image.set_data(new_state['pixel'][:, 410:840])
            # display.display(plt.gcf())
            # display.clear_output(wait=True)

        # next loop I'll start from where I arrived
        starting_position = target

    return normalized_probabilities.index(max(normalized_probabilities))    


# To run: python3 -m src.explore_room
if __name__ == "__main__":
    win = 0
    for i in range(100):
        env, goals_info = generate_env()
        state = env.reset()
        #print_level(state)
        #print(goals_info)
        i = exhaustive_exploration(state, env)

        if goals_info[i][3] == 'uncursed':
            win+=1
    
    print(win)