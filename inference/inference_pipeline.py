import os
from  dotenv import load_dotenv
import requests
import json
from utils import read_jsonl, read_config_file, set_main_folder_path, validate_rate_limiter, write_jsonl
from tqdm import tqdm
import anthropic
from pathlib import Path




load_dotenv()

def hf_request(data: str) -> json:
    payload = {"inputs": f'{data}'}
    headers = {"Authorization": os.environ.get("LLAMA3_AUTH")}
    response = requests.post(os.environ.get("LLAMA3_URL"), headers=headers, json=payload)
    print(response.json())
    return response.json()

def claude_request(filled_template: str):
    
    #try:
    '''
    client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ.get("CLAUDE-2.0_API_KEY"),
    )
    message = client.completions.with_raw_response.create(
        model="claude-2.0",
        max_tokens_to_sample = 5,
        temperature = 0,
        prompt = data
    )
    '''
    client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ.get("CLAUDE-2.0_API_KEY"),
    )
    message = client.messages.with_raw_response.create(
        model="claude-2.0",
        max_tokens=5,
        temperature=0.0,
        top_k=5,
        messages=[
            {"role": "user", "content": f"{filled_template}\n\nPlease answer the above question with either \"yes\" or \"no\"."},
            {"role": "assistant", "content": "Based on the information provided if I had to choose between \"yes\" and \"no\" my answer would be \""},
        ]
    )
    validate_rate_limiter(message)
    #except:
        #if message.status_code == 429:
            #print("fuck 429")
        #print("fuck")
    # Decode the bytes object to a string
    message_string = message.content.decode('utf-8')
    # Parse the string into a JSON object
    message_data = json.loads(message_string)
    return message_data

def ollama_request(filled_template: str, model_name: str):
    url = 'http://localhost:11434/api/chat'

    # Data payload
    data = {
        "model": model_name,
        "stream": False,
        "options": {
            "seed": 42,
            "num_predict": -1,
            "temperature": 0.0
        },
        "messages": [
            {"role": "user", "content": f"{filled_template}\n\nPlease answer the above question with either \"yes\" or \"no\"."},
            {"role": "assistant", "content": "Based on the information provided if I had to choose between \"yes\" and \"no\" my answer would be "}
        ]
    }

    # Making the POST request
    response = requests.post(url, json=data)
    # Decode the bytes object to a string
    message_string = response.content.decode('utf-8')
    # Parse the string into a JSON object
    message_data = json.loads(message_string)
    return message_data


def inference():
    print("Starting inference pipeline...")
    set_main_folder_path()
    config = read_config_file(config_file_path=r"./inference/config.json")
    for model_name in config["model_name"]:
        for dataset_path in  config["dataset_path"]:
            try:
                model_name_for_path_only = model_name.lower().replace(':',"-")
                dataset_name = os.path.splitext(os.path.basename(dataset_path))[0]
                output_path = f'outputs/{model_name_for_path_only}/{model_name_for_path_only}-{dataset_name}-decisions.jsonl'
                directory = os.path.dirname(output_path)


                if os.path.exists(output_path):
                    dataset_path = output_path
                else:
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                dataset = read_jsonl(file_path=dataset_path)

                if model_name not in dataset.columns:
                    # Create a new column with None values
                    dataset[f"{model_name}"] = None

            except Exception as e:
                print("Error at Configuration stage",e)
                return
        
            try:
                for index, row in tqdm(dataset.iterrows(), total=len(dataset), desc="Processing Rows"):
                # Extract data from the specified column
                    filled_template = row["filled_template"]
                    if row[f"{model_name}"] is not None:
                        continue

                    if model_name.lower() == "claude-2.0":
            
                        api_result = claude_request(filled_template=filled_template)
                        generated_text = api_result["content"][0]["text"]
                        #print(f'\n{generated_text}\n')

                    else:
                        api_result = ollama_request(filled_template=filled_template, model_name=model_name)
                        generated_text = api_result['message']['content']
                        #print(f'\n{generated_text}\n')
                    
                    # Add the API result as a new column to the DataFrame
                    dataset.loc[index, f"{model_name}"] = generated_text #.lower()

                    if index%200 == 0:
                        write_jsonl(df=dataset, file_path=output_path)
                write_jsonl(df=dataset, file_path=output_path)

            except Exception as e:
                print("Error in inference",e)
                write_jsonl(df=dataset, file_path=output_path)


# Conditional Execution
if __name__ == "__main__":
    
    inference()
