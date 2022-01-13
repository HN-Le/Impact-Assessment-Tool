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
    method_fragments = os.path.join(dirname, 'docs', '1.3.1 - Method Fragments.pdf')
    metrics = os.path.join(dirname, 'docs', '1.3.2 - Metrics.pdf')

    sampling_strategy = os.path.join(dirname, 'docs', '2.1 - Sampling Strategy.pdf')
    data_collection = os.path.join(dirname, 'docs', '2.2 - Data Collection.pdf')

    loading_in_data = os.path.join(dirname, 'docs', '3.1 - Loading in Data.pdf')
    summary_data = os.path.join(dirname, 'docs', '3.2 - Summary data.pdf')

    metric_results = os.path.join(dirname, 'docs', '4.1.1 - Metric results.pdf')
    evaluation = os.path.join(dirname, 'docs', '4.1.2 - Evaluation.pdf')

    about = os.path.join(dirname, 'docs', '5 - About.pdf')
    all_documentation = os.path.join(dirname, 'docs', '0 - All Documentation.pdf')

class Size:
    label_frame_width = 720
    label_frame_height = 150

    button_width = 9
    button_height = 1

    listbox_width = 70
    listbox_height = 10

    # hd sizes
    hd_frame_width = 1280
    hd_frame_height = 720

    # textbox frame sizes
    txt_box_width = 80
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

class MethodSteps:

    phase_1 = ["1. Define project goal (see document 1.1)",
               "2. Create goal model (see document 1.2)",
               "3. Select relevant method fragments (see document 1.3.1)",
               "4. Provide metric definitions (see document 1.3.2)",
               "5. Add additional metrics (see document 1.3.2)",
               "6. Define targets for each metric (see document 1.3.2)",
               "7. Determine demographics of interests (see document 1.3.2)"]

    phase_2 = ["1. Determine sampling strategy (see document 2.1)",
               "2. Collect context data (project provider data, see document 2.2)",
               "3. Perform survey with community/school leader (see document 2.2)",
               "4. Perform survey with teacher(s) (see document 2.2)",
               "5. Perform survey with students (see document 2.2)",
               "6. Process data in collective dataset (done by uploading survey data at step 2.2)"]

    phase_3 = ["1. Perform data analysis in results (see document 3.1)",
               "2. Create general data visualizations (see document 3.2)",
               "3. Visualize specific demographic data (see document 3.2)",
               "4. Insert data in spreadsheet (automatically done by tool)"]

    phase_4 = ["1. Evaluate in metric results (see document 4.1.1)",
               "2. Evaluate on project goals and targets (see document 4.1.2)",
               "3. Evaluate with evaluation questions (see document 4.1.2)",
               "4. Write impact assessment report (based on tool results)",
               "5. Create or change project plans"]

























