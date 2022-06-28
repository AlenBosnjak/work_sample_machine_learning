from json_extract import json_extract
import sqlite3
import json
import pandas as pd

# some_file.py

#cur.execute("CREATE TABLE playerStatistic (fixture_id INTEGER, team_id INTEGER,timestamp INTEGER, name TEXT, player_id INTEGER, minutes INTEGER, number INTEGER, position TEXT, rating INTEGER, offside INTEGER, total_shots INTEGER, on_goal_shots INTEGER, total_goals INTEGER, conceded INTEGER, assists INTEGER, saves INTEGER, total_passes INTEGER, key_passes INTEGER, pass_accuracy INTEGER, total_tackels INTEGER, blocks INTEGER, interceptions INTEGER, total_duels INTEGER, won_duels INTEGER, dribble_attempts INTEGER, dribble_success INTEGER, dribble_past INTEGER, drawn_fouls INTEGER, commited_fouls INTEGER, yellow INTEGER, red INTEGER, won_penalty INTEGER, commited_penalty INTEGER, scored_penalty INTEGER, missed_penalty INTEGER, saved_penalty INTEGER)")

def get_fixture_timestamp(fixture_id):
    path = r"XXXX-XXXX"
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT timestamp FROM fixtures AS ps WHERE ps.fixture_id = (?)", con, params=(fixture_id,))
    timestamp_int = int(df.loc[0]['timestamp'])
    con.close()
    return timestamp_int

#fixture_id INTEGER, team_id INTEGER,timestamp INTEGER ,name TEXT, player_id INTEGER, minutes INTEGER, number INTEGER, position TEXT, rating INTEGER, offside INTEGER, total_shots INTEGER, on_goal_shots INTEGER, total_goals INTEGER, conceded INTEGER, assists INTEGER, saves INTEGER, total_passes INTEGER, key_passes INTEGER, pass_accuracy INTEGER, total_tackels INTEGER, blocks INTEGER, interceptions INTEGER, total_duels INTEGER, won_duels INTEGER, dribble_attempts INTEGER, dribble_success INTEGER, dribble_past INTEGER, drawn_fouls INTEGER, commited_fouls INTEGER, yellow INTEGER, red INTEGER, won_penalty INTEGER, commited_penalty INTEGER, scored_penalty INTEGER, missed_penalty INTEGER, saved_penalty INTEGER

def type_help(variable, name):
    if(isinstance(variable, str)):
        print(name, "TEXT")
        print(variable)
    elif(isinstance(variable, bool)):
        print(name, "BOOL")
        print(variable)
    elif(isinstance(variable, int)):
        print(name, "INTEGER")
        print(variable)
    else:
        print(name,"HELP!")
        print(variable)
    print(type(variable))

#teamId muss noch rein

