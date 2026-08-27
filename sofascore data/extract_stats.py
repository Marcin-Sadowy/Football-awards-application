import json
from selenium import webdriver
from pathlib import Path

#Directories for file opening and saving

base_dir = Path(__file__).resolve().parent
match_ids_file = base_dir / 'match_ids.txt'
lineups_directory = base_dir / 'lineups'


#Create dictionary for lineups. It will be in the form {match id : [list of players]}
lineups = {}
player_ids = {}
#Read the match ids we extracted in the extract_match_ids file
match_ids = []

with open(match_ids_file, 'r') as f:
    for match_id in f:
        match_ids.append(match_id.strip())

base_url = 'https://www.sofascore.com/api/v1/event'

#Set up the google chrome instance

options = webdriver.ChromeOptions()

options.set_capability(
    'goog:loggingPrefs', {'performance' : 'ALL', 'browser' : 'ALL'}
)

driver = webdriver.Chrome(options=options)

for id in match_ids:
    
        try:
            driver.get(f'{base_url}/{id}/lineups')
            json_text = driver.find_element('tag name', 'pre').text
            data = json.loads(json_text)
            
            lineup = []
            file_path = lineups_directory / f'{id}.txt'
            
            with open(file_path, 'w') as file:
                for player in data['home']['players']:
            
                    player_id = player['player']['id']
                    player_name = player['player']['name']
            
                    lineup.append(player_id)
                    player_ids[player_id] = player_name
            
                    file.write(json.dumps(player['player']['statistics'], indent=2))
                    file.write('\n')
            
                    lineups[id] = lineup

        except:
            print(f"Failed for match id: {id}")

        

with open('player_ids.txt', 'w', encoding='utf-8') as f:
    for id, name in player_ids.items():
        f.write(f'{id} : {name}\n')