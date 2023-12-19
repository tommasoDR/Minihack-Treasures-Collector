##### FILE PATH ####
import os

room_pattern_path = "/rooms_pattern/room{}.des"
object_file_path = "/objects_info.json"
results_directory = "/results"

project_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
room_pattern_path = project_folder_path + room_pattern_path
object_file_path = project_folder_path + object_file_path
results_directory = project_folder_path + results_directory


##### CONFIG VARIABLES #####
num_rooms = 3
num_patterns = 4
num_generations_spins = 2
probability_threshold = 0.95

##### CONSTANT SYMBOLS #####
all_walls = ["|", "-", "{"]
real_walls = ["|", "-"]
conditioning_symbol = "{"
