import os
from  dotenv import load_dotenv
import requests
import json
from utils import read_jsonl, read_config_file, set_main_folder_path
from tqdm import tqdm


load_dotenv()

def hf_request(data: dict) -> json:
    payload = {"inputs": f'{data}'}
    headers = {"Authorization": os.environ.get("LLAMA3_AUTH")}
    response = requests.post(os.environ.get("LLAMA3_URL"), headers=headers, json=payload)
    print(response.json())
    return response.json()


def inference():
    print("Starting inference pipeline...")
    set_main_folder_path()

    config = read_config_file(config_file_path="inference\\config.json")
    model_name = config["model_name"].lower()
    dataset_path = config["dataset_path"]
    
    dataset = read_jsonl(file_path=dataset_path)

    with open(f'inference\\prompts\\{model_name}_prompt.txt', 'r') as file:
        prompt = file.read()
    

    for index, row in tqdm(dataset.iterrows(), total=len(dataset), desc="Processing Rows"):
    # Extract data from the specified column
        filled_template = row["filled_template"]
        prompt = prompt.format(filled_template=filled_template)
        # Call the API with the data
        payload = {}
        if model_name.lower() == "llama3":
            api_result = hf_request(data=prompt)
            generated_text = api_result[0]["generated_text"]
        
        # Add the API result as a new column to the DataFrame
        dataset.loc[index, f"{model_name}"] = generated_text

        print(generated_text)

# Conditional Execution
if __name__ == "__main__":
    
    inference()
