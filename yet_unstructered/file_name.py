import http.client
import json


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


def store_fixture_data(league_id , season ,raw_string_path):
    conn = http.client.HTTPSConnection("XXXX-XXXX")

    headers = {
        'x-rapidapi-host': "XXXX-XXXX",
        'x-rapidapi-key': "XXXX-XXXX"
        }

    conn.request("GET", "/fixtures?league="+ str(league_id) + "&season=" + str(season), headers=headers)

    res = conn.getresponse()
    data = res.read()


    with open(raw_string_path, 'w', encoding='utf-8') as f:
        json.dump(json.loads(data), f)

def fixture_file_name_generator(path,additional_word ,league_name, season):
    file_name = '\\' +str(league_name) + "_" + str(season) + str(additional_word) +".json"
    full_path = path + file_name
    return full_path


