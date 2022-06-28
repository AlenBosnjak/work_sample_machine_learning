from json_extract import json_extract
import sqlite3
import json
import pandas as pd
# some_file.py

#cur.execute("CREATE TABLE lineups (fixture_id INTEGER, team_id INTEGER,timestamp INTEGER, player_id INTEGER, player_name TEXT, player_number INTEGER, player_position TEXT, grid TEXT)")

def get_fixture_timestamp(fixture_id):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT timestamp FROM fixtures AS ps WHERE ps.fixture_id = (?)", con, params=(fixture_id,))
    
    timestamp_int = int(df.loc[0]['timestamp'])
    con.close()
    return timestamp_int
#fixture_id INTEGER, team_id INTEGER, player_id INTEGER, player_name TEXT, player_number INTEGER, player_position TEXT, grid TEXT

def type_help(variable, name):
    if(isinstance(variable, str)):
        print(name, "TEXT")
        print(variable)
    else:
        print(name,"INTEGER")
        print(variable)
    print(type(variable))

def get_player(startXis_list, number_in_list, number_in_lineup, team_list):
        id = json_extract(startXis_list[number_in_list][number_in_lineup], "id")
        name = json_extract(startXis_list[number_in_list][number_in_lineup], "name")
        number = json_extract(startXis_list[number_in_list][number_in_lineup], "number")
        pos = json_extract(startXis_list[number_in_list][number_in_lineup], "pos")
        grid = json_extract(startXis_list[number_in_list][number_in_lineup], "grid")
        team_id = team_list[number_in_list]['id']

        return  team_id, id[0], name[0], number[0], pos[0], grid[0]

def lineup_to_db(raw_path_lineups, con):
    cur = con.cursor()
    with open(raw_path_lineups, encoding='utf-8') as f:
        lineups = json.load(f)
        fixture = json_extract(lineups, "fixture")
        startXis = json_extract(lineups, "startXI")
        
        
        teams = json_extract(lineups, "team")
        
        #StartXis und Teams beinhalten doppelt do viele Einträge wie fixtures, alle geraden zahlen sind home die ungeraden away
        home_iterator=0 
        away_iterator=1

        for i in range (0, len(fixture)):
            #print(fixture[i], "hier")
           
            timestamp = get_fixture_timestamp(int(fixture[i]))
            for number_in_lineup in range (0, 11):
                
                team_id, player_id, player_name, player_number, player_position, grid= get_player(startXis, home_iterator, number_in_lineup , teams)
                
                fixture_id = int(fixture[i])
                cur.execute("INSERT INTO lineups VALUES (?,?,?,?,?,?,?,?);", (fixture_id, team_id,timestamp, player_id, player_name, player_number, player_position, grid))

            for number_in_lineup in range (0, 11):
                team_id, player_id, player_name, player_number, player_position, grid  = get_player(startXis, away_iterator, number_in_lineup , teams)
                
                fixture_id = int(fixture[i])
                cur.execute("INSERT INTO lineups VALUES (?,?,?,?,?,?,?,?);", (fixture_id, team_id,timestamp, player_id, player_name, player_number, player_position, grid))
            if(home_iterator+2 < len(startXis)):
                home_iterator = home_iterator+2
            if(away_iterator+2 < len(startXis)):
                away_iterator = away_iterator+2
    
    con.commit()
    
    


