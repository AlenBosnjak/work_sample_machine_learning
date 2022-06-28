import sqlite3
import time
from traceback import print_tb
import pandas as pd
import winsound


def len_awayFixtureStatistic():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    all = cur.execute('SELECT * FROM awayFixtureStatistic').fetchall()
    print(len(all))
    con.close()

def len_homeFixtureStatistic():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    all = cur.execute('SELECT * FROM homeFixtureStatistic').fetchall()
    print(len(all))
    con.close()

def len_fixtures():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    all = cur.execute('SELECT * FROM fixtures AS f').fetchall()
    con.close()
    return len(all)

def len_lineups():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    all = cur.execute('SELECT * FROM lineups').fetchall()
    print(len(all))
    con.close()

def len_playerStatistic():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    all = cur.execute('SELECT * FROM playerStatistic').fetchall()
    print(len(all))
    con.close()

def testing():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    pd.set_option('display.max_rows', None)
    start = time.time()
    df = pd.read_sql_query("SELECT team_id FROM teamRatings WHERE elo < 1450", con)
    elapsed_time_fl = (time.time() - start) 
    print(str(elapsed_time_fl)+ " time")
    print(df)
    con.close()
    return df
def test_panda():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    print(type(pd.read_sql_query("SELECT * FROM fixtures",con)))
    print(pd.read_sql_query("SELECT * FROM fixtures",con))
    pd.set_option('display.max_columns', 500)
    
    df = pd.read_sql_query("SELECT * FROM fixtures",con)
    print(df[['fixture_id', 'result']])
    print(type(df))
    
    first = df.loc[2]
    print(first)
    print(type(first))
    con.close()

def get_fixture_home_away_id_timestamp(i):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM fixtures AS f ORDER BY league_id, timestamp ASC", con)
    small_df = df[['fixture_id', 'home_id', 'away_id', 'timestamp']]
    fixture_id = int(small_df.loc[i]["fixture_id"])
    home_id = int(small_df.loc[i]["home_id"])
    away_id = int(small_df.loc[i]["away_id"])
    timestamp = int(small_df.loc[i]["timestamp"])
    con.close()
    return fixture_id, home_id, away_id, timestamp

def get_fixture_goals_result(fixture_id):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM fixtures AS f WHERE f.fixture_id = (?)", con, params=(fixture_id,))
    if None not in (df.loc[0]["home_goals"], df.loc[0]["away_goals"], df.loc[0]["result"]):
        home_goals = int(df.loc[0]["home_goals"])
        away_goals = int(df.loc[0]["away_goals"])
        result = float(df.loc[0]["result"])
        con.close()

        return  home_goals, away_goals, result
    else:
        print("NONE in get_fixture_goals_result")
        return None, None, None

def get_lineup_dataframe(fixture_id, team_id, timestamp):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM lineups AS lu WHERE lu.fixture_id = (?) AND lu.team_id = (?) AND lu.timestamp = (?)", con, params=(fixture_id, team_id, timestamp))
    con.close()
    return df

def get_player_stats_for_fixture(fixture_id, team_id, player_id):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM playerStatistic AS ps WHERE ps.fixture_id = (?) AND ps.team_id = (?) AND ps.player_id = (?)", con, params=(fixture_id, team_id, player_id))
    con.close()

def get_player_stats_last_five_games(player_id, timestamp):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM playerStatistic AS ps WHERE ps.player_id = (?) AND ps.timestamp < (?) ORDER BY ps.timestamp DESC", con, params=(player_id,timestamp))
    df.drop(columns='fixture_id', inplace=True)
    df.drop(columns='team_id', inplace=True)
    df.drop(columns='timestamp', inplace=True)
    if (len(df) == 0):
        df = pd.read_sql_query("SELECT * FROM playerStatistic AS ps WHERE ps.player_id = (?) AND ps.timestamp = (?)", con, params=(player_id,timestamp))
        df = df.head(n=1) #trimmen auf 1 eintrag, um nicht alle x tausend auf null zu setzen
        df.drop(columns='fixture_id', inplace=True)
        df.drop(columns='team_id', inplace=True)
        df.drop(columns='timestamp', inplace=True)
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    df_cut = df.head(n=5)
    df_cut_numeric = df_cut._get_numeric_data()
    df_mean = df_cut_numeric.mean(numeric_only = True)
    con.close()
    return df_mean

