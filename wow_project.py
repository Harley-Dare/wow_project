# goofin with wow api

import configparser
import requests
import sys
import json
from Character import Character
from requests.exceptions import RequestException 
import sqlite3
import math



# Returns the config file 
def read_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

# Returns an OAuth token
def get_token():
    # Do not show client details, keep in config file separate
    config_file = "/home/harley/Documents/programming/wow_project/config.ini"
    config = read_config(config_file)
    CLIENT_ID = config.get("API", "client_id")
    CLIENT_SECRET = config.get("API", "client_secret")
    
    # Obtain an OAuth token using client id and secret
    oauth = requests.post(f"https://us.battle.net/oauth/token", data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    if oauth.status_code != 200:
        raise Exception(f"The token request failed due to: {oauth.text}")
    else:
        access_token = oauth.json()['access_token']
    return access_token

# populate a list of characters
def read_in_characters():
    config_file = "/home/harley/Documents/programming/wow_project/config.ini"
    config = read_config(config_file)
    characters_full_string = config.get("Characters", "characters")
    character_list_split = characters_full_string.split("; ")
    characters = []
    
    for character in character_list_split:
        name, server, region = character.split(", ")
        temp_char = Character(name, server, region)
        characters.append(temp_char)
    
    return characters

# get character gear
def get_gear(name, server, region):
    API_KEY = get_token()
    API_URL = f"https://{region}.api.blizzard.com/profile/wow/character/{server}/{name}/equipment"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Battlenet-Namespace": f"profile-{region}",
    }
    
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1) 
    else:
        equipment_data = response.json()
        return equipment_data
    
# get character profile
def get_character_profile(name, server, region):
    API_KEY = get_token()
    API_URL = f"https://{region}.api.blizzard.com/profile/wow/character/{server}/{name}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Battlenet-Namespace": f"profile-{region}",
    }
    
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch profile data. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1) 
    else:
        character_profile_data = response.json()
        return character_profile_data  
    
# get character keystone info
def get_character_keystone_data(name, server, region):
    API_KEY = get_token()
    API_URL = f"https://{region}.api.blizzard.com/profile/wow/character/{server}/{name}/mythic-keystone-profile/season/11"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Battlenet-Namespace": f"profile-{region}",
    }
    
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch keystone data. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1) 
    else:
        keystone_data = response.json()
        return keystone_data      

# write data to json
def write_to_json(data, filename):
    with open(f"{filename}", "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Saved data to {filename}")
    
# database populating
def populate_db(name, character_class, item_level, rating, server, region):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS data (
            name TEXT,
            class TEXT,
            item_level INTEGER,
            rating INTEGER,
            server TEXT,
            region TEXT
        )
    ''')
    
    cursor.execute(f'''
                   INSERT INTO data (name, class, item_level, rating, server, region)
                   VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, character_class, item_level, rating, server, region))
    conn.commit()

# clear table
def clear_table():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM data")
    row_count = cursor.fetchone()[0]
    # If the table has contents (row_count > 0), delete the rows
    if row_count > 0:
        cursor.execute(f"DELETE FROM data")
        conn.commit()
        print(f"Cleared {row_count} rows from data.")
    else:
        print(f"No rows to clear in data.")

# sort table by item level
def sort_table_by_ilvl():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    sort = "SELECT * FROM data ORDER BY item_level DESC"
    cursor.execute(sort)
    


#####################
characters = read_in_characters()
database_name = "data"
try:
 clear_table()
except:
    print("ow")
try:
    for character in characters:
        temp_name = character.name
        temp_server = character.server
        temp_region = character.region
        
        print(temp_name)
        
        character_profile_data = get_character_profile(temp_name, temp_server, temp_region)
        character_keystone_data = get_character_keystone_data(temp_name, temp_server, temp_region)
        
        character.mythic_rating = math.floor(character_keystone_data["mythic_rating"]["rating"])
        character.item_level = character_profile_data["average_item_level"]
        character.character_class = character_profile_data["character_class"]["name"]["en_US"]
        
        populate_db(temp_name, character.character_class, character.item_level, character.mythic_rating, temp_server, temp_region)

except RequestException as e:
    print(f"Error with {temp_name}")
    
sort_table_by_ilvl()
