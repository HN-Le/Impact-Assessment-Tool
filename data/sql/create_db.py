import sqlite3
from sqlite3 import Error
import os
import pandas as pd

# from . import populate_core_data as core

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main ():
    dirname = os.getcwd()
    name_db = 'test_database.db'
    database = os.path.join(dirname, name_db)

    conn = create_connection(database)

    define_sql_table(conn)

    load_in_fragments(conn)

    conn.close()

def define_sql_table(conn):
    sql_create_project_table = """ CREATE TABLE IF NOT EXISTS project (
                                                 project_id integer PRIMARY KEY,
                                                 project_id_name varchar(200) 
                                             ); """

    sql_create_metric_target_table = """ CREATE TABLE IF NOT EXISTS metric_target (
                                             metric_target_id integer PRIMARY KEY,
                                             target_name varchar(50) NOT NULL,
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

    sql_create_metric_table = """CREATE TABLE IF NOT EXISTS metric (
                                             metric_id integer PRIMARY KEY,
                                             metric_name varchar(200) NOT NULL,
                                             method_fragment_id integer NOT NULL,
                                             metric_definition text,
                                             metric_question text,
                                             metric_value_type varchar(25),
                                             multiple_answers bool,
                                             answer_options text,
                                             FOREIGN KEY (method_fragment_id) REFERENCES method_fragment (method_fragment_id)
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

    sql_create_method_fragment_id = """ CREATE TABLE IF NOT EXISTS method_fragment (
                                                 method_fragment_id integer PRIMARY KEY,
                                                 method_fragment_name varchar(100) 
                                             ); """

    if conn is not None:
        # create project table
        create_table(conn, sql_create_project_table)

        # create task table
        create_table(conn, sql_create_metric_target_table)

        # create task table
        create_table(conn, sql_create_measuring_point_table)

        # create task table
        create_table(conn, sql_create_metric_table)

        # create task table
        create_table(conn, sql_create_metric_value_table)

        # create task table
        create_table(conn, sql_create_method_fragment_id)


    else:
        print("Error! cannot create the database connection.")


def create_metric(conn, metric):

    sql = """ INSERT INTO metric(metric_name, method_fragment_id, metric_definition, metric_question, metric_value_type) 
            VALUES (?,?,?,?,?) """

    cur = conn.cursor()
    cur.execute(sql, metric)
    conn.commit()

    return cur.lastrowid

def create_method_fragment(conn, method_fragment):

    cur = conn.cursor()

    sql = """ INSERT INTO method_fragment(method_fragment_name) 
            VALUES (?) """

    # check whether it is already present in database
    cur.execute("SELECT * FROM method_fragment WHERE method_fragment_name=?", method_fragment)
    entry = cur.fetchone()

    if entry is None:
        cur.execute(sql, method_fragment)
        conn.commit()
        print('New entry added')

    else:
        print('Entry found')

    return cur.lastrowid

def load_in_fragments(conn):
    dirname = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    filename = os.path.join(dirname, 'method_fragments', 'master_list.xlsx')

    raw_data = pd.read_excel(filename)
    dataframe = pd.DataFrame(raw_data)

    unique_values = dataframe.category.unique()

    for row in unique_values:
        create_method_fragment(conn, ((row,)))

if __name__ == '__main__':
    main()