def get_home_stats_last_five_games(home_id, timestamp):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM homeFixtureStatistic AS ps WHERE ps.team_id = (?) AND ps.timestamp < (?) ORDER BY ps.timestamp DESC", con, params=(home_id,timestamp))
    df.drop(columns='fixture_id', inplace=True)
    df.drop(columns='team_id', inplace=True)
    df.drop(columns='timestamp', inplace=True)
    if (len(df) == 0):
        print("get_home_stats_last_five_games:", "no games from team", home_id, "before:", timestamp)
        df = pd.read_sql_query("SELECT * FROM homeFixtureStatistic", con)
        df = df.head(n=1)
        df.drop(columns='fixture_id', inplace=True)
        df.drop(columns='team_id', inplace=True)
        df.drop(columns='timestamp', inplace=True)
        print("is filled with zeros")
        for col in df.columns:
            df[col].values[:] = 0

    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    df_cut = df.head(n=5)
    df_cut_numeric = df_cut._get_numeric_data()
    df_mean = df_cut_numeric.mean(numeric_only = True)
    con.close()
    return list(df_mean)

def get_away_stats_last_five_games(away_id, timestamp):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM awayFixtureStatistic AS ps WHERE ps.team_id = (?) AND ps.timestamp < (?) ORDER BY ps.timestamp DESC", con, params=(away_id,timestamp))
    df.drop(columns='fixture_id', inplace=True)
    df.drop(columns='team_id', inplace=True)
    df.drop(columns='timestamp', inplace=True)
    if (len(df) == 0):
        print("get_away_stats_last_five_games:", "no games from team", away_id, "before:", timestamp)
        print("is filled with zeros")
        df = pd.read_sql_query("SELECT * FROM homeFixtureStatistic", con)
        df = df.head(n=1)
        df.drop(columns='fixture_id', inplace=True)
        df.drop(columns='team_id', inplace=True)
        df.drop(columns='timestamp', inplace=True)
        for col in df.columns:
            df[col].values[:] = 0
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    df_cut = df.head(n=5)
    df_cut_numeric = df_cut._get_numeric_data()
    df_mean = df_cut_numeric.mean(numeric_only = True)
    con.close()
    return list(df_mean)
    
def checkColumnNames(name):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    print('\nColumns in', name ,' table:')
    data=cur.execute("SELECT * FROM '%s'" % name)
    for column in data.description:   
        print(column[0])
    con.close()
   
def dropTable(name):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("DROP TABLE '%s'" % name)
    con.commit()
    con.close()

def get_fixture_timestamp(fixture_id):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT timestamp FROM fixtures AS ps WHERE ps.fixture_id = (?)", con, params=(fixture_id,))
    timestamp_int = int(df.loc[0]['timestamp'])
    con.close()
    return timestamp_int

def get_fixture_values(fixture_id):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM fixtures AS ps WHERE ps.fixture_id = (?)", con, params=(fixture_id,))
    keys = list(df.keys())
    values = list(df.values)
    values = values[0]
    con.close()
    return values

def get_fixture_keys():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM fixtures", con)
    keys = list(df.keys())
    con.close()
    return keys
    
def get_player_statistics_home_away_keys():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM playerStatistic", con)
    df.drop(columns='fixture_id', inplace=True)
    df.drop(columns='team_id', inplace=True)
    df.drop(columns='timestamp', inplace=True)
    df.drop(columns='name', inplace=True)
    df.drop(columns='position', inplace=True)
    keys = list(df.keys())
    home_keys = []
    away_keys = []
    for j in range (0, 11):
        for k in range (0, len(keys)):
            key = "h_p"+ str(j) +"_"+ keys[k]
            home_keys.append(key)
        for k in range (0, len(keys)):
            key = "a_p"+ str(j) +"_"+keys[k]
            away_keys.append(key)
    con.close()
    return home_keys, away_keys
#checkColumnNames("lineups") 
def get_team_statistics_keys():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM homeFixtureStatistic", con)
    df.drop(columns='fixture_id', inplace=True)
    df.drop(columns='team_id', inplace=True)
    df.drop(columns='timestamp', inplace=True)
    df.drop(columns='name', inplace=True)
    keys = list(df.keys())
    home_keys = []
    away_keys = []
    
    for k in range (0, len(keys)):
        key = "h_"+ keys[k]
        home_keys.append(key)
    for k in range (0, len(keys)):
        key = "a_" +keys[k]
        away_keys.append(key)
    con.close()
    return home_keys, away_keys

