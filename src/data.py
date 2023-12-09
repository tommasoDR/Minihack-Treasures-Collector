##### FILE PATH ####
import os

room_pattern_path = "/rooms_pattern/room{}.des"
object_file_path = "/objects_info.json"

project_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
room_pattern_path = project_folder_path + room_pattern_path
object_file_path = project_folder_path + object_file_path


##### CONFIG VARIABLES #####
num_rooms = 3
num_patterns = 4
num_generations_spins = 2
