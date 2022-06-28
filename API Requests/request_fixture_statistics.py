import json
import http.client
import time
import sqlite3

def request_fixture_statistics_home(season, league_id, store_json_path, con):
    cur = con.cursor()
    fixture_and_home_id = cur.execute("SELECT fixture_id, home_id FROM fixtures AS f WHERE f.season =? AND f.league_id=?", (season, league_id)).fetchall()
    results = []
    start = time.time()
    anfragen = 0
    #print(len(player_IDs))
    for i in range(0, len(fixture_and_home_id)):
            

            fixture_id = fixture_and_home_id[i][0]
            home_id = fixture_and_home_id[i][1]
            if(i%400 == 0 and i !=0):
                x = 70 # Put in whatever seconds you want it to wait
                print("Fixture stats home: Wait for reqeust per minute")
                #print("i =", i)
                time.sleep(x)

            
            str_request = "/fixtures/statistics?fixture="+ str(fixture_id) + "&team=" + str(home_id)
            conn = http.client.HTTPSConnection("v3.football.api-sports.io")

            headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': "XXXX-XXXX"
            }
            
            conn.request("GET", str_request, headers=headers)
            res = conn.getresponse()
            data = res.read()
            results.append(json.loads(data))
            anfragen = anfragen + 1 
            
    
    elapsed_time_fl = (time.time() - start) 
    print(str(elapsed_time_fl)+ " time")
    print(str(anfragen)+ " anfragen")
    with open(store_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f)    
        

def request_fixture_statistics_away(season,league_id , store_json_path, con):
    cur = con.cursor()
    fixture_and_away_id = cur.execute("SELECT fixture_id, away_id FROM fixtures AS f WHERE f.season =? AND f.league_id=?", (season, league_id)).fetchall()
    results = []
    start = time.time()
    anfragen = 0
    #print(len(player_IDs))
    for i in range(0, len(fixture_and_away_id)):
            

            fixture_id = fixture_and_away_id[i][0]
            away_id = fixture_and_away_id[i][1]

            if(i%400 == 0 and i !=0):
                x = 70 # Put in whatever seconds you want it to wait
                print("Fixture stats away: Wait for reqeust per minute")
                
                time.sleep(x)

            
            str_request = "/fixtures/statistics?fixture="+ str(fixture_id) + "&team=" + str(away_id)
            conn = http.client.HTTPSConnection("v3.football.api-sports.io")

            headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': "XXXX-XXXX"
            }
            
            conn.request("GET", str_request, headers=headers)

            res = conn.getresponse()
            data = res.read()
            results.append(json.loads(data))
            anfragen = anfragen + 1 
            
    
    elapsed_time_fl = (time.time() - start) 
    print(str(elapsed_time_fl)+ " time")
    print(str(anfragen)+ " anfragen")
    with open(store_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f)    
        

#store_fixture_statistics_away()