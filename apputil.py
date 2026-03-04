import os
import pandas as pd
import requests


class Genius:
    """Simple wrapper class for interacting with the Genius REST API."""

    def __init__(self, access_token):
        """Initialize the Genius API wrapper.

        Args:
            access_token (str): Valid Genius API access token.
        """
        # Store the API access token for authenticated requests
        self.access_token = access_token
        
        # Base endpoint for all Genius API requests
        self.__base_url = 'http://api.genius.com'

    def get_artist_id(self, search_term):
        """Retrieve an artist's Genius ID using a search query.

        Args:
            search_term (str): Artist name (or keyword) to search for.

        Returns:
            int | None: The Genius artist ID if found, otherwise None.
        """
        try:
            # Construct search endpoint with query parameter
            search_url = f"{self.__base_url}/search?q={search_term}"
            
            # Send GET request with authorization header
            response = requests.get(
                search_url,
                headers={"Authorization": "Bearer " + self.access_token}
            )

            # Parse JSON response
            json_data = response.json()

            # If no matching results are returned, exit early
            if len(json_data['response']['hits']) == 0:
                return None

            # Extract the first search result
            first_result = json_data['response']['hits'][0]

            # Return the primary artist ID from the first result
            return first_result['result']['primary_artist']['id']

        # Catch and report any unexpected errors
        except Exception as e:
            print(f'Error retrieving artist ID for "{search_term}": {e}')
            return None


    def get_artist(self, search_term):
        """Retrieve full artist details from Genius using a search term.

        Args:
            search_term (str): Artist name (or keyword) to search for.

        Returns:
            dict | None: Artist metadata dictionary if found, otherwise None.
        """

        # First retrieve the artist's Genius ID
        artist_id = self.get_artist_id(search_term)
        
        # If no artist was found, stop here
        if artist_id is None:
            return None

        try:
            # Construct endpoint to retrieve artist details
            artist_url = f"{self.__base_url}/artists/{artist_id}"
            
            # Send authorized GET request
            response = requests.get(
                artist_url,
                headers={"Authorization": "Bearer " + self.access_token}
            )

            # Return the artist information section of the response
            return response.json()['response']['artist']
        
        # Catch and report any unexpected errors
        except Exception as e:
            print(f'Error retrieving artist data for "{search_term}" (id:{artist_id}): {e}')
            return None

    def get_artists(self, search_terms):
        """Retrieve summary information for multiple artists.

        Args:
            search_terms (list[str]): List of artist names (or keywords).

        Returns:
            pandas.DataFrame: DataFrame containing:
                - search_term
                - artist_name
                - artist_id
                - followers_count
        """

        # Initialize empty DataFrame with predefined columns
        df = pd.DataFrame(columns=[
            'search_term',
            'artist_name',
            'artist_id',
            'followers_count'
        ])

        # Loop through each provided search term
        for term in search_terms:
            # Retrieve detailed artist data
            artist_data = self.get_artist(term)

            # If no artist was found, insert placeholder values
            if artist_data is None:
                row = {
                    'search_term': term,
                    'artist_name': 'no result',
                    'artist_id': 'no result',
                    'followers_count': 'no result'
                }

            else:
                # Extract relevant fields from the API response
                row = {
                    'search_term': term,
                    'artist_name': artist_data['name'],
                    'artist_id': artist_data['id'],
                    'followers_count': artist_data['followers_count']
                }

            # Append the row to the DataFrame
            df = pd.concat([df, pd.DataFrame([row])])

        # Return compiled results
        return df
