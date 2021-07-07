import csv
import os
from .constants import FieldTypes as FT
import pandas as pd

class surveyModel:

    def __init__(self):
        # HARDCODED, CHANGE LATER!
        self.raw_data = pd.read_excel("C:/Users/Tiny/ IA-Tool-V1/data/method_fragments/master_list.xlsx")
        self.dataframe = pd.DataFrame(self.raw_data)

    def show_relevant_fragments(self, df, item, target):

        # print('Checked item: ',item)

        test_values = df.loc[(df['category'] == item) & (df['target'] == target)]
        test_value_question = test_values['survey_input'].tolist()

        # print('Test Values: ',test_values)

        return test_value_question



