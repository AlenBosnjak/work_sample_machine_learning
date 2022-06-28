import numpy
from yet_unstructered.read_db import get_fixture_home_away_id_timestamp, get_lineup_dataframe,get_player_stats_last_five_games, len_fixtures
import pandas as pd

def is_available(lineup):
    if(len(lineup) == 0):
        return False
    else:
        return True

def calculate_player_stats_for_fixture(fixture_id, home_id, away_id, timestamp):
        home_lineup = get_lineup_dataframe(fixture_id, home_id, timestamp)
        away_lineup = get_lineup_dataframe(fixture_id, away_id, timestamp)
        home_player_values = []
        away_player_values = []

        if(is_available(home_lineup) and is_available(away_lineup)):
            
            #get keys
            player_id = int(home_lineup['player_id'].values[0])
            mean_df = get_player_stats_last_five_games(player_id, timestamp)
            keys = list(mean_df.keys())
            
            


            for j in range (0, len(home_lineup)):
                
                home_lineup.fillna('NULL', inplace=True)
                if(isinstance(home_lineup['player_id'].values[j], numpy.int64)): #hat spieler eine player_id?
                    player_id = int(home_lineup['player_id'].values[j])
                    mean_df = get_player_stats_last_five_games(player_id, timestamp)
                    value = list(mean_df)
                   
                    for k in range (0, len(keys)):
                        
                        if(k >= len(value)):
                            home_player_values.append(0.0)
                        else:
                            home_player_values.append(value[k])
                else:
                    for k in range (0, len(keys)):
                        home_player_values.append(0.0)

            
            for j in range (0, len(away_lineup)):
                
                away_lineup.fillna('NULL', inplace=True)
                if(isinstance(away_lineup['player_id'].values[j], numpy.int64)): #hat spieler eine player_id?
                    player_id = int(away_lineup['player_id'].values[j])
                    
                    mean_df = get_player_stats_last_five_games(player_id, timestamp)
                    value = list(mean_df)
                    for k in range (0, len(keys)):
                        
                        if(k >= len(value)):
                            away_player_values.append(0.0)
                        else:
                            away_player_values.append(value[k])
                else:
                    for k in range (0, len(keys)):
                        away_player_values.append(0.0)
        else:
              home_player_values = [0] *30 *11
              away_player_values = [0] *30 *11

            
        return home_player_values, away_player_values
        