def testing2(season, league_id):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    fixture_ids = cur.execute("SELECT fixture_id FROM fixtures AS f WHERE f.season =? AND f.league_id=?", (season, league_id)).fetchall()
    print(len(fixture_ids))
    for i in range (0, len(fixture_ids)):
        
        nerv = str(fixture_ids[i][0])
        players = cur.execute("SELECT * FROM playerStatistic as ps WHERE ps.fixture_id =?", (nerv,)).fetchall()
        print(len(players))
        print(players[0])
    con.commit()
    #print(pd.read_sql_query("SELECT fixture_id, home_id FROM fixtures AS f WHERE f.season = (?)", con, params=(season,)))
    con.close()

def create_playerStatistics():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("CREATE TABLE playerStatistic (fixture_id INTEGER, team_id INTEGER,timestamp INTEGER, name TEXT, player_id INTEGER, minutes INTEGER, number INTEGER, position TEXT, rating INTEGER, offside INTEGER, total_shots INTEGER, on_goal_shots INTEGER, total_goals INTEGER, conceded INTEGER, assists INTEGER, saves INTEGER, total_passes INTEGER, key_passes INTEGER, pass_accuracy INTEGER, total_tackels INTEGER, blocks INTEGER, interceptions INTEGER, total_duels INTEGER, won_duels INTEGER, dribble_attempts INTEGER, dribble_success INTEGER, dribble_past INTEGER, drawn_fouls INTEGER, commited_fouls INTEGER, yellow INTEGER, red INTEGER, won_penalty INTEGER, commited_penalty INTEGER, scored_penalty INTEGER, missed_penalty INTEGER, saved_penalty INTEGER)")
    con.close()

def create_lineups():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("CREATE TABLE lineups (fixture_id INTEGER, team_id INTEGER,timestamp INTEGER, player_id INTEGER, player_name TEXT, player_number INTEGER, player_position TEXT, grid TEXT)")
    con.close()

def create_home_statistics():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("CREATE TABLE homeFixtureStatistic (fixture_id INTEGER, team_id INTEGER,timestamp INTEGER, name TEXT, Shots_on_Goal INTEGER, Shots_off_Goal INTEGER, Total_Shots INTEGER, Blocked_Shots INTEGER, Shots_insidebox INTEGER, Shots_outsidebox INTEGER, Fouls INTEGER, Corner_Kicks INTEGER, Offsides INTEGER, Ball_Possession INTEGER, Yellow_Cards INTEGER, Red_Cards INTEGER, Goalkeeper_Saves INTEGER, Total_passes INTEGER, Passes_accurate INTEGER, Passing_accuracy INTEGER)")
    con.close()

def create_away_statistics():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("CREATE TABLE awayFixtureStatistic (fixture_id INTEGER, team_id INTEGER,timestamp INTEGER, name TEXT, Shots_on_Goal INTEGER, Shots_off_Goal INTEGER, Total_Shots INTEGER, Blocked_Shots INTEGER, Shots_insidebox INTEGER, Shots_outsidebox INTEGER, Fouls INTEGER, Corner_Kicks INTEGER, Offsides INTEGER, Ball_Possession INTEGER, Yellow_Cards INTEGER, Red_Cards INTEGER, Goalkeeper_Saves INTEGER, Total_passes INTEGER, Passes_accurate INTEGER, Passing_accuracy INTEGER)")
    con.close()

def create_elo():
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    df = pd.read_sql_query("SELECT DISTINCT away_id FROM fixtures UNION SELECT DISTINCT home_id FROM fixtures", con)
    pd.set_option('display.max_rows', None)
    
    cur.execute("CREATE TABLE teamRatings(team_id INTEGER, timestamp INTEGER ,elo REAL, attack REAL, defence REAL)")
    for i in range(len(df)):
        team_id = int(df.iloc[i]['away_id'])
        elo =  float(1500)
        attack = float(0) 
        defence = float (0)
        cur.execute("INSERT INTO teamRatings VALUES (?,?,?,?);", (team_id, elo, attack, defence)) #es steht awas_is aber nur weil UNION ersten select als name zurück gibt
        
    con.commit()
    con.close()

def get_team_rating(team_id):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    df = pd.read_sql_query("SELECT *  FROM teamRatings AS tr WHERE team_id = (?)", con, params=(team_id,))
    elo = float(df.loc[0]["elo"])
    attack = float(df.loc[0]["attack"])
    defence = float(df.loc[0]["defence"])
    con.close()
    return elo, attack, defence

def update_team_rating( team_id, elo, attack, defence, fixture_id):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("UPDATE teamRatings SET elo=?, attack =?, defence =? WHERE team_id =? AND fixture_id = ?", (elo, attack, defence, team_id, fixture_id))
    con.commit()
    con.close()
    return


