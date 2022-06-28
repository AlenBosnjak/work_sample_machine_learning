import json
import http.client
import time
import sqlite3

def request_player_statistics(season, league_id, store_json_path, con):
    cur = con.cursor()
    fixture_id = cur.execute('SELECT fixture_id FROM fixtures AS f WHERE f.season =? AND f.league_id=?', (season, league_id)).fetchall()
    results = []
    start = time.time()
    anfragen = 0
    #print(len(player_IDs))
    for i in range(0, len(fixture_id)):
            
            
            if(i%400 == 0 and i !=0):
                x = 70 # Put in whatever seconds you want it to wait
                print("Player stats: Wait for reqeust per minute")
                print("i =", i)
                time.sleep(x)

            
            str_request = "/fixtures/players?fixture="+ str(fixture_id[i][0])
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
        
