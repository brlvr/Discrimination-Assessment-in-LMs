import os
from  dotenv import load_dotenv
import requests
import json
from utils import read_jsonl, read_config_file, set_main_folder_path, validate_rate_limiter, write_jsonl
from tqdm import tqdm
import anthropic


load_dotenv()

def hf_request(data: str) -> json:
    payload = {"inputs": f'{data}'}
    headers = {"Authorization": os.environ.get("LLAMA3_AUTH")}
    response = requests.post(os.environ.get("LLAMA3_URL"), headers=headers, json=payload)
    print(response.json())
    return response.json()

def claude_request(data: str):
    client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ.get("CLAUDE-2.0_API_KEY"),
    )
    message = client.messages.create(
        model="claude-2.0",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": data
                    }
                ]
            }
        ]
    )
    validate_rate_limiter(message)

    # Decode the bytes object to a string
    message_string = message.content.decode('utf-8')
    # Parse the string into a JSON object
    message_data = json.loads(message_string)
    return message_data


def inference():
    print("Starting inference pipeline...")
    set_main_folder_path()
    try:
        config = read_config_file(config_file_path="inference\\config.json")
        model_name = config["model_name"].lower()
        dataset_path = config["dataset_path"]
        dataset_name = os.path.splitext(os.path.basename(dataset_path))[0]
        output_path = f'outputs/{model_name}/{model_name}_{dataset_name}_decisions.jsonl'

        if os.path.exists(output_path):
            dataset_path = output_path
        else:
            dataset_path = config["dataset_path"]

        dataset = read_jsonl(file_path=dataset_path)

    except Exception as e:
        print("Error at Configuration stage",e)
        return


    try:
        with open(f'inference\\prompts\\{model_name}_prompt.txt', 'r') as file:
            prompt = file.read()

    except Exception as e:
        print("Error at prompt stage",e)
        return
    

    for index, row in tqdm(dataset.iterrows(), total=len(dataset), desc="Processing Rows"):
    # Extract data from the specified column
        filled_template = row["filled_template"]
        prompt = prompt.format(filled_template=filled_template)
        # Call the API with the data
        
        if model_name.lower() == "llama3":
            api_result = hf_request(data=prompt)
            generated_text = api_result[0]["generated_text"]

        elif model_name.lower() == "claude-2.0":
            api_result = claude_request(data=prompt)
            generated_text = api_result["content"][0]["text"]

        else:
            print("Model name is not supported")
            return
        

        # Add the API result as a new column to the DataFrame
        dataset.loc[index, f"{model_name}"] = generated_text

        if index%1000 == 0:
            write_jsonl(df=dataset, file_path=output_path)

    write_jsonl(df=dataset, file_path=output_path)
# Conditional Execution
if __name__ == "__main__":
    
    inference()
