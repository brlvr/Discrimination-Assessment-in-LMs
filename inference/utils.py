import json
import pandas as pd
import jsonlines
import os


def read_jsonl(file_path: str) -> pd.DataFrame:
    with jsonlines.open(file_path, 'r') as reader:
        line_dicts = [line for line in reader]
    df_final = pd.DataFrame(line_dicts)

    return df_final


def read_config_file(config_file_path):
    with open(config_file_path, 'r') as file:
        config = json.load(file)
    return config


def find_main_folder(current_dir, target_folder_name):
    # Check if the current directory contains the target folder
    if target_folder_name in os.listdir(current_dir):
        return current_dir
    # If not, go up one level
    parent_dir = os.path.dirname(current_dir)
    # Base case: If the parent directory is the root directory ('/'), return None
    if parent_dir == current_dir:
        return None
    # Recursive case: Continue searching in the parent directory
    return find_main_folder(parent_dir, target_folder_name)


def set_main_folder_path():
    # Get the path of the current script
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    # Find the main folder by recursively navigating upwards until 'main_folder' is found
    main_folder_path = find_main_folder(current_script_path, 'Discrimination-Assessment-in-LMs')
    print(main_folder_path)
    if main_folder_path is None:
        print("Main folder 'Discrimination-Assessment-in-LMs' not found.")
        return
    os.chdir(main_folder_path + f'\\Discrimination-Assessment-in-LMs')
    print('Working directory changed to: Discrimination-Assessment-in-LMs')
    return