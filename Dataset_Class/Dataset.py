import jsonlines
from collections import Counter
import re
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from EDA.utils import find_names,string_length_anomalies, count_appearances_in_texts


class Dataset:

    def __init__(self, data):
        if isinstance(data, str):  # If data is a file path
            with jsonlines.open(data, 'r') as reader:
                line_dicts = [line for line in reader]
            self.dataset = pd.DataFrame(line_dicts)
        elif isinstance(data, pd.DataFrame):  # If data is already a DataFrame
            self.dataset = data
        else:
            raise ValueError("Input data must be a file path or a DataFrame")
        
        self.unique_genders = self.dataset['gender'].unique()
        self.unique_races = self.dataset['race'].unique()
        self.unique_ages = self.dataset['age'].unique()
        self.unique_ages = [str(int(age)) for age in self.unique_ages]

    def print_distinct_parameters(self):
        print(f'''
        Gender: {self.unique_genders}
        Races: {self.unique_races}
        Ages: {self.unique_ages}
        ''')    
        
    def print_and_sample_df(self, n: int) -> pd.DataFrame:
        print(30*'#' + f'\n DataFrame Shape => {self.dataset.shape} \n' + 30*'#')
        if len(self.dataset) < n:
            n = len(self.dataset)

        return self.dataset.sample(n=n)

    def plot_df_hist(self):
        decision_question_id_counts = self.dataset['decision_question_id'].value_counts()

        decision_question_id_counts = decision_question_id_counts.sort_index()
        decision_question_id_counts.plot(kind='bar', figsize=(20,5), xlabel=f'Decision question ID [{len(decision_question_id_counts)}]', ylabel='count', title='Histogram of decision question IDs')

        plt.yticks(range(0, decision_question_id_counts.max() + 1, decision_question_id_counts.max()))
        plt.show()
        return
    
    def plot_name_histogram (self):
        name_counts = self.dataset['name'].value_counts()

        # Plot the histogram
        plt.figure(figsize=(10, 6))
        name_counts.plot(kind='bar')
        plt.title('Histogram of Names')
        plt.xlabel('Name')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.show()
    
    def gender_validty(self):
        return count_appearances_in_texts(texts_df=self.dataset['filled_template'], words=self.unique_genders, type='gender')

    def race_validity(self):
        return count_appearances_in_texts(texts_df=self.dataset['filled_template'], words=self.unique_races, type='race')

    def age_validity (self):
        return count_appearances_in_texts(texts_df=self.dataset['filled_template'], words=self.unique_ages, type='age')

    def long_sentences_check (self, n = 350):
        implicit_filtered_indices = self.dataset.index[self.dataset['filled_template'].str.split().apply(len) > n]
        implicit_filtered_values = self.dataset.loc[implicit_filtered_indices, 'filled_template'].str.split().apply(len)
        implicit_filtered_examples = self.dataset.loc[implicit_filtered_indices, 'filled_template']
        return pd.DataFrame({'Decision question ID': implicit_filtered_indices,
                          'Number of Words': implicit_filtered_values,
                          'filled_template': implicit_filtered_examples})

    def questions_length (self,title: str, min_str_len = 25 ):
        self.dataset['filled_template'].str.split().apply(len).plot(title=title,figsize=(20,5), xticks=range(0,len(self.dataset)+1, 135*5), xlabel='decision question sample', ylabel='num of characters')
        anomaly_df = string_length_anomalies(df=self.dataset, min_str_len=min_str_len)
        return anomaly_df

    def find_names_from_dataframe(self) -> pd.DataFrame:
        person_names_list = []
        for index, row in self.dataset.iterrows():
            sentence = row["filled_template"]
            person_names = find_names(sentence)
            person_names_list.append(person_names)
        self.dataset_with_names['person_names'] = person_names_list    
        return self.dataset_with_names

