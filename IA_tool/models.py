
import os
import pandas as pd
from sqlite3 import Error
import sqlite3
import numpy as np

from .constants import FieldTypes as FT
import csv


class surveyModel:

    def __init__(self):
        # HARDCODED, CHANGE LATER!
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

    def __init__(self, database):

        # create connection
        self.conn = self.create_connection(database)

        # list of project time points
        self.measure_point_list = {"start_of_project",
                                   "halfway_point_project",
                                   "end_project",
                                   "year_after_project_end"}

        # populate db
        self.define_sql_table(self.conn)

        # HARDCODED, REMOVE LATER
        self.project = ("Test Project")
        self.create_project(self.conn, self.project)

        self.project_2 = ("Test Project Versie 2")
        self.create_project(self.conn, self.project_2)

        self.load_in_stock_data()


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
                                                 metric_name varchar(200) NOT NULL,
                                                 method_fragment_id integer,
                                                 metric_definition text,
                                                 metric_question text,
                                                 metric_value_type varchar(25),
                                                 multiple_answers bool,
                                                 answer_options text,
                                                 target_name varchar(50),
                                                 user_made bool,
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
                                                 data_bool boolean,
                                                 data_str text,
                                                 data_int integer,
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
            print('New method fragment added')

        else:
            print('Method fragment found')

        return cur.lastrowid

    def create_metric(self, metric):

        cur = self.conn.cursor()

        sql = """ INSERT INTO metric(metric_name, method_fragment_id, metric_definition, metric_question, metric_value_type, multiple_answers, answer_options, target_name, user_made) 
                VALUES (?,?,?,?,?,?,?,?,?) """

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
            print('New metric added')

        else:
            print('Metric found')

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
            print('New project added')

        else:
            print('Project found')

        return cur.lastrowid

    def create_measuring_point(self, conn, measuring_point):

        cur = conn.cursor()

        sql = """ INSERT INTO measuring_point(measuring_point_name, project_id ) 
                VALUES (?,?) """

        # check whether it is already present in database
        measuring_point_name = measuring_point[0]

        # print("create_measuring_point: type ", type(measuring_point_name))
        # print("create_measuring_point: measuring_point_name ", measuring_point_name)

        test_sql = "SELECT * FROM measuring_point WHERE measuring_point_name = ? "
        cur.execute(test_sql, (((measuring_point_name),)))

        entry = cur.fetchone()

        # print('create_measuring_point - entry: ', entry)

        if entry is None:
            cur.execute(sql, measuring_point)
            conn.commit()
            print('New measuring point added')

        else:
            print('Measuring point found')

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
                   metric_question, metric_value_type, multiple_answers, answer_options, target_name, user_made)

            self.create_metric(row)


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
            # print('Measure_point_query: measure_point - ', measure_point)
            self.create_measuring_point(self.conn, measure_point)

    def query_with_par(self, query, parameter):

        cur = self.conn.cursor()
        print('models: parameters --- ', parameter)

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

    def delete_row_with_par(self, query, parameter):

        cur = self.conn.cursor()

        try:
            cur.execute(query, (parameter,))
        except Error as e:
            raise e
        else:
            self.conn.commit()
