import psycopg2
import json
import sys 
import os 

if not os.path.isfile('config.json'):
    sys.exit('config.json is required!')
else:
    with open('config.json') as f:
        config = json.load(f)

def connect():
    try:
        conn = psycopg2.connect(
            host=config['db_host'],
            database=config['db_name'],
            user=config['db_user'],
            port=config['db_port'],
            password=['db_pw']
        )
        
        return conn

    except Exception as e:
        print(e)


def create_profile_table():
    pass


if __name__ == '__main__':
    create_profile_table()

