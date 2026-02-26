import os
from dotenv import load_dotenv
import requests

load_dotenv()
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


# Exercise 1
class Genius:
    def __init__(self, access_token):
        # Store the token so other methods can use it
        self.access_token = access_token
        
        # Base url of the Genius API
        self.base_url = 'http://api.genius.com'

    # Exercise 2
    def get_artist(self, search_term):
        # Make a search query
        genius_search_url = f"{self.base_url}/search?q={search_term}"

        response = requests.get(genius_search_url, 
            headers={"Authorization": "Bearer " + self.access_token})

        json_data = response.json()

        # Get the first result if there is one
        if len(json_data['response']['hits']) == 0:
            return None

        first_result = json_data['response']['hits'][0]

        # Get the artist id
        artist_id = first_result['result']['primary_artist']['id']

        # Make another query for the artist info
        genius_artist_url = f"{self.base_url}/artists/{artist_id}"
        response = requests.get(genius_artist_url, 
            headers={"Authorization": "Bearer " + self.access_token})

        # Return the json data
        return response.json()['response']['artist']

# testing
g = Genius(ACCESS_TOKEN)
print(g.get_artist('Radiohead'))