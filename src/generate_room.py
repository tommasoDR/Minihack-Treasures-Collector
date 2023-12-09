import gym
import minihack
import numpy as np
import sys
import json
from utils import *
from data import *


def read_des_file(des_file: str) -> str:
    """
    Reads the des file and returns the map

    :param des_file: the path of the des file
    :return: the map as a string
    """
    try:
        with open(des_file, 'r') as file:
            content = file.read()

        start_index = content.find('MAP')
        end_index = content.find('ENDMAP')

        if start_index != -1 and end_index != -1 and start_index < end_index:
            map_content = content[start_index + len('MAP'):end_index]
        else:
            raise Exception("MAP and ENDMAP not found in des file")
    except Exception as e:
        print("Error reading des file")
        print(str(e), file=sys.stderr)
        sys.exit(1)
    return map_content


def read_object_file(object_file) -> (list, list):
    """
    Reads the object file and returns the list of clue objects and goal objects

    :param object_file: the path of the object file
    :return: the list of clue objects and goal objects
    """
    try:
        with open(object_file, 'r') as file:
            json_content = json.loads(file.read())
            clue_objects = json_content["clue_objects"]
            goal_objects = json_content["goal_objects"]
    except Exception as e:
        print("Error reading object file")
        print(str(e), file=sys.stderr)
        sys.exit(1)
    return clue_objects, goal_objects


def random_room_type() -> int:
    """
    Returns a random room type

    :return: a random room type as an integer
    """
    return np.random.randint(0, num_rooms)


def random_pattern_file() -> str:
    """
    Returns a random pattern file path

    :return: a random pattern file path as a string
    """
    pattern = np.random.randint(1, num_patterns + 1)
    return room_pattern_path.format(pattern)


def add_goal_objects(levelgen, goal_objects, room_type):
    """
    Adds the goal objects to the level generator

    :param levelgen: the MiniHack level generator
    :param goal_objects: the list of goal objects
    :param room_type: the type of the room
    """
    if len(goal_objects) != num_rooms:
        print("Number of goal objects must be equal to number of rooms")
        sys.exit(1)
    curse_state = ["cursed" for i in range(len(goal_objects))]
    curse_state[room_type] = "uncursed"
    i = 0
    for (object_name, object_symbol) in goal_objects:
        levelgen.add_object(name=object_name, symbol=object_symbol, place=None, cursestate=curse_state[i])
        i += 1


def add_random_objects(levelgen, object_info, room_type):
    """
    Adds random objects to the level generator

    :param levelgen: the MiniHack level generator
    :param object_info: the list of objects
    :param room_type: the type of the room
    """
    for _ in range(num_generations_spins):
        np.random.shuffle(object_info)
        for i in range(len(object_info)):
            (object_name, object_symbol, _, spawn_probability) = object_info[i]
            p = np.random.uniform()
            if p <= spawn_probability[room_type]:
                levelgen.add_object(name=object_name, symbol=object_symbol, place=None, cursestate=None)


def generate_env():
    """
    Generates a random MiniHack environment, with goal objects and random objects.
    Objects are defined and taken from the object file.
    The room type is randomly chosen.
    The room pattern is randomly chosen.

    :return: the MiniHack environment (type: gym.Env)
    """
    room_pattern_file = random_pattern_file()
    levelgen = minihack.LevelGenerator(map=read_des_file(room_pattern_file), lit=True, flags=("premapped",))
    room_type = random_room_type()
    clue_objects, goal_objects = read_object_file(object_file_path)
    add_goal_objects(levelgen, goal_objects, room_type)
    add_random_objects(levelgen, clue_objects, room_type)
    env = gym.make("MiniHack-Skill-Custom-v0",
                   observation_keys=("screen_descriptions_crop", "chars", "colors", "pixel"), obs_crop_h=3,
                   obs_crop_w=3, max_episode_steps=10000, autopickup=False, des_file=levelgen.get_des())
    return env


# generate_env()
if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)
    env = generate_env()
    print_level(env.reset())
