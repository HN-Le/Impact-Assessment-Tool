
import os
import pandas as pd


class importCoreData():

    # populate from csv file
    dirname = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    filename = os.path.join(dirname, 'method_fragments', 'master_list.xlsx')

    raw_data = pd.read_excel(filename)
    dataframe = pd.DataFrame(raw_data)

    # metric_id
    # metric_name
    # method_fragment_id
    # metric_definition
    # metric_question
    # metric_value_type

    # method_fragment_id
    # method_fragment_name

