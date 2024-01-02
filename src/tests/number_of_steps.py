from src.tests.utils import get_parser, plot_histogram
from src.explore_room import exhaustive_exploration
from src.generate_room import generate_env
from src.utils import manhattan_distance, euclidean_distance, TFFFM_distance, diagonal_distance
import src.data as data


args = get_parser()

num_redo = args.num_redo
room_pattern = args.room_pattern

distances = [
    manhattan_distance,
    TFFFM_distance,
]

map_conditioning = [False, True]

results = []

data.probability_threshold = 1

for conditioning in map_conditioning:

    for distance in distances:

        total = 0

        for redo in range(num_redo):
            env, goals_info = generate_env(room_pattern)
            guessed_room, _, steps, _ = exhaustive_exploration(env.reset(), env, distance, optimization=conditioning)
            total += steps

        total /= num_redo
        results.append(total)

title = "Room pattern {} on {} runs".format(room_pattern, num_redo)
x_label = "Distance"
y_label = "Number of Steps"
metrics = [
    "Manhattan \nwithout conditioning",
    "TFFFM \nwithout conditioning",
    "Manhattan \nwith conditioning",
    "TFFFM \nwith conditioning",
]

plot_histogram(metrics, results, x_label, y_label, title, "number_of_steps", True, False)
