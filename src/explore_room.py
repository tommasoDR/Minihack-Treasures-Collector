import random
from utils import *
from a_star import a_star
from generate_room import generate_env
from IPython import display

# Trade-off between exploration and exploitation
PROB_NEAREST_UNVISITED = 0.7


def exhaustive_exploration(
        initial_state,
        environment
):
    """
    Performs an exhaustive search of the map, visiting all the floor positions

    :param initial_state: the state of the game when starting the exploration
    :param environment: the environment of the game
    """
    game_map = initial_state['chars']
    starting_position = get_player_location(game_map)
    floor_positions = get_floor_positions(state)
    game = initial_state['pixel']

    while floor_positions:

        # obtain floor visited (the neighbors of start)
        neighborhood = floor_visited([starting_position])

        # delete floor visited
        floor_positions = list(filter(lambda x: x not in neighborhood, floor_positions))

        if not floor_positions:
            break

        # generate a random number between 0 and 1
        p = random.uniform(0, 1)
        if p <= PROB_NEAREST_UNVISITED:
            # nearest unvisited floor location target
            target = min(floor_positions, key=lambda x: euclidean_distance(starting_position, x))
        else:
            # random target
            target = random.choice(floor_positions)

        # path with A* to the target location
        path = a_star(game_map, starting_position, target, [])

        # delete floors visited with the path
        neighborhood = floor_visited(path)
        floor_positions = list(filter(lambda x: x not in neighborhood, floor_positions))

        actions = actions_from_path(path)

        image = plt.imshow(game[:, 410:840])
        for action in actions:
            new_state, _, _, _ = environment.step(action)
            image.set_data(new_state['pixel'][:, 410:840])
            display.display(plt.gcf())
            display.clear_output(wait=True)

        # next loop I'll start from where I arrived
        starting_position = target


if __name__ == "__main__":
    env = generate_env()
    state = env.reset()

    exhaustive_exploration(state, env)
