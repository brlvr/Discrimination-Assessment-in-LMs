import jsonlines
from collections import Counter
import re
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd

from eda_main import count_lines

def read_dataset (file_path: str,num_lines: int = 0) -> pd.DataFrame:
    """
    This function gets path to dataset, reads it and returns a dataframe.
    num_lines is the amount of lines you want to read.
    """
    max_lines = count_lines(file_path)
    num_lines = 0 if num_lines < -1 else max_lines if num_lines > max_lines or num_lines == -1 else num_lines
    with jsonlines.open(file_path, 'r') as reader:
        for line_num, line in tqdm(enumerate(reader)):
            if line_num == num_lines:
                break
            if line_num==0:
                keys = list(line.keys())
                dataset = pd.DataFrame(columns=keys)
            dataset.loc[len(dataset)] = line
    return dataset    


def PlotCharactersHistogram(dataset: pd.DataFrame):
    """
    This function gets a dataset, and plots hisotgram of its characters counts per template.
    """
    CharactersHistogram = dataset['filled_template'].str.len()
    plt.hist(CharactersHistogram, bins=100, color='skyblue', edgecolor='black')
    plt.xlabel('Number of Characters')
    plt.ylabel('Frequency')
    plt.title('Prompts number of characaters histogram')
    
    y_min, y_max = plt.ylim()
    #plt.xlim(0,100)
    plt.ylim(0, y_max)
    plt.show()


def FeaturesHistogram(dataset: pd.DataFrame):
    """
    This function gets a dataset and runs over it columns to make histogram for feature (without "filled_template").
    """
    column_names = dataset.columns.tolist()[1:] #Remove first element "filled_template", already made histogram for it.
    for col in column_names:
        column_data = dataset[col] 
        plt.hist(column_data, bins=20, color='skyblue', edgecolor='black')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.title('Histogram of {}'.format(col))
        plt.show()  

def CreateRaceTemplate(dataset: pd.DataFrame):
    

def main():
    print ("Ron EDA...")
    dataset = read_dataset(file_path=".\discrim-eval\explicit.jsonl", num_lines=-1)
    #PlotCharactersHistogram(dataset)
    #FeaturesHistogram(dataset)

if __name__ == "__main__":
    main()