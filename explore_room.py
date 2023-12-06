
import gym
import minihack
import random
from utils import *
from generate_room import generate_env


def exhaustive_search(game_map: np.ndarray, start: Tuple[int, int], floor_positions: [], game):
    
    target = (0,0)

    while True:

        # all floor floor has been visited
        if not floor_positions:
            print(floor_positions)
            return 

        # obtain floor visited (the neighbors of start)
        already_visited_arr = already_visited([start])

        # delete floor visited 
        for point in already_visited_arr:
            if point in floor_positions:
                floor_positions.remove(point)

        randoom_number = random.randint(1, 10)
        if (1 <= randoom_number <= 7): 
            # near floor target 
            min = float('inf')
            for point in floor_positions:
                if (euclidean_distance(start, point) < min): 
                    target = point
                    min = euclidean_distance(start, point)
        else:
            # randoom target 
            target = random.choice(floor_positions)

        # path with A*
        path = a_star(game_map, start, target, manhattan_distance)
        # delete floor visited with path 
        for point in already_visited(path):
            if point in floor_positions:
                floor_positions.remove(point)

        # MOVIMENTO DA IMPLEMENTARE, non funziona :(
        #actions = actions_from_path(start,path)
        #image = plt.imshow(game[25:300, :475])
        #for action in actions:
        #    s, _, _, _ = env.step(action)
        #    display.display(plt.gcf())
        #    display.clear_output(wait=True)
        #    image.set_data(s['pixel'][25:300, :475])

        # neext loop I'll start from where I arrived
        start = target
        

env = generate_env()
state = env.reset()
env.render()

game_map = state['chars']
start = get_player_location(game_map)
floor_positions = get_floor_positions(state)
game = state['pixel']

# gli passo game perchè serve per vedere i movimenti (?)
exhaustive_search(game_map, start, floor_positions, game)



