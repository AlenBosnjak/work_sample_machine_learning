from json_extract import json_extract
import sqlite3
import json
import sys
sys.path.insert(0, 'XXXX-XXXX')
from yet_unstructered.read_db import get_fixture_timestamp
# some_file.py

#cur.execute("CREATE TABLE awayFixtureStatistic (fixture_id INTEGER, team_id INTEGER,timestamp INTEGER, name TEXT, Shots_on_Goal INTEGER, Shots_off_Goal INTEGER, Total_Shots INTEGER, Blocked_Shots INTEGER, Shots_insidebox INTEGER, Shots_outsidebox INTEGER, Fouls INTEGER, Corner_Kicks INTEGER, Offsides INTEGER, Ball_Possession INTEGER, Yellow_Cards INTEGER, Red_Cards INTEGER, Goalkeeper_Saves INTEGER, Total_passes INTEGER, Passes_accurate INTEGER, Passing_accuracy INTEGER)")

#fixture_id INTEGER, id INTEGER, name TEXT, Shots_on_Goal INTEGER, Shots_off_Goal INTEGER, Total_Shots INTEGER, Blocked_Shots INTEGER, Shots_insidebox INTEGER, Shots_outsidebox INTEGER, Fouls INTEGER, Corner_Kicks INTEGER, Offsides INTEGER, Ball_Possession INTEGER, Yellow_Cards INTEGER, Red_Cards INTEGER, Goalkeeper_Saves INTEGER, Total_passes INTEGER, Passes_accurate INTEGER, Passing_accuracy INTEGER

def home_statistics_to_db(raw_path_home_statistics, con):
    cur = con.cursor()
    with open(raw_path_home_statistics, encoding='utf-8') as f:
        home_statistics = json.load(f)

    for i in range (0, len(home_statistics)):
       
        fixture = json_extract(home_statistics[i] , "fixture")
        response = json_extract(home_statistics[i] , "response")
        
        #print(fixture[0])
        team = json_extract(response, "team")
        if(len(team) > 0):
            team_id = json_extract (team, "id")
            
            team_name = json_extract (team, "name")
            statistics = json_extract(response, "statistics")
            types = json_extract (statistics, "type")
            value = json_extract (statistics, "value")
            
            fixture[0] = int(fixture[0])#fixture_id
            team_id[0] = int(team_id[0])
            timestamp = get_fixture_timestamp(fixture[0])
            if(isinstance(value[15], str)):
                value[15] = int(value[15].replace('%', '')) #pass_accuracy
            if(isinstance(value[9], str)):
                value[9] = int(value[9].replace('%', '')) #ball_possesion
                print(value[9])
            for i in range (0, len(value)):
                if(value[i] == None):
                    value[i] = 0
            
            
            
                #Shots on Goal, Shots off Goal, Total Shots, Blocked Shots, Shots insidebox, Shots outsidebox, Fouls, Corner Kicks, Offsides, Ball Possession, Yellow Cards, Red Cards, Goalkeeper Saves, Total passes, Passes accurate, Passes % 
            #cur.execute("INSERT INTO homeFixtureStatistic VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (fixture[0],team_id[0],timestamp, team_name[0], value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10],value[11],value[12],value[13],value[14],value[15]))
    
    con.commit()
    
   
def away_statistics_to_db(raw_path_away_statistics, con):
    cur = con.cursor()
    with open(raw_path_away_statistics, encoding='utf-8') as f:
        away_statistics = json.load(f)

    for i in range (0, len(away_statistics)):
       
        fixture = json_extract(away_statistics[i] , "fixture")
        response = json_extract(away_statistics[i] , "response")
        
        team = json_extract(response, "team")
        #print(fixture[0])
        if(len(team) > 0):
            team_id = json_extract (team, "id")
            team_name = json_extract (team, "name")
            statistics = json_extract(response, "statistics")
            value = json_extract (statistics, "value")
            
            fixture[0] = int(fixture[0])#fixture_id
            team_id[0] = int(team_id[0])
            timestamp = get_fixture_timestamp(fixture[0])
            if(isinstance(value[15], str)):
                value[15] = int(value[15].replace('%', '')) #pass_accuracy
            if(isinstance(value[9], str)):
                value[9] = int(value[9].replace('%', '')) #ball_possesion
            for i in range (0, len(value)):
                if(value[i] == None):
                    value[i] = 0
            
                #Shots on Goal, Shots off Goal, Total Shots, Blocked Shots, Shots insidebox, Shots outsidebox, Fouls, Corner Kicks, Offsides, Ball Possession, Yellow Cards, Red Cards, Goalkeeper Saves, Total passes, Passes accurate, Passes % 
            #cur.execute("INSERT INTO awayFixtureStatistic VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (fixture[0],team_id[0],timestamp, team_name[0], value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10],value[11],value[12],value[13],value[14],value[15]))
        
    con.commit()
    

