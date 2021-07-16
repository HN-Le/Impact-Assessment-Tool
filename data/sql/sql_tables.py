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

sql_create_metric_value_table = """CREATE TABLE IF NOT EXISTS metric (
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
