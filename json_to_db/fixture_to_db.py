import sqlite3
import json
from json_extract import json_extract
import sys
sys.path.insert(0, 'XXXX-XXXX')
from yet_unstructered.file_name import fixture_file_name_generator

def calc_result(home_goals, away_goals):
    if(home_goals > away_goals):
        result = 0 #heimsieg
    elif(home_goals < away_goals):
        result = 1 #auswärtssieg
    else:
        result = 0.5
    return result

con = sqlite3.connect('football.db')
cur = con.cursor()
print ("Opened database successfully")
cur.execute("CREATE TABLE fixtures (fixture_id INTEGER PRIMARY KEY, referee TEXT, timestamp INTEGER, league_id INTEGER, league_name TEXT,season INTEGER, league_round TEXT,result REAL, home_id INTEGER, home_name INTEGER, home_goals INTEGER, away_id INTEGER, away_name INTEGER, away_goals INTEGER)")

#fixture_id INTEGER PRIMARY KEY, referee TEXT, league_id INTEGER, league_name TEXT, league_round TEXT, home_id INTEGER, home_name INTEGER, home_goals INTEGER, away_id INTEGER, away_name INTEGER, away_goals INTEGER,
def fixtures_to_db(raw_path_home_statistics):
    with open(raw_path_home_statistics, encoding='utf-8') as f: #r'C:\Users\Anwender\Dropbox\PC\Documents\GitHub\sql_dataset_creation\JSON\Bundesliga_2020.json'
        bundesliga_json = json.load(f)


    response = bundesliga_json['response']
    print(response[0].keys())


    for i in range (0, len(response)):
        print("i: ", i)
    
    #fixture_dict
        fixtures = json_extract(response[i] , "fixture")
    
    #teams_dict
        teams = json_extract(response[i], "teams")

        home = json_extract(teams[0], "home")
        home_name = json_extract(home[0], "name")
        home_id = json_extract(home[0], "id")

        away = json_extract(teams[0], "away")
        away_name = json_extract(away[0], "name")
        away_id = json_extract(away[0], "id")

    #goals_dict
        goals = json_extract(response[i], "goals")

        home_goals = json_extract(goals[0], "home")
        #print("HOME: ", home_name[0],"HOME-id: ", home_id[0], "Home-Goals: ", home_goals[0])

        away_goals = json_extract(goals[0], "away")
        #print("AWAY: ", away_name[0],"AWAY-id: ", away_id[0], "Away-Goals: ", away_goals[0])
        result = calc_result(home_goals, away_goals)
        #league_dict
        league = json_extract(response[i], "league")

        league_id = json_extract(league[0], "id")
        league_name = json_extract(league[0], "name")
        league_round = json_extract(league[0], "round")
        league_season = json_extract(league[0], "season")
        #print("id: ", league_id[0], "name: ", league_name[0], "round: ", league_round[0], "season:", league_season[0])

        cur.execute("INSERT INTO fixtures VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (fixtures[0]['id'],fixtures[0]['referee'],fixtures[0]['timestamp'], league_id[0], league_name[0], league_season[0], league_round[0],result, home_id[0], home_name[0], home_goals[0], away_id[0], away_name[0], away_goals[0]))

    con.commit()
    print ("stored database successfully")
    


season = [2015,2016,2017,2018,2019,2020]
leagues = {
  "Bundesliga": 78,
  "Premier_League": 39,
  "La_Liga": 140,
  "Serie_A": 135,
  "Ligue_1": 61,
  "Eredivisie": 88,
  "Primeira_Liga": 94
}

path = "C:\\Users\\Anwender\\Dropbox\\PC\\Documents\\GitHub\\sql_dataset_creation\\JSON"
additional_word = ""


for key, value in leagues.items():
    for i in range(0, len(season)):
        path = "C:\\Users\\Anwender\\Dropbox\\PC\\Documents\\GitHub\\sql_dataset_creation\\JSON"
        path = fixture_file_name_generator(path,additional_word ,key, season[i])
        print(path)
        fixtures_to_db(path)
con.close()

