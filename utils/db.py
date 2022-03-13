import psycopg2
import psycopg2.sql as sql 
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
    Drops the specified table.
    '''
    statement = '''DROP TABLE IF EXISTS {0}
    CASCADE
    '''

    cur = conn.cursor()
    model_query = sql.SQL(statement)
    query = model_query.format(sql.Identifier(table_name))

    cur.execute(query)
    conn.commit()
    cur.close()

def drop_all_rows(conn, table_name):
    '''
    Drops all rows from the specified table.
    '''
    statement = 'DELETE FROM {0}'

    cur = conn.cursor()
    model_query = sql.SQL(statement)
    query = model_query.format(sql.Identifier(table_name))

    cur.execute(query)
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
    conn.commit()
    profile = cur.fetchone()
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

def update_summons(conn, discord_id, summons):
    '''
    Updates the support summons set on a member profile as specified by the discord user ID.
    Since not all summons need to be defined, the statement needs to be able to handle missing values.
    '''
    statement = '''UPDATE members SET
    fire_a = COALESCE(%s, fire_a),
    fire_b = COALESCE(%s, fire_b),
    water_a = COALESCE(%s, water_a),
    water_b = COALESCE(%s, water_b),
    wind_a = COALESCE(%s, wind_a),
    wind_b = COALESCE(%s, wind_b),
    earth_a = COALESCE(%s, earth_a),
    earth_b = COALESCE(%s, earth_b),
    light_a = COALESCE(%s, light_a),
    light_b = COALESCE(%s, light_b),
    dark_a = COALESCE(%s, dark_a),
    dark_b = COALESCE(%s, dark_b),
    misc_a = COALESCE(%s, misc_a),
    misc_b = COALESCE(%s, misc_b)
    WHERE discord_id = %s
    RETURNING *
    '''
    cur = conn.cursor()
    cur.execute(statement, (summons.get('fire_a'), summons.get('fire_b'), summons.get('water_a'), summons.get('water_b'), 
                            summons.get('wind_a'), summons.get('wind_b'), summons.get('earth_a'), summons.get('earth_b'),
                            summons.get('light_a'), summons.get('light_b'), summons.get('dark_a'), summons.get('dark_b'),
                            summons.get('misc_a'), summons.get('misc_b'), discord_id)
    )
    conn.commit()
    profile = cur.fetchone()
    cur.close()

    return profile 

def update_spark(conn, discord_id, resources, profile):
    '''
    Updates the spark statistics for a member profile as specified by the discord user ID.
    Since not all resources need to be defined, the statement needs to be able to handle missing values.
    '''
    crystals = resources.get('crystals', profile[3])
    tickets = resources.get('tickets', profile[4])
    ten_tickets = resources.get('ten_tickets', profile[5])
    rolls = crystals // 300 + tickets + 10 * ten_tickets

    statement = '''UPDATE members SET
    crystals = COALESCE(%s, crystals),
    tickets = COALESCE(%s, tickets),
    ten_tickets = COALESCE(%s, ten_tickets),
    rolls = COALESCE(%s, rolls)
    WHERE discord_id = %s
    RETURNING *
    '''

    cur = conn.cursor()
    cur.execute(statement, (crystals, tickets, ten_tickets, rolls, discord_id)
    )
    conn.commit()
    profile = cur.fetchone()
    cur.close()

    return profile 

def read_materials():
    file_path = 'materials_list.txt'
    materials = {}

    with open(file_path) as f:
        for line in f:
            # Remove comments and empty lines 
            if not line.startswith('#') and line != '\n':
                line = line.strip()

                variable = line.lower().replace("'", '').replace('-', ' ').replace(' ', '_')
                materials[line] = variable

    return materials

def create_donation_table(conn):
    materials = read_materials()
    variables = list(materials.values())

    cur = conn.cursor()

    columns = [sql.Identifier(v).as_string(cur) + f' integer DEFAULT 0 CHECK ({sql.Identifier(v).as_string(cur)} >= 0)' for v in variables]

    statement = 'CREATE TABLE IF NOT EXISTS donations (discord_id bigint PRIMARY KEY REFERENCES members,{0})'

    model_query = sql.SQL(statement)
    column_list = sql.SQL(','.join(columns))

    query = model_query.format(column_list)

    cur.execute(query)
    cur.close()
    conn.commit()

def save_donation(conn, discord_id, material, quantity):
    '''
    Registers a donation. Creates a row in the donation table if there doesn't exist one for the user specified by the Discord ID.
    '''
    statement = '''INSERT INTO donations (discord_id, {0})
    VALUES (%s, %s)
    ON CONFLICT (discord_id) DO UPDATE
        SET {0} = donations.{0} + EXCLUDED.{0}
    RETURNING {0}
    '''

    cur = conn.cursor()
    model_query = sql.SQL(statement)
    material = sql.Identifier(material)
    query = model_query.format(material)

    cur.execute(query, (discord_id, quantity))
    row = cur.fetchone()
    cur.close()
    conn.commit()

    return row 

if __name__ == '__main__':
    conn = connect()
    if conn:
        #create_profile_table(conn)
        #drop_table(conn, 'donations')
        create_donation_table(conn)
        #drop_all_rows(conn, 'members')
        conn.close()
    else:
        pass

