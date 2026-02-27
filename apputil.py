import os
import pandas as pd
import requests


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
        try:
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

        # Handle any exceptions
        except Exception as e:
            print(f'An error occurred while retrieving artist id for "{search_term}": {e}')
            return None


    def get_artist(self, search_term):
        """ Returns the artist information from Genius given a search term.

        Args:
            search_term (str): the search term to look for the artist

        Returns:
            dict: the 'JSON' data in Python format with the artist info, empty if no result
        """

        # Get the artist id
        artist_id = self.get_artist_id(search_term)
        
        # If there are no results, return None 
        if artist_id is None:
            return None

        # Make another query to get the artist info
        try:
            artist_url = f"{self.__base_url}/artists/{artist_id}"
            response = requests.get(artist_url, 
                headers={"Authorization": "Bearer " + self.__access_token})

            # Return the json data
            return response.json()['response']['artist']
        
        # Handle any exceptions
        except Exception as e:
            print(f'An error occurred while retrieving artist data for "{search_term}" (id:{artist_id}): {e}')
            return None

    def get_artists(self, search_terms):
        """ Returns some basic information for each artist searched for.

        Args:
            search_terms (list(str)): a list of search terms 

        Returns:
            pandas.DataFrame: the search term, artist name, artist id, and 
            follower count for each artist 
        """

        # Create a dataframe to return
        df = pd.DataFrame(columns=['search_term', 'artist_name', 'artist_id', 'followers_count'])

        # Search for the artist data for each search term
        for term in search_terms:
            # Get the data for each artist
            artist_data = self.get_artist(term)

            # If there are no results, we will create a no result entry
            if artist_data is None:
                row = {
                    'search_term': term,
                    'artist_name': 'no result',
                    'artist_id': 'no result',
                    'followers_count': 'no result'
                }

            else:
                # Create the row we want to add to the dataframe using the 
                # data from the artist
                row = {
                    'search_term': term,
                    'artist_name': artist_data['name'],
                    'artist_id': artist_data['id'],
                    'followers_count': artist_data['followers_count']
                }

            # Add the row to the dataframe
            df = pd.concat([df, pd.DataFrame([row])])

        # Return the dataframe
        return df
