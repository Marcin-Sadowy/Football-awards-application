import json
from selenium import webdriver
from pathlib import Path

#Directories for file opening and saving

base_dir = Path(__file__).resolve().parent
match_ids_file = base_dir / 'match_ids.txt'
lineups_directory = base_dir / 'lineups'


#Create dictionary for lineups. It will be in the form {match id : [list of players]}
lineups = {}
#Create a dictionary for stats in the form (match id: all players' stats)
stats = {}
#Create a dictionary for player_ids in the form (player id : name)
player_ids = {}
#Read the match ids we extracted in the extract_match_ids file
match_ids = []

with open(match_ids_file, 'r') as f:
    for match_id in f:
        match_ids.append(match_id.strip())

base_url = 'https://www.sofascore.com/api/v1/event'

#Set up the google chrome instance

options = webdriver.ChromeOptions()


driver = webdriver.Chrome(options=options)

for id in match_ids:
    
        try:
            driver.get(f'{base_url}/{id}/lineups')
            
            json_text = driver.find_element('tag name', 'pre').text

            data = json.loads(json_text)

            lineup = []
            match_stats = []

            for team in ['home', 'away']:
                for player in data[team]['players']:

                
                    player_id = player['player']['id']
                    player_name = player['player']['name']
                
                    lineup.append(player_id)
                    player_ids[player_id] = player_name
                    match_stats.append(player_id)
                
                    player_stats = player['statistics']
                    match_stats.append(player_stats)

            lineups[id] = lineup
            stats[id] = match_stats

        except Exception as e:
            print(f"Failed for match id: {id} : {e}")

        
#Write name-id pairs for all player
with open('player_ids.txt', 'w', encoding='utf-8') as f:
    for id, name in player_ids.items():
        f.write(f'{id} : {name}\n')

#Create a file from each match containing player stats from that match
for match_id, match_stats in stats.items():

    file_path = lineups_directory / f'{match_id}.txt'

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(match_stats, file, indent=2)