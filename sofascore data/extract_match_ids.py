#WE ARE GETTING ALL OF THE MATCH IDs using Selenium (extension that acts like a browser, we use it to omit Sofascore's anti-bot defense)


import json
from selenium import webdriver

tournament_id = 16 #sofascore tournament id for the world cup

season_id = 58210 #sofascore season id for the 2026 world cup

base_url = 'https://www.sofascore.com/api/v1' #base url for interacting with api

options = webdriver.ChromeOptions()

options.set_capability(
    'goog:loggingPrefs', {"performance" : "ALL", "browser" : "ALL"}
) #grant permissions to the driver so that it can do the same as we can when we use chrome

driver = webdriver.Chrome(options=options) #initiate google chrome instance

page = 0 #Start from the most recent events and collect data from all pages (so we start from the last matches and move backward)
with open("match_ids.txt", 'w') as f:
    while True:
        try:
            driver.get(f"{base_url}/unique-tournament/{tournament_id}/season/{season_id}/events/last/{page}") #go to the url containing all of the match data
        except:
            pass

        json_text = driver.find_element("tag name", "pre").text #pre is the tag in the html of the link in which all of the json data is
        data = json.loads(json_text) #get the json

        for event in data['events']:
            f.write(str(event['id']) + '\n') #extract only the match_ids

        if not data['hasNextPage']: #when we reach the beginning, end the loo[]
            break

        page+=1


