
import os
import pickle

import pandas as pd
from sqlite3 import Error
import sqlite3
import numpy as np

class surveyModel:

    def __init__(self):
        dirname = os.getcwd()
        filename = os.path.join(dirname, 'data', 'method_fragments', 'master_list.xlsx')

        self.raw_data = pd.read_excel(filename)
        self.dataframe = pd.DataFrame(self.raw_data)

    def show_relevant_fragments(self, df, item, target):

        # print('Checked item: ',item)

        relevant_categories = df.loc[(df['category'] == item) & (df['target'] == target)]
        relevant_survey_inputs = relevant_categories['survey_input']
        relevant_metrics = relevant_categories['metric']
        relevant_type = relevant_categories['type']

        list_items = [relevant_survey_inputs, relevant_metrics, relevant_type]

        return list_items

class SQLModel:

    def __init__(self, database, new):

        if new:
            # create connection
            self.conn = self.create_connection(database)

            # list of project time points
            self.measure_point_list = ["start_of_project", "halfway_point_project", "end_project", "year_after_project_end"]

            # populate db
            self.define_sql_table(self.conn)

            # HARDCODED, REMOVE LATER
            self.project = ("Test Project")
            self.create_project(self.conn, self.project)

            self.project_2 = ("Test Project Versie 2")
            self.create_project(self.conn, self.project_2)

            self.load_in_stock_data()

        else:
            # create connection
            self.conn = self.create_connection(database)

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            conn.execute("PRAGMA foreign_keys = 1")
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def define_sql_table(self, conn):

        sql_create_method_fragment_id = """ CREATE TABLE IF NOT EXISTS method_fragment (
                                                     method_fragment_id integer PRIMARY KEY,
                                                     method_fragment_name varchar(100) 
                                                 ); """

        sql_create_metric_table = """CREATE TABLE IF NOT EXISTS metric (
                                                 metric_id integer PRIMARY KEY,
                                                 metric_name text NOT NULL,
                                                 method_fragment_id integer,
                                                 metric_definition text,
                                                 metric_question text,
                                                 metric_value_type varchar(25),
                                                 multiple_answers bool,
                                                 answer_options text,
                                                 target_name varchar(50),
                                                 user_made bool,
                                                 data_type varchar(50),
                                                 FOREIGN KEY (method_fragment_id) REFERENCES method_fragment (method_fragment_id)
                                             );"""

        sql_create_project_table = """ CREATE TABLE IF NOT EXISTS project (
                                                     project_id integer PRIMARY KEY,
                                                     project_name varchar(200) 
                                                 ); """

        sql_create_metric_target_table = """ CREATE TABLE IF NOT EXISTS metric_target (
                                                 metric_target_id integer PRIMARY KEY,
                                                 increase boolean NOT NULL,
                                                 metric_target_value integer NOT NULL,
                                                 interest_demographic boolean,
                                                 interest_scope text,
                                                 project_id integer NOT NULL,
                                                 metric_id integer NOT NULL,
                                                 FOREIGN KEY (metric_id) REFERENCES metric (metric_id),
                                                 FOREIGN KEY (project_id) REFERENCES project (project_id)
                                             );"""

        sql_create_measuring_point_table = """CREATE TABLE IF NOT EXISTS measuring_point (
                                                 measuring_point_id integer PRIMARY KEY,
                                                 measuring_point_name varchar(50) NOT NULL,
                                                 project_id integer NOT NULL,
                                                 FOREIGN KEY (project_id) REFERENCES project (project_id)
                                             );"""

        sql_create_metric_value_table = """CREATE TABLE IF NOT EXISTS metric_value (
                                                 metric_value_id integer PRIMARY KEY,
                                                 measuring_point_id integer NOT NULL,
                                                 metric_id integer NOT NULL,
                                                 file_id integer,
                                                 data_bool boolean,
                                                 data_str text,
                                                 data_int integer,
                                                 data_float float,
                                                 FOREIGN KEY (metric_id) REFERENCES metric (metric_id),
                                                 FOREIGN KEY (measuring_point_id) REFERENCES measuring_point (measuring_point_id)
                                             );"""

        if conn is not None:

            # create task table
            self.create_table(conn, sql_create_method_fragment_id)

            # create task table
            self.create_table(conn, sql_create_metric_table)

            # create project table
            self.create_table(conn, sql_create_project_table)

            # create task table
            self.create_table(conn, sql_create_metric_target_table)

            # create task table
            self.create_table(conn, sql_create_measuring_point_table)

            # create task table
            self.create_table(conn, sql_create_metric_value_table)


        else:
            print("Error! cannot create the database connection.")

    def create_method_fragment(self, conn, method_fragment):


        cur = conn.cursor()

        sql = """ INSERT INTO method_fragment(method_fragment_name) 
                VALUES (?) """

        # check whether it is already present in database
        cur.execute("SELECT * FROM method_fragment WHERE method_fragment_name=?", method_fragment)
        entry = cur.fetchone()

        if entry is None:
            cur.execute(sql, method_fragment)
            conn.commit()
            # print('New method fragment added')

        # else:
        #     print('Method fragment found')

        return cur.lastrowid

    def create_metric(self, metric):

        cur = self.conn.cursor()

        sql = """ INSERT INTO metric(metric_name, method_fragment_id, metric_definition, metric_question, metric_value_type, multiple_answers, answer_options, target_name, user_made, data_type) 
                VALUES (?,?,?,?,?,?,?,?,?,?) """

        # check whether it is already present in database
        metric_name = metric[0]
        metric_target = metric[7]
        method_frag_id = metric[1]

        test_sql = "SELECT * FROM metric WHERE metric_name = ? AND target_name = ? AND method_fragment_id = ?"
        cur.execute(test_sql, (str(metric_name), str(metric_target), str(method_frag_id)))

        entry = cur.fetchone()

        if entry is None:
            cur.execute(sql, metric)
            self.conn.commit()
            # print('New metric added')

        # else:
        #     print('Metric found')

        return cur.lastrowid

    def create_metric_value(self, metric_value):

        cur = self.conn.cursor()

        sql = """ INSERT INTO metric_value(measuring_point_id, metric_id, file_id, data_bool, data_str, data_int, data_float)
                VALUES (?,?,?,?,?,?,?) """

        cur.execute(sql, metric_value)
        self.conn.commit()

        return cur.lastrowid

    def create_project(self, conn, project):

        cur = conn.cursor()

        sql = """ INSERT INTO project(project_name) 
                VALUES (?) """

        # check whether it is already present in database
        cur.execute("SELECT * FROM project WHERE project_name=?", ((project,)))
        entry = cur.fetchone()

        if entry is None:
            cur.execute(sql, ((project,)))
            conn.commit()
            # print('New project added')

        # else:
        #     print('Project found')

        return cur.lastrowid

    def create_measuring_point(self, measuring_point):

        cur = self.conn.cursor()

        sql = """ INSERT INTO measuring_point(measuring_point_name, project_id ) 
                VALUES (?,?) """

        # check whether it is already present in database
        measuring_point_name = measuring_point[0]

        # print("create_measuring_point: type ", type(measuring_point_name))
        # print("create_measuring_point: measuring_point_name ", measuring_point_name)

        sql_check = "SELECT * FROM measuring_point WHERE measuring_point_name = ? "
        cur.execute(sql_check, (((measuring_point_name),)))

        entry = cur.fetchone()

        # print('create_measuring_point - entry: ', entry)

        if entry is None:
            cur.execute(sql, measuring_point)
            self.conn.commit()
            # print('New measuring point added')

        # else:
        #     print('Measuring point found')

        return cur.lastrowid

    def create_metric_target(self, metric_target):

        cur = self.conn.cursor()

        sql = """ INSERT INTO metric_target(increase, metric_target_value, interest_demographic, interest_scope, project_id, metric_id) 
                VALUES (?,?,?,?,?,?) """

        # print('METRIC TARGET', metric_target)

        # check whether it is already present in database
        metric_id = metric_target[5]

        # print("create_measuring_point: type ", type(measuring_point_name))
        # print("create_measuring_point: measuring_point_name ", measuring_point_name)

        sql_check = "SELECT * FROM metric_target WHERE metric_id = ? "
        cur.execute(sql_check, (((metric_id),)))

        entry = cur.fetchone()

        # print('create_measuring_point - entry: ', entry)

        if entry is None:
            cur.execute(sql, metric_target)
            self.conn.commit()
            # print('New metric target added')

        else:
            # print('Metric target found')
            sql_update = 'update metric_target set metric_target_value = (?), increase = (?), interest_demographic =(?), interest_scope =(?) where metric_id = (?)'
            parameters = self.parameter

            # parameters = (metric_target[1], metric_target[0], metric_target[3], metric_id)
            # print('Metric_target| parameters: ', parameters)
            self.update_row_with_par(sql_update, parameters)

        return cur.lastrowid

    def load_in_stock_data(self):

        dirname = os.getcwd()
        filename = os.path.join(dirname, 'data', 'method_fragments', 'master_list.xlsx')

        raw_data = pd.read_excel(filename)
        dataframe = pd.DataFrame(raw_data)

        unique_values = dataframe.category.unique()
        dataframe.fillna(np.nan, inplace=True)

        for row in unique_values:
            self.create_method_fragment(self.conn, (row,))

        for index, row in dataframe.iterrows():
            category = row['category']
            metric_name = row['metric']
            metric_definition = None
            metric_question = row['survey_input']
            metric_value_type = row['type']
            answer_options = row['answer_options']
            multiple_answers = row['multiple_answers_possible']
            target_name = row['target']
            user_made = False
            data_type = row['data_type']

            if multiple_answers == 'yes':
                multiple_answers = True

            else:
                multiple_answers = False

            cur = self.conn.cursor()
            cur.execute(""" SELECT method_fragment_id FROM method_fragment WHERE method_fragment_name = (?) """,
                        (category,))
            method_fragment_id = cur.fetchall()
            method_fragment_id = int(method_fragment_id[0][0])

            row = (metric_name, method_fragment_id, metric_definition,
                   metric_question, metric_value_type, multiple_answers,
                   answer_options, target_name, user_made, data_type)

            self.create_metric(row)

    def send_parameter(self, parameter):
        self.get_parameter(parameter)

    def get_parameter(self, parameter):
        self.parameter = parameter

    def populate_measure_point_query(self):
        for point in self.measure_point_list:

            cur = self.conn.cursor()
            cur.execute(""" SELECT project_id FROM project WHERE project_name = (?) """,
                        ((self.project),))
            project_id = cur.fetchone()

            measure_point = (point, int(project_id[0]))

            # print('Measure_point_query: point - ', point)
            # print('Measure_point_query: project_id - ', project_id)
            # print('Measure_point_query: project_name - ', ((self.project),))
            # print('Measure_point_query: measure_point -

            self.create_measuring_point(measure_point)

    def query_with_par(self, query, parameter):

        cur = self.conn.cursor()
        # print('models: parameters --- ', parameter)

        try:
            cur.execute(query, parameter)
        except Error as e:
            raise e
        else:
            self.conn.commit()
            # cursor.description is None when
            # no rows are returned
            if cur.description is not None:
                return cur.fetchall()

    def query_no_par(self, query):

        cur = self.conn.cursor()
        # print('models: no parameters --- ' )

        try:
            cur.execute(query)
        except Error as e:
            raise e
        else:
            self.conn.commit()
            # cursor.description is None when
            # no rows are returned
            if cur.description is not None:
                return cur.fetchall()

    def update_row_with_par(self, query, parameter):
        cur = self.conn.cursor()

        try:
            # print('update_row parameters', parameter)
            cur.execute(query, parameter)
        except Error as e:
            raise e
        else:
            self.conn.commit()
            # print('Row updated ------')


    def delete_row_with_par(self, query, parameter):

        cur = self.conn.cursor()

        try:
            cur.execute(query, (parameter,))
        except Error as e:
            raise e
        else:
            self.conn.commit()

    def empty_table(self):

        cur = self.conn.cursor()

        query = "DELETE FROM metric_value"

        try:
            cur.execute(query)
        except Error as e:
            raise e
        else:
            self.conn.commit()
            print("DELETED")

