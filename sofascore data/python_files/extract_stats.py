import json
from selenium import webdriver
from pathlib import Path

#Directories for file opening and saving

base_dir = Path(__file__).resolve().parent.parent
match_ids_file = base_dir / 'match_ids.txt'
stats_directory = base_dir / 'raw_stats'
player_ids_directory = base_dir / 'match and player tables'



#Create a dictionary for stats in the form (match id: all players' stats)
stats = {}
#Create a dictionary for player_ids in the form (player id : name)
player_ids = {}
#Read the match ids we extracted in the extract_match_ids file
match_ids = []

player_stats_csv = ''
goalkeeper_stats_csv = ''


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

            match_stats = []

            for team in ['home', 'away']:
                for player in data[team]['players']:

                    player_id = player['player']['id']
                    player_name = player['player']['name']
                    player_ids[player_id] = player_name


                    player_stats = player['statistics']

                    if len(player_stats.keys()) > 3:

                        if 'saves' in player_stats.keys():

                            if goalkeeper_stats_csv == '':

                                goalkeeper_stats_csv += 'match_id player_id '
                                for key in player_stats.keys():
                                    if key != 'ratingVersions' and key != 'statisticsType':
                                        goalkeeper_stats_csv += key + ' '
                                goalkeeper_stats_csv += '\n'

                            goalkeeper_stats_csv += str(id) + ' ' + str(player_id) + ' '
                            for value in player_stats.values():
                                if not isinstance(value, dict):
                                    goalkeeper_stats_csv += str(value) + ' '
                            goalkeeper_stats_csv += '\n'

                        else:

                            if player_stats_csv == '':
                                player_stats_csv += 'match_id player_id '
                                for key in player_stats.keys():
                                    if key != 'ratingVersions' and key != 'statisticsType':
                                        player_stats_csv += key + ' '
                                player_stats_csv += '\n'

                            player_stats_csv += str(id) + ' ' + str(player_id) + ' '
                            for value in player_stats.values():

                                if not isinstance(value, dict):
                                    player_stats_csv += str(value) + ' '
                            player_stats_csv += '\n'
                            




                    match_stats.append(player_id)
                
                    
                    match_stats.append(player_stats)

            stats[id] = match_stats

        except Exception as e:
            print(f"Failed for match id: {id} : {e}")

        
#Write name-id pairs for all player
with open(player_ids_directory/'player_ids.txt', 'w', encoding='utf-8') as f:
    f.write('Player_id Player_name')
    for id, name in player_ids.items():
        f.write(f'{id} {name}\n')

#Create a file from each match containing player stats from that match
for match_id, match_stats in stats.items():

    file_path = stats_directory / f'{match_id}.txt'

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(match_stats, file, indent=2) #we have to change something there in order for the structure of the stats to be better for database use

with open('goalkeeper_stats.txt' , 'w', encoding='utf-8') as file:
    file.write(goalkeeper_stats_csv)

with open('player_stats.txt' , 'w', encoding='utf-8') as file:
    file.write(player_stats_csv)
