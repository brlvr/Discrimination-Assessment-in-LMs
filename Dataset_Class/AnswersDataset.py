import jsonlines
from collections import Counter
import re
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

class AnswersDataset:

    def __init__(self, data, model_name):
        if isinstance(data, str):  # If data is a file path
            with jsonlines.open(data, 'r') as reader:
                line_dicts = [line for line in reader]
            self.dataset = pd.DataFrame(line_dicts)
        elif isinstance(data, pd.DataFrame):  # If data is already a DataFrame
            self.dataset = data
        else:
            raise ValueError("Input data must be a file path or a DataFrame")
        self.model_name = model_name
    
    def print_and_sample_df(self, n: int) -> pd.DataFrame:
        print(30*'#' + f'\n DataFrame Shape => {self.dataset.shape} \n' + 30*'#')
        if len(self.dataset) < n:
            n = len(self.dataset)

        return self.dataset.sample(n=n)
    
    def CutAnswers (self, AnswerLen: str):
        self.dataset[self.model_name] = self.dataset[self.model_name].apply(lambda x: x[:10])
    
    def Get_Yes_No_Answers(self,row: str):
        row_split = row.split()
        row_as_Series = pd.Series(row_split)

        yes_pattern = r'\b(?:' + re.escape('yes') + r')\b'
        no_pattern = r'\b(?:' + re.escape('no') + r')\b'
        yes_count = row_as_Series.str.count(yes_pattern, flags=re.IGNORECASE).sum()
        no_count = row_as_Series.str.count(no_pattern, flags=re.IGNORECASE).sum()
        if (yes_count ==1 and no_count==0):
            return 'Yes'
        elif (yes_count ==0 and no_count==1):
            return 'No'
        else:
            return 'None'
        print ('done here')
        
    def BinaryAnswers(self):
        #self.dataset[self.model_name] = (self.dataset[self.model_name].apply(lambda x: pd.Series(x))).apply(lambda x: x.apply(self.Get_Yes_No_Answers))
        #self.dataset[self.model_name].apply(lambda x: print(type(x)))
        #self.dataset[self.model_name] = self.dataset[self.model_name].apply(lambda x: x.apply(self.Get_Yes_No_Ansers))
        self.dataset['BinaryAnswer'] = self.dataset[self.model_name].apply(lambda x: self.Get_Yes_No_Answers(x))
        # regex_yes = r'\b(?:yes)\b'
        # regex_no = r'\b(?:no)\b'
        # print (type(self.dataset[self.model_name]))
        # # Replace "yes" with 1 and "no" with 0
        # self.dataset[self.model_name] = self.dataset[self.model_name].str.contains(regex_yes, case=False).astype(int).replace({True: 1, False: 0})
        # self.dataset[self.model_name] = self.dataset[self.model_name].str.contains(regex_no, case=False).astype(int).replace({True: 0, False: 1})

    def printNoneAnswers(self,n=5):
        NoneAnswersIdx = self.dataset['BinaryAnswer']=='None'
        if NoneAnswersIdx.any():
            return self.dataset[NoneAnswersIdx].sample(n=n)
        else:
            print ("There are 0 'None' Answers.")
        

    
    def ValidateAnswers(self):
        yes_count = self.dataset['BinaryAnswer'].astype(str).str.count('Yes').sum()
        no_count = self.dataset['BinaryAnswer'].astype(str).str.count('No').sum()
        none_count = self.dataset['BinaryAnswer'].astype(str).str.count('None').sum()
        print (f"There are {yes_count} Yes answers, {no_count} No answers and {none_count} None answers.")
        

        