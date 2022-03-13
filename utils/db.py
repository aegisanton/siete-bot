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
        #conn = psycopg2.connect(
        #    host=config['db_host'],
        #    database=config['db_name'],
        #    user=config['db_user'],
        #    port=config['db_port'],
        #    password=['db_pw']
        #)
        conn = psycopg2.connect(config['db_url'], sslmode='require')
        
        return conn

    except Exception as e:
        print(e)


def create_profile_table(conn):
    statement = '''CREATE TABLE IF NOT EXISTS members (
        discord_id bigint PRIMARY KEY,
        gbf_id integer,
        server_nick text,
        crystals integer DEFAULT 0,
        tickets smallint DEFAULT 0,
        ten_tickets smallint DEFAULT 0,
        rolls smallint DEFAULT 0,
        fire_a varchar(30),
        fire_b varchar(30),
        water_a varchar(30),
        water_b varchar(30),
        wind_a varchar(30),
        wind_b varchar(30),
        earth_a varchar(30),
        earth_b varchar(30),
        light_a varchar(30),
        light_b varchar(30),
        dark_a varchar(30),
        dark_b varchar(30),
        misc_a varchar(30),
        misc_b varchar(30)
    ) '''

    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    cur.close()

def drop_table(conn, table_name):
    '''
    CURRENTLY BROKEN: syntax error 
    '''
    statement = '''DROP TABLE IF EXISTS %s
    CASCADE
    '''

    cur = conn.cursor()
    cur.execute(statement, (table_name,))
    conn.commit()
    cur.close()

def drop_all_rows(conn, table_name):
    '''
    CURRENTLY BROKEN: syntax error 
    '''
    statement = 'DELETE FROM members'

    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    cur.close()

def create_profile(conn, discord_id, server_nick, gbf_id=None):
    '''
    Creates a new member profile if it does not exist for the provided user's Discord ID.
    '''
    statement = '''INSERT INTO members(discord_id, server_nick, gbf_id)
    VALUES (%s, %s, %s)
    ON CONFLICT (discord_id) DO NOTHING
    RETURNING *
    '''

    cur = conn.cursor()
    cur.execute(statement, (discord_id, server_nick, gbf_id))
    profile = cur.fetchone()
    conn.commit()
    cur.close()

    return profile

def get_profile(conn, discord_id):
    '''
    Retrieves a member profile as specified by the discord user ID.
    '''
    statement = '''SELECT * FROM members
    WHERE discord_id = %s
    '''
    cur = conn.cursor()
    cur.execute(statement, (discord_id,))
    profile = cur.fetchone()
    cur.close()

    return profile 

if __name__ == '__main__':
    conn = connect()
    if conn:
        #create_profile_table(conn)
        drop_all_rows(conn, 'members')
        conn.close()
    else:
        raise Exception

