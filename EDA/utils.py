# Imports
import jsonlines
from collections import Counter
import re
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Global Constants or Configuration

def count_lines(file_path: str) -> int:
    with open(file_path, 'r', encoding='utf8') as f:
        num_lines = sum(1 for line in f)
    return num_lines


def count_apperances_in_texts(texts_df: pd.DataFrame, words: list[str]) -> pd.DataFrame:
    output_df = pd.DataFrame(texts_df, texts_df.name)

    for word in words:
        pattern = r'\b' + re.escape(word) + r'\b'
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