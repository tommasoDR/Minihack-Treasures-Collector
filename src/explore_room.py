import random
from src.utils import *
from src.a_star import a_star
from src.generate_room import generate_env
from IPython import display

# Trade-off between exploration and exploitation
ALPHA = 0.9


def exhaustive_search(
        game_map: np.ndarray,
        starting_position: Location,
        floor_positions: List[Location],
        game,
        environment
):
    """
    Performs an exhaustive search of the map, visiting all the floor positions

    :param display:
    :param game_map: The map of the game
    :param start: The starting position of the agent
    :param floor_positions: The list of floor positions as a list of Location
    :param game:
    """

    print("Starting position: {}".format(starting_position))
    print("Number of floor positions: {}".format(len(floor_positions)))

    while floor_positions:

        # obtain floor visited (the neighbors of start)
        neighborhood = already_visited([starting_position])

        # delete floor visited
        floor_positions = list(filter(lambda x: x not in neighborhood, floor_positions))

        if not floor_positions:
            break

        # generate a random number between 0 and 1
        p = random.uniform(0, 1)
        if p <= ALPHA:
            # nearest unvisited floor location target
            target = min(floor_positions, key=lambda x: euclidean_distance(starting_position, x))
        else:
            # random target
            target = random.choice(floor_positions)

        # path with A* to the target location
        path = a_star(game_map, starting_position, target, [])

        # delete floors visited with the path
        floor_positions = list(filter(lambda x: x not in path, floor_positions))

        actions = actions_from_path(starting_position, path)
        image = plt.imshow(game[:, 410:840])
        for action in actions:
            s, _, _, _ = environment.step(action)
            display.display(plt.gcf())
            display.clear_output(wait=True)
            image.set_data(s['pixel'][:, 410:840])

        # next loop I'll start from where I arrived
        starting_position = target


if __name__ == "__main__":
    env = generate_env()
    state = env.reset()
    env.render()

    game_map = state['chars']
    start = get_player_location(game_map)
    floor = get_floor_positions(state)
    game = state['pixel']

    exhaustive_search(game_map, start, floor, game, env)
