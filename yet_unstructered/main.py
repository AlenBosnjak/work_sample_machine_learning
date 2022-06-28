import sqlite3
import sys
import winsound
sys.path.insert(0, '/XXXX-XXXX')
sys.path.insert(0, 'XXXX-XXXX')
sys.path.insert(0, '/XXXX-XXXX')
from yet_unstructered.read_db import get_fixture_timestamp
from yet_unstructered.file_name import fixture_file_name_generator
from request_fixture_statistics import request_fixture_statistics_home, request_fixture_statistics_away
from request_lineups import request_lineups
from request_player_statistics import request_player_statistics
from fixture_statistics_to_db import home_statistics_to_db, away_statistics_to_db
from lineup_to_db import lineup_to_db
from player_statistics_to_db import player_statistics_to_db


def reqeust_all_data(league_name, season, league_id):
        con = sqlite3.connect('football.db')
    
        # try:
            #fixture_statistic_home to JSON
        path = "XXXX-XXXX"
        additional_word = "_home_stats"
        store_json_path = fixture_file_name_generator(path,additional_word, league_name, season)
        

        #fixture_statistic_home to db
        home_statistics_to_db(store_json_path, con)

        #fixture_statistic_away to JSON
        path = "XXXX-XXXX"
        additional_word = "_away_stats"
        store_json_path = fixture_file_name_generator(path,additional_word, league_name, season)
        request_fixture_statistics_home(season, league_id, store_json_path, con)
        request_fixture_statistics_away(season, league_id, store_json_path, con)
        request_lineups(season, league_id, store_json_path, con)
        request_player_statistics(season, league_id, store_json_path, con)

        #fixture_statistic_away to db
        away_statistics_to_db(store_json_path, con)

        #lineups to JSON
        path = "XXXX-XXXX"
        additional_word = "_lineups"
        store_json_path = fixture_file_name_generator(path,additional_word, league_name, season)
        request_lineups(season, league_id, store_json_path, con)

        #lineups to db
        lineup_to_db(store_json_path, con)

        #player_statistics to JSON
        path = "XXXX-XXXX"
        additional_word = "_player_statistics"
        store_json_path = fixture_file_name_generator(path,additional_word, league_name, season)
        request_player_statistics(season, league_id, store_json_path, con)
        
        #player_statistics to db
        player_statistics_to_db(store_json_path, con)
        
        con.close()

seasons = [2015, 2016, 2017, 2018, 2019, 2020]
leagues = {
  "Bundesliga": 78,
  "Premier_League": 39,
  "La_Liga": 140,
  "Serie_A": 135,
  "Ligue_1": 61,
  "Eredivisie": 88,
  "Primeira_Liga": 94
}

#main("Primeira_Liga", 2015, 94)
    
for key, value in leagues.items():
    for i in range(0, len(seasons)):
        print(key, value, seasons[i])
        reqeust_all_data(str(key), seasons[i], value)
#eredivisie home_statistics von 2015 und 2016, 2017, 2018 sind doppelt in der Datenbank