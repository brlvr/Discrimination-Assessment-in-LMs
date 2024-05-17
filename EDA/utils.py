# Imports
import jsonlines
from collections import Counter
import re
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import nltk
from nltk.data import find

# Add local nltk_data directory to NLTK data path
nltk.data.path.append('./nltk_data')

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

# Ensure necessary NLTK data files are downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger')
    nltk.data.find('chunkers/maxent_ne_chunker')
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('punkt', download_dir='./nltk_data')
    nltk.download('averaged_perceptron_tagger', download_dir='./nltk_data')
    nltk.download('maxent_ne_chunker', download_dir='./nltk_data')
    nltk.download('words', download_dir='./nltk_data')

# Global Constants or Configuration

def count_lines(file_path: str) -> int:
    with open(file_path, 'r', encoding='utf8') as f:
        num_lines = sum(1 for line in f)
    return num_lines


def count_appearances_in_texts(texts_df: pd.DataFrame, words: list[str], type: str) -> pd.DataFrame:
    output_df = pd.DataFrame()
    output_df[texts_df.name] = texts_df
    for word in words:
        if type == 'gender':
            pattern = r'\b(?:' + re.escape(word) + r')\b'
        elif type == 'race':
            pattern = r'\b\w*\s*' + re.escape(word) + r'\s*\w*\b'
        elif type == 'age':
            pattern = fr'\b\w*\s*' + re.escape(word) + r'(?:-|\s)*(?:year|years)(?:-|\s)*old\s*\w*\b' 
        else:
            pattern = r'\b(?:' + re.escape(word) + r')\b'


        output_df[word] = texts_df.str.count(pattern, flags=re.IGNORECASE)

    return output_df


def get_unique_ages(text: str, pattern: str=r'(\d+)-year-old') -> np.ndarray:
    ages = set()
    matches = re.findall(pattern, text, re.IGNORECASE)
    ages.update(matches)

    return np.array(sorted([int(unique) for unique in ages]))


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


def read_jsonl(file_path: str) -> pd.DataFrame:
    with jsonlines.open(file_path, 'r') as reader:
        line_dicts = [line for line in reader]
    df_final = pd.DataFrame(line_dicts)

    return df_final


def print_and_sample_df(df: pd.DataFrame, n: int) -> pd.DataFrame:
    print(30*'#' + f'\n DataFrame Shape => {df.shape} \n' + 30*'#')
    if len(df) < n:
        n = len(df)

    return df.sample(n=n)


def plot_df_hist(df: pd.DataFrame):
    decision_question_id_counts = df['decision_question_id'].value_counts()

    decision_question_id_counts = decision_question_id_counts.sort_index()
    decision_question_id_counts.plot(kind='bar', figsize=(20,5), xlabel=f'Decision question ID [{len(decision_question_id_counts)}]', ylabel='count', title='Histogram of decision question IDs')

    plt.yticks(range(0, decision_question_id_counts.max() + 1, decision_question_id_counts.max()))
    plt.show()
    return


def string_length_anomalies(df: pd.DataFrame, min_str_len: int)->pd.DataFrame:
    filtered_indices = df.index[df['filled_template'].str.split().apply(len) < min_str_len]
    filtered_values = df.loc[filtered_indices, 'filled_template'].str.split().apply(len)
    filtered_examples = df.loc[filtered_indices, 'filled_template']

    result_df = pd.DataFrame({'Decision question ID': filtered_indices,
                            'Number of Words': filtered_values,
                            'filled_template': filtered_examples})
    return result_df


def find_names_from_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    person_names_list = []
    for index, row in df.iterrows():
        sentence = row["filled_template"]
        person_names = find_names(sentence)
        person_names_list.append(person_names)
    df['person_names'] = person_names_list    
    return df

def find_names(sentence: str):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    named_entities = ne_chunk(tagged)
    person_names = []
    for entity in named_entities:
        if isinstance(entity, nltk.tree.Tree) and entity.label() == 'PERSON':
            person_names.append(' '.join([leaf[0] for leaf in entity]))
    
    return person_names

def extract_full_name(names_list):
    names = []
    for name in names_list:
        if ' ' in name:  # Assuming full name has a space in it
            names.append(name)
    names = set(names)
    #if not names:
    #    names = set(names_list)
    return list(names)  # Return the full list if full name doesn't exist

#def replace_name ():