class pathModel:

    def __init__(self):

        self.user_doc_file_paths = {'project_goals' : '',
                                    'goal_model' : '',
                                    'sampling_strategy' : ''}

        self.user_project_dates = {'date_sop': '',
                                   'date_hop': '',
                                   'date_eop': '',
                                   'date_yap': ''}

        self.dc_file_paths = {'sop_provider': '',
                               'sop_leader': '',
                               'sop_teacher': '',
                               'sop_student': '',

                               'hop_provider': '',
                               'hop_leader': '',
                               'hop_teacher': '',
                               'hop_student': '',

                               'eop_provider': '',
                               'eop_leader': '',
                               'eop_teacher': '',
                               'eop_student': '',

                               'yap_provider': '',
                               'yap_leader': '',
                               'yap_teacher': '',
                               'yap_student': ''
                              }

    def update_user_doc_path_dict(self, doc, file_path):
        self.user_doc_file_paths[doc] = file_path

    def update_dc_path_dict(self, targets_with_period, index, file_path):
        self.dc_file_paths[targets_with_period[index]] = file_path


class appDataModel:

    def __init__(self):

        print('appDataModel')
        self.load_from_save_file = False

    def get_file_name(self, filename):
        self.file_name = filename

    def save_to_file(self, database_path, path_model):

        try:
            data = {'project_goals_path' : self.pp_dict['project_goals'],
                    'goal_model_path' : self.pp_dict['goal_model'],
                    'selected_method_fragments' : self.method_fragments,
                    'isSelected' : self.method_fragments_bool,
                    'sampling_strategy_path' : self.pp_dict['sampling_strategy'],
                    'date_sop' : self.data_collection_dict_dates['date_sop'],
                    'date_hop' : self.data_collection_dict_dates['date_hop'],
                    'date_eop' : self.data_collection_dict_dates['date_eop'],
                    'date_yap' : self.data_collection_dict_dates['date_yap'],
                    'data_collection_paths' : self.data_collection_dict_paths,
                    'data_file_status_list' : self.data_collection_dict_states,
                    'selected_file_counter' : self.selected_file_counter,
                    'database_path' : database_path,
                    'path_model': path_model,
                    'metric_evaluation' : self.user_input_objects[0],
                    'target_evaluation' : self.user_input_objects[1],
                    'eval_question_1': self.user_input_objects[2],
                    'eval_question_2': self.user_input_objects[3],
                    'eval_question_3': self.user_input_objects[4],
                    'eval_question_4': self.user_input_objects[5],
                    'eval_question_5': self.user_input_objects[6],
                    'eval_question_6': self.user_input_objects[7],
                    'eval_question_7': self.user_input_objects[8]
                    }

            with open(self.file_name, 'wb') as f:
                pickle.dump(data, f)

        except Exception as e:
            print ("error saving state:", str(e))

        # print('data: ', data)
        # print('project_purpose', project_purpose)
        # print('data_collection', data_collection)
        # print('data_collection_paths', data_collection_paths)
        # print('data_analysis_loading', data_analysis_loading)

    def load_from_file(self):

        print('self.file_name: ', self.file_name)
        try:
            with open(self.file_name, "rb") as f:
                self.data = pickle.load(f)

        except Exception as e:
            print("error loading saved state:")

    def get_project_purpose(self, dict, method_frags, frags_selected):
        self.pp_dict = dict
        self.method_fragments = method_frags
        self.method_fragments_bool = frags_selected

    def get_data_collection(self, dict_date, dict_paths, status_list):
        self.data_collection_dict_dates = dict_date
        self.data_collection_dict_paths = dict_paths
        self.data_collection_dict_states = status_list

    def get_data_analysis(self, counter):
        self.selected_file_counter = counter

    def get_impact_evaluation(self, user_input):
        self.user_input_objects = user_input
