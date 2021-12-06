import os

# data types used
class FieldTypes:
    string = 1
    string_list = 2
    iso_date_string = 3
    long_string = 4
    decimal = 5
    integer = 6
    boolean = 7

class PdfFiles:
    dirname = os.getcwd()

    project_goals = os.path.join(dirname, 'docs', '1.1 - Project Goals.pdf')
    goal_model = os.path.join(dirname, 'docs', '1.2 - Goal Model.pdf')
    method_fragments = os.path.join(dirname, 'docs', '1.3 - Method Fragments.pdf')

    sampling_strategy = os.path.join(dirname, 'docs', '2.1 - Sampling Strategy.pdf')
    data_collection = os.path.join(dirname, 'docs', '2.2 - Data Collection.pdf')

    loading_in_data = os.path.join(dirname, 'docs', '3.1 - Loading in Data.pdf')
    summary_data = os.path.join(dirname, 'docs', '3.2 - Summary data.pdf')

    metric_results = os.path.join(dirname, 'docs', '4.1 - Metric results.pdf')
    evaluation = os.path.join(dirname, 'docs', '4.2 - Evaluation.pdf')

    about = os.path.join(dirname, 'docs', '5 - About.pdf')
    all_documentation = os.path.join(dirname, 'docs', '0 - All Documentation.pdf')

class Size:
    label_frame_width = 800
    label_frame_height = 150

    button_width = 9
    button_height = 1

    listbox_width = 70
    listbox_height = 10

    # hd sizes
    hd_frame_width = 1280
    hd_frame_height = 720

    # textbox frame sizes
    txt_box_width = 100
    txt_box_height = 10

class DataTypes:
    likert_6 = ['I need a lot of additional knowledge about the topic',
                'I need some additional knowledge about the topic',
                'I need a little additional knowledge about the topic',
                'I have some knowledge about the topic',
                'I have good knowledge about the topic',
                'I have strong knowledge about the topic']

    likert_6_show = ['I need a lot\nof additional\nknowledge about the topic',
                'I need some\nadditional knowledge\nabout the topic',
                'I need a little\nadditional knowledge\nabout the topic',
                'I have some\nknowledge about\nthe topic',
                'I have good\nknowledge about\nthe topic',
                'I have strong\nknowledge about\nthe topic']

    likert_6_score = {'I need a lot of additional knowledge about the topic' : 1,
                    'I need some additional knowledge about the topic' : 1,
                    'I need a little additional knowledge about the topic' : 1,
                    'I have some knowledge about the topic' : 1,
                    'I have good knowledge about the topic' : 1,
                    'I have strong knowledge about the topic' : 1}

    likert_7 = ['strongly disagree',
                'disagree',
                'somewhat disagree',
                'neither agree or disagree',
                'somewhat agree',
                'agree',
                'strongly agree']

    likert_7_show = ['strongly\ndisagree',
                'disagree',
                'somewhat\ndisagree',
                'neither agree\nor disagree',
                'somewhat\nagree',
                'agree',
                'strongly\nagree']

    likert_7_score = {'strongly disagree' : 1,
                    'disagree' : 1,
                    'somewhat disagree' : 1,
                    'neither agree or disagree' : 1,
                    'somewhat agree' : 1,
                    'agree' : 1,
                    'strongly agree' : 1}

    mWater_types = {"multiple_choice" : 'Radio Button Question',
                    "multiple_choice_multi": 'Multi-check Question',
                    'boolean' : 'Radio Button Question',
                    'likert_6' : 'Radio Button Question',
                    'likert_7' : 'Radio Button Question',
                    'numerical' : 'Number Question',
                    'scale' : 'Likert Question',
                    'string' : 'Tekst Question'}

    mWater_formats = {'int' : 'Whole number',
                      'float' : 'Decimal number',
                      'string': 'Single line of text'}







