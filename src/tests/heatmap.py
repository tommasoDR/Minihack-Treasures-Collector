import argparse
from matplotlib import pyplot as plt
from src.explore_room import exhaustive_exploration
from src.generate_room import generate_env
from src.utils import manhattan_distance, TFFFM_distance
from src.tests.utils import get_parser


args = get_parser()

num_redo = args.num_redo
room_pattern = args.room_pattern


distances = [
    manhattan_distance,
    TFFFM_distance
]

optimizations = [
    False,
    True
]

room_pattern = args.room_pattern

# Fix the room pattern
env, goals_info = generate_env(room_pattern)
env_reset = env.reset()

for distance, optimization in zip(distances, optimizations):

    guessed_room, _, _, heatmap = exhaustive_exploration(env.reset(), env, distance=distance, optimization=optimization)

    fig, ax = plt.subplots()

    # Plot the heatmap
    im = ax.imshow(heatmap[:, 25:51], cmap='gist_gray', interpolation='nearest', aspect='auto')
    plt.colorbar(im)

    # Remove x and y ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # plt.savefig(results_directory + f"/heatmap_{distance.__name__}_room{room_pattern}.pdf")

    plt.show()