def player_statistics_to_db(raw_path_player_stats, con):
    cur = con.cursor()
    with open(raw_path_player_stats, encoding='utf-8') as f:
        player_statistics = json.load(f)
        fixture = json_extract(player_statistics, "fixture")
        response = json_extract(player_statistics, "response")

        for i in range(0, len(response)):
            player = json_extract(response[i], "players")
            team = json_extract(response[i], "team")
            #müssen getrennt  werden, da nicht immer gleich viele Spieler von away und home
            #print(fixture[i])
            if(len(player)>0):
                home_players = player[0]
                home_team_id = json_extract(team[0], "id")
                away_players = player[1]
                away_team_id = json_extract(team[1], "id")
                timestamp = get_fixture_timestamp(int(fixture[i]))
            
            
            
                for j in range (0, len(home_players)):
                    name, player_id = get_player(home_players[j])
                    minutes, number, position, rating, h_captain, h_substitute = get_games(home_players[j])
                    offside = get_offsides(home_players[j])
                    total_shots, on_goal_shots = get_shots(home_players[j])
                    total_goals, conceded, assists, saves = get_Goals(home_players[j])
                    total_passes, key_passes, pass_accuracy = get_passes(home_players[j])
                    total_tackels, blocks, interceptions = get_tackles(home_players[j])
                    total_duels, won_duels = get_duels(home_players[j])
                    dribble_attempts, dribble_success, dribble_past = get_dribbles(home_players[j])
                    drawn_fouls, commited_fouls = get_fouls(home_players[j])
                    yellow, red = get_cards(home_players[j])
                    won_penalty, commited_penalty, scored_penalty, missed_penalty, saved_penalty = get_penalty(home_players[j])
                    

                    cur.execute("INSERT INTO playerStatistic VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (int(fixture[i]), home_team_id[0],timestamp ,name , player_id , minutes , number , position , rating , offside , total_shots , on_goal_shots , total_goals , conceded , assists , saves , total_passes , key_passes , pass_accuracy , total_tackels , blocks , interceptions , total_duels , won_duels , dribble_attempts , dribble_success , dribble_past , drawn_fouls , commited_fouls , yellow , red , won_penalty , commited_penalty , scored_penalty , missed_penalty , saved_penalty))
                
                for j in range (0, len(away_players)):
                    name, player_id = get_player(away_players[j])
                    minutes, number, position, rating, captain, substitute = get_games(away_players[j])
                    offside = get_offsides(away_players[j])
                    total_shots, on_goal_shots = get_shots(away_players[j])
                    total_goals, conceded, assists, saves = get_Goals(away_players[j])
                    total_passes, key_passes, pass_accuracy = get_passes(away_players[j])
                    total_tackels, blocks, interceptions = get_tackles(away_players[j])
                    total_duels, won_duels = get_duels(away_players[j])
                    dribble_attempts, dribble_success, dribble_past = get_dribbles(away_players[j])
                    drawn_fouls, commited_fouls = get_fouls(away_players[j])
                    yellow, red = get_cards(away_players[j])
                    won_penalty, commited_penalty, scored_penalty, missed_penalty, saved_penalty = get_penalty(away_players[j])
                    
                    cur.execute("INSERT INTO playerStatistic VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (int(fixture[i]), away_team_id[0],timestamp ,name , player_id , minutes , number , position , rating , offside , total_shots , on_goal_shots , total_goals , conceded , assists , saves , total_passes , key_passes , pass_accuracy , total_tackels , blocks , interceptions , total_duels , won_duels , dribble_attempts , dribble_success , dribble_past , drawn_fouls , commited_fouls , yellow , red , won_penalty , commited_penalty , scored_penalty , missed_penalty , saved_penalty))

    con.commit()
    
    

    
def get_player(player):
    name = json_extract(player, "name")
    id = json_extract(player, "id")
    return name[0], id[0]


def get_games(player):
    minutes = json_extract(player, "minutes")
    number = json_extract(player, "number")
    position = json_extract(player, "position")
    rating = json_extract(player, "rating")
    captain = json_extract(player, "captain")
    substitute =  json_extract(player, "substitute")
    variables =  [minutes[0], number[0], position[0], rating[0], captain[0], substitute[0]]
    minutes[0], number[0], position[0], rating[0], captain[0], substitute[0] = erase_none(variables)
    return minutes[0], number[0], position[0], rating[0], captain[0], substitute[0]

def get_offsides(player):
    offside = json_extract(player, "offside")
    variables =  [offside]
    offside = erase_none(variables)
    return offside[0]

def get_shots(player):
    shots = json_extract(player, "shots")
    total_shots = json_extract(shots, "total")
    on_goal_shots = json_extract(shots, "on")
    variables =  [total_shots[0], on_goal_shots[0]]
    total_shots[0], on_goal_shots[0] = erase_none(variables)
    return total_shots[0], on_goal_shots[0]

def get_Goals(player):
    goals = json_extract(player, "goals")
    total_goals = json_extract(goals, "total")
    conceded = json_extract(goals, "conceded")
    assists = json_extract(goals, "assists")
    saves = json_extract(goals, "saves")
    variables =  [total_goals[0], conceded[0], assists[0], saves[0]]
    total_goals[0], conceded[0], assists[0], saves[0] = erase_none(variables)
    return total_goals[0], conceded[0], assists[0], saves[0]

def get_passes(player):
    passes = json_extract(player, "passes")
    total_passes = json_extract(passes, "total")
    key_passes = json_extract(passes, "key")
    pass_accuracy = json_extract(passes, "accuracy")
    if(isinstance(pass_accuracy[0], str)):
                string = pass_accuracy[0]
                string = string.replace('%', '')
                if(string != None):
                    pass_accuracy = int(string) #pass_accuracy
    else:
        pass_accuracy = pass_accuracy[0]
    variables =  [total_passes[0], key_passes[0], pass_accuracy]
    total_passes[0], key_passes[0], pass_accuracy = erase_none(variables)
    return total_passes[0], key_passes[0], pass_accuracy

def get_tackles(player):
    tackles = json_extract(player, "tackles")
    total_tackels = json_extract(tackles, "total")
    blocks = json_extract(tackles, "blocks")
    interceptions = json_extract(tackles, "interceptions")
    variables =  [total_tackels[0], blocks[0], interceptions[0]]
    total_tackels[0], blocks[0], interceptions[0] = erase_none(variables)
    return total_tackels[0], blocks[0], interceptions[0]

def get_duels(player):
    duels = json_extract(player, "duels")
    total_duels = json_extract(duels, "total")
    won = json_extract(duels,"won")
    variables =  [total_duels[0], won[0]]
    total_duels[0], won[0] = erase_none(variables)
    return total_duels[0], won[0]

def get_dribbles(player):
    dribbles = json_extract(player, "dribbles")
    dribble_attempts = json_extract(dribbles, "attempts")
    dribble_success = json_extract(dribbles, "success")
    dribble_past = json_extract(dribbles, "past")#wie oft ausgedribbelt
    variables =  [dribble_attempts[0], dribble_success[0], dribble_past[0]]
    dribble_attempts[0], dribble_success[0], dribble_past[0] = erase_none(variables)
    return dribble_attempts[0], dribble_success[0], dribble_past[0]

def get_fouls(player):
    fouls = json_extract(player, "fouls")
    drawn = json_extract(fouls, "drawn")
    commited = json_extract(fouls, "commited")
    variables =  [drawn[0], commited]
    drawn[0], commited = erase_none(variables)
    return drawn[0], commited

def get_cards(player):
    yellow = json_extract(player, "yellow")
    red = json_extract(player, "red")
    variables =  [yellow[0], red[0]]
    yellow[0], red[0] = erase_none(variables)
    return yellow[0], red[0]

def get_penalty(player):
    penalty = json_extract(player, "penalty")
    won = json_extract(penalty, "won")
    commited = json_extract(penalty, "commited")
    scored = json_extract(penalty, "scored")
    missed = json_extract(penalty, "missed")
    saved = json_extract(penalty, "saved")
    variables =  [won[0], commited[0], scored[0], missed[0], saved[0]]
    won[0], commited[0], scored[0], missed[0], saved[0] = erase_none(variables)
    return won[0], commited[0], scored[0], missed[0], saved[0]


def erase_none(variables):
    for i in range (0, len(variables)):
        if(variables[i]== None):
            variables[i] = 0
        elif(isinstance(variables[i], list)):
            if(len(variables[i]) == 0):
                variables[i] = 0
        
    return tuple(variables)

