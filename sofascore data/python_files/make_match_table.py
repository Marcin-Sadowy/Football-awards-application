#For each match_id we will extract the home team and away team 

import json
from selenium import webdriver
from pathlib import Path

#Directories
current_dir = Path(__file__).resolve().parent.parent
match_ids_path = current_dir / 'match_ids.txt'
match_table_path = current_dir / 'match and player tables'

#Extract match_ids

match_ids = []
  
with open(match_ids_path, 'r') as f:
        for match_id in f:
            match_ids.append(match_id.strip())



#Set up the url

base_url = 'https://www.sofascore.com/api/v1'

tournament_id = 16

season_id = 5280

#Set up the browser instance

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options)

#Make the table file
with open(match_table_path/'match_table.txt', 'w', encoding='utf-8') as match_table:

    match_table.write('Match_id Team1 Team2\n')

    #Extract both teams for each match_id

    for id in match_ids:

        try: 

            driver.get(f'{base_url}/event/{id}')
        
            json_text = driver.find_element('tag name', 'pre').text
            
            data = json.loads(json_text)

            team_1 = data['event']['homeTeam']['name']
            team_2 = data['event']['awayTeam']['name']



            match_table.write(f'{id} {team_1} {team_2}\n')
        
        except Exception as e:
            print(f"Extracting failed for id: {id}, {e}")






