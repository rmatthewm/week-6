import os
from dotenv import load_dotenv
import requests

load_dotenv()
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


class Genius:
    """ A wrapper for the Genius API. """

    def __init__(self, access_token):
        """ Constructor, takes access token to be able to access the Genius API.

        Args:
            access_token (str): the access token 
        """
        # The access toke to use
        self.__access_token = access_token
        
        # Base url of the Genius API
        self.__base_url = 'http://api.genius.com'

    def get_artist_id(self, search_term):
        """ Returns the artist id from Genius given a search term.

        Args:
            search_term (str): the search term to look for the artist

        Returns:
            int: the artist id, or None if no artist is found
        """
        # Make a search query to find the songs with the desired artist 
        search_url = f"{self.__base_url}/search?q={search_term}"
        response = requests.get(search_url, 
            headers={"Authorization": "Bearer " + self.__access_token})

        json_data = response.json()

        # If there are no results, return None
        if len(json_data['response']['hits']) == 0:
            return None

        # Otherwise, get the first result
        first_result = json_data['response']['hits'][0]

        # Return the artist id
        return first_result['result']['primary_artist']['id']


    def get_artist(self, search_term):
        """ Returns the artist information from Genius given a search term.

        Args:
            search_term (str): the search term to look for the artist

        Returns:
            dict: the 'JSON' data in Python format with the artist info, empty if no result
        """

        # Get the artist id
        artist_id = self.get_artist_id(search_term)
        
        # If there are no results, return an empty dictionary
        if artist_id is None:
            return {}

        # Make another query to get the artist info
        artist_url = f"{self.__base_url}/artists/{artist_id}"
        response = requests.get(artist_url, 
            headers={"Authorization": "Bearer " + self.__access_token})

        # Return the json data
        return response.json()['response']['artist']

    def get_artists(self, search_term):
        pass
       
# testing
g = Genius(ACCESS_TOKEN)
print(g.get_artist('Radiohead'))