# Plots the unexplored cells in terms of the threshold values

from src.tests.utils import get_parser, plot_histogram
from src.explore_room import exhaustive_exploration
from src.generate_room import generate_env
import src.data as data

threshold_values = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

args = get_parser()

num_redo = args.num_redo
room_pattern = args.room_pattern

results = []

for threshold in threshold_values:
    data.probability_threshold = threshold
    print(data.probability_threshold)
    total = 0
    for redo in range(num_redo):
        env, goals_info = generate_env(room_pattern)
        guessed_room, unvisited_positions_percentage, _, _ = exhaustive_exploration(env.reset(), env)
        total += unvisited_positions_percentage

    total /= num_redo
    results.append(total)

title = "Room pattern {}, on {} runs".format(room_pattern, num_redo)
x_label = "Probability Threshold"
y_label = "Unexplored Cells (%)"
plot_histogram(threshold_values, results, x_label, y_label, title, "unexplored_cells", True)
