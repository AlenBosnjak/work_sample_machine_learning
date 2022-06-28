import time
from yet_unstructered.read_db import get_fixture_goals_result, get_fixture_home_away_id_timestamp, get_team_rating, len_fixtures, update_team_rating


def update_elo(self_elo,  other_team_elo, result, goal_diff, is_home):
        k_weight = 20
        
        expected_result = get_expected_result(self_elo, other_team_elo)
        #G = torgewichtung
        G = calc_G(goal_diff)
        result_for_team = calc_result_for_team(result, is_home)

        # update elo
        self_elo = self_elo + k_weight * G * (result_for_team - expected_result)
        return self_elo

def calc_G(goal_diff):
    if(goal_diff <= 1):
        G = 1
    elif(goal_diff == 2):
        G = 1.5
    else:
        G = (11+goal_diff)/8

    return G

def calc_result_for_team(result, is_home):
    #Diese umrechnung ist abhängig, von dem mapping in fixture_to_db und wird benötigt 
    if(result == 0.5):
        return 0.5 #unentschieden für heim und auswärts gleich
    if(is_home):
        if(result == 0): #0 bedeutet heimsieg, wenn heimmannschaft gib für die elo rechnung eine 1 zurück
            return 1
        else:
            return 0 #wenn kein unetschieden oder sieg bleibt nur niederlage
    else:
        return result 

def get_expected_result(self_elo, other_team_elo):
    
    #elo difference
    elo_diff = self_elo - other_team_elo
    
    #We = expected result
    expected_result = 1/(10**(-elo_diff/400)+1)
    return expected_result

def update_attack(self_att, goals_shot, other_team_def):
    alpha = 0.1
    ratio = 0.75
    self_att = self_att + ((goals_shot - self_att)*ratio + (goals_shot + other_team_def)*(1-ratio)) *alpha
    return self_att
    
    #nach jeder fixture für jedes Team aufzurufen
def update_defence(self_def, goals_got, other_team_att): 
    alpha=0.1 
    ratio=0.75
    self_def = self_def - ((goals_got+self_def)*ratio + (goals_got - other_team_att)*(1-ratio))*alpha
    return self_def



def calc_goal_difference(home_goals, away_goals):
    if None not in (home_goals, away_goals):
        return abs(home_goals - away_goals)
    else: 
        return None

