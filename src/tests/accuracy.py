from src.explore_room import exhaustive_exploration
from src.generate_room import generate_env
from src.tests.utils import get_parser

args = get_parser()

num_redo = args.num_redo
room_pattern = args.room_pattern

win = 0
for redo in range(num_redo):
    env, goals_info = generate_env(room_pattern)
    state = env.reset()
    i, _, _, _ = exhaustive_exploration(state, env)

    if goals_info[i][3] == 'uncursed':
        win += 1

print("Win rate: ", win/num_redo)
