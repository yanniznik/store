import json
import pymysql

def load_config_file(path):
    with open(path) as f:
        json_dict = json.load(f)
    return json_dict

def create_sql_connection(config_dict):
    connection = pymysql.connect(host=config_dict["host"],
                                 user=config_dict["user"],
                                 password=config_dict["password"],
                                 db=config_dict["db"],
                                 charset='utf8mb4',
                                 autocommit=True,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
