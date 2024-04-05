# Imports
import jsonlines
from collections import Counter
import re
from tqdm import tqdm

# Global Constants or Configuration
DEBUG_MODE = False


def count_lines(file_path: str) -> int:
    with open(file_path, 'r') as f:
        num_lines = sum(1 for line in f)
    return num_lines

def count_apperences(decision_question:str, countfor: any) -> int:
    word_count = len(re.findall(r'\b' + re.escape(countfor) + r'\b', decision_question, re.IGNORECASE))
    return word_count



def read_jsonl(file_path: str, num_lines: int = 0):
    
    max_lines = count_lines(file_path)

    num_lines = 0 if num_lines < -1 else max_lines if num_lines > max_lines or num_lines == -1 else num_lines

    decision_question_id_counter = {}

    with jsonlines.open(file_path, 'r') as reader:
        for line_num, line in tqdm(enumerate(reader)):
            if line_num == num_lines:
                break

            # for each decision_question we want to see if it is complete in the sense of explicit age, gender and race.
            decision_question =line['filled_template']
            #print(f"\n\n Line number: {line_num}\n\n {line.keys()}")

            decision_question_id_counter[f"{line['decision_question_id']}"] = decision_question_id_counter.get(f"{line['decision_question_id']}", 0) + 1
            
            #check age

            #check gender
            gender = line['gender']
            gender_apperences = count_apperences(decision_question=line['filled_template'], countfor=line['gender'])
            if gender_apperences != 1:
                
                print(80*"*" + f"\n\nThe word '{gender}' appears {gender_apperences} times in the text:\n{decision_question}.\n\n" + 80*"*")
            #check race


        print(decision_question_id_counter)
    return

# Main Function or Entry Point
def main():
    print("Starting the program...")

    if DEBUG_MODE:
        print("Debug mode is enabled.")

    
    read_jsonl(file_path=".\discrim-eval\explicit.jsonl", num_lines=-1)
    # need to read each decision_question and check if any of the categories apeear once in each decision_question


# Conditional Execution
if __name__ == "__main__":
    
    main()