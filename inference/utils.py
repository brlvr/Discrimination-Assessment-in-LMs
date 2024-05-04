import json
import pandas as pd
import jsonlines
import os
import time
from datetime import datetime, timezone
import pytz


def read_jsonl(file_path: str) -> pd.DataFrame:
    with jsonlines.open(file_path, 'r') as reader:
        line_dicts = [line for line in reader]
    df_final = pd.DataFrame(line_dicts)

    return df_final

def write_jsonl(df: pd.DataFrame, file_path: str):
    df_records = df.to_dict(orient='records')
    with open(file_path, 'w') as f:
        for entry in df_records:
            f.write(f"{json.dumps(entry)}\n")
    return


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


def validate_rate_limiter(response):
    remaining = int(response.headers['anthropic-ratelimit-requests-remaining'])
    reset_time = response.headers['anthropic-ratelimit-requests-reset']

    # If no more requests are allowed, wait until the reset time
    if remaining == 0:
        # Define your local timezone, e.g., Israel's timezone- the code depand on it!!
        local_timezone = pytz.timezone('Asia/Jerusalem')
        # Parse the reset time as a datetime object and paerse to local timezone
        reset_datetime = datetime.strptime(reset_time, '%Y-%m-%dT%H:%M:%SZ')
        reset_datetime = reset_datetime.replace(tzinfo=timezone.utc)
        reset_datetime = reset_datetime.astimezone(local_timezone)
        reset_datetime = reset_datetime.replace(tzinfo=None)
        # Get the current time in UTC make it in the same units 
        current_datetime = datetime.now()
        # Calculate the number of seconds to wait
        wait_seconds = (reset_datetime - current_datetime).total_seconds()

        # Add some extra delay to ensure the limit has been reset by the server
        wait_seconds += 7  # For example, wait an extra 7 seconds

        print(f"Rate limit reached. Waiting for {wait_seconds} seconds.")
        
        # Wait until the reset time
        time.sleep(wait_seconds)