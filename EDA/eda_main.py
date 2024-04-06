# Imports
import jsonlines
from collections import Counter
import re
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd

# Global Constants or Configuration
DEBUG_MODE = False


def count_lines(file_path: str) -> int:
    with open(file_path, 'r', encoding='utf8') as f:
        num_lines = sum(1 for line in f)
    return num_lines

def count_apperences_in_text(text: str, words: list) -> list:
    word_count = []
    for word in words:
        word_count.append(len(re.findall(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE)))
    return word_count


def bar_plot(data: dict, title: str ="title", xlabel: str = "xlabel", ylabel: str = "ylabel"):
    # Extract keys and values from the dictionary
    labels = list(data.keys())
    values = list(data.values())

    # Plot the histogram
    plt.bar(labels, values)

    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    # Show the plot
    plt.show()
    return



def read_jsonl(file_path: str, num_lines: int = 0):
    
    max_lines = count_lines(file_path)

    num_lines = 0 if num_lines < -1 else max_lines if num_lines > max_lines or num_lines == -1 else num_lines

    
    decision_question_id_counter = {}
    genders = set()
    ages = list(range(20,81,10))
    races = set()

    print(ages)
    with jsonlines.open(file_path, 'r') as reader:
        for line_num, line in tqdm(enumerate(reader)):
            if line_num == num_lines:
                break
            
            
            decision_question_id_counter[f"{line['decision_question_id']}"] = decision_question_id_counter.get(f"{line['decision_question_id']}", 0) + 1
            genders.add(line['gender'])
            races.add(line['race'])


            #gender_apperences = count_apperences_in_text(text=line['filled_template'], countfor=list(genders))
            age_apperences= 1
            race_apperences = 1

            # for each decision_question we want to see if it is complete in the sense of explicit age, gender and race.
            decision_question =line['filled_template']
            #print(f"\n\n Line number: {line_num}\n\n {line.keys()}")
            
            #check age

            #check gender
            gender = line['gender']
            #genders_apperences = count_apperences_in_text(text=line['filled_template'], countfor=list(line['gender']))

        bar_plot(data=decision_question_id_counter, title="Histogram of Decision question ID", xlabel=f'Decision question ID ({len(decision_question_id_counter)})', ylabel='Frequency')
        print(genders)
        print(races)
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