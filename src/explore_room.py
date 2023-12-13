import random
from time import sleep

from .utils import *
from .a_star import a_star
from .generate_room import generate_env, read_object_file
from IPython import display

# Trade-off between exploration and exploitation
PROB_NEAREST_UNVISITED = 1.0


def exit_room(state, image, environment, target_coordinates: Location):
    """
    Exits the room, going to the target coordinates.

    :param state: the current state of the game
    :param environment: the environment of the game
    :param target_coordinates: the coordinates of the target
    :return: the index of the room that has been exited
    """
    # pause the program for two seconds
    #sleep(2)
    current_player_location = get_player_location(state['chars'])
    path = a_star(state['chars'], current_player_location, target_coordinates, [])
    actions = actions_from_path(path)
    for action in actions:
        state, _, _, _ = environment.step(action)
        image.set_data(state['pixel'][:, 410:840])
        #display.display(plt.gcf())
        display.clear_output(wait=True)


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
    normalized_probabilities = [1 / num_rooms] * num_rooms

    game_map = initial_state['chars']
    starting_position = get_player_location(game_map)

    # map with fake walls
    conditioned_map = precondition_game_map(game_map)

    # I consider imaginary walls as places to visit (use game_map)
    floor_positions = get_floor_positions(game_map)
    # print_chars_level(game_map)

    # obtain floor visited (the neighbors of start)
    neighborhood = get_neighbors([starting_position])

    # delete floor visited
    floor_positions = list(filter(lambda position: position not in neighborhood, floor_positions))

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
        if symbol == "{":
            # the target is the closest walkable point to the fake wall target
            target = closest_target_to_wall(target, conditioned_map)


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

                    # Check if coordinates are already present in obj_seen dictionary
                    if (x, y) in obj_seen.keys():
                        # print("Coordinates already present in obj_seen dictionary")
                        continue

                    # Add coordinates to obj_seen dictionary
                    obj_seen[(x, y)] = obj

                    # Extract probabilities of the object
                    probabilities = probabilities_map.get(obj.to_string())

                    # Found a goal object
                    if probabilities is None:
                        continue

                    # Multiply the probabilities of the object (each referred to the respective room) with each of
                    # the probabilities relating to the rooms
                    for i in range(len(room_probabilities)):
                        room_probabilities[i] *= probabilities[i]

                    # Normalize the probabilities
                    multiplier = 1 / sum(room_probabilities)

                    # print("Multiplier: " + str(multiplier))
                    normalized_probabilities = [multiplier * p for p in room_probabilities]

                    # If the probability of a room is greater than 0.95, then the target is the exit of that room
                    for room in range(len(normalized_probabilities)):

                        if normalized_probabilities[room] >= 0.95:

                            object_name = GoalObject.from_string(goal_objects[room][0])
                            # check if target_room is in values of the obj_seen dictionary
                            if object_name not in obj_seen.values():
                                break

                            # get coordinates of the target room
                            target_coordinates = list(obj_seen.keys())[list(obj_seen.values()).index(object_name)]

                            # print("Object: " + target_room.name + ", Target coordinates: " + str(target_coordinates))
                            exit_room(new_state, image, environment, target_coordinates)
                            return room

            image.set_data(new_state['pixel'][:, 410:840])
            #display.display(plt.gcf())
            display.clear_output(wait=True)

        # next loop I'll start from where I arrived
        starting_position = target

    # print(obj_seen, floor_positions)
    guessed_room = normalized_probabilities.index(max(normalized_probabilities))
    object_name = GoalObject.from_string(goal_objects[guessed_room][0])
    if object_name not in obj_seen.values():
        print("The target object is not in the room..., the missing object is: " + object_name.name)
        return guessed_room
    target_coordinates = list(obj_seen.keys())[list(obj_seen.values()).index(object_name)]

    # print("Object: " + target_room.name + ", Target coordinates: " + str(target_coordinates))
    exit_room(new_state, image, environment, target_coordinates)
    return guessed_room


# To run: python3 -m src.explore_room
if __name__ == "__main__":
    win = 0
    num_redo = 250
    for _ in range(num_redo):
        env, goals_info = generate_env()
        state = env.reset()
        # print_level(state)
        # print(goals_info)
        i = exhaustive_exploration(state, env)

        if goals_info[i][3] == 'uncursed':
            win += 1

    print(win, num_redo)