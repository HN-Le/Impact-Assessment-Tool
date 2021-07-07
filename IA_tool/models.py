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

        relevant_categories = df.loc[(df['category'] == item) & (df['target'] == target)]
        relevant_survey_inputs = relevant_categories['survey_input']
        relevant_metrics = relevant_categories['metric']
        relevant_type = relevant_categories['type']

        list_items = [relevant_survey_inputs, relevant_metrics, relevant_type]

        return list_items





