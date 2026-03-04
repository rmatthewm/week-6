import os
import pandas as pd
import requests


class Genius:
    """Simple wrapper class for interacting with the Genius REST API."""

    def __init__(self, access_token):
        """Initialize the Genius API wrapper."""
        self.access_token = access_token
        self.__base_url = 'http://api.genius.com'

    def get_artist_id(self, search_term):
        """Retrieve an artist's Genius ID using a search query."""
        try:
            search_url = f"{self.__base_url}/search"

            response = requests.get(
                search_url,
                params={"q": search_term},
                headers={"Authorization": "Bearer " + self.access_token}
            )

            json_data = response.json()

            # Safely check structure
            hits = json_data.get("response", {}).get("hits", [])
            if not hits:
                return None

            return hits[0]["result"]["primary_artist"]["id"]

        except Exception:
            return None

    def get_artist(self, search_term):
        """Retrieve full artist details from Genius using a search term."""

        artist_id = self.get_artist_id(search_term)

        if artist_id is None:
            return None

        try:
            artist_url = f"{self.__base_url}/artists/{artist_id}"

            response = requests.get(
                artist_url,
                headers={"Authorization": "Bearer " + self.access_token}
            )

            json_data = response.json()

            # Safely access nested keys
            return json_data.get("response", {}).get("artist")

        except Exception:
            return None

    def get_artists(self, search_terms):
        """Retrieve summary information for multiple artists."""

        df = pd.DataFrame(columns=[
            'search_term',
            'artist_name',
            'artist_id',
            'followers_count'
        ])

        for term in search_terms:
            artist_data = self.get_artist(term)

            if artist_data is None:
                row = {
                    'search_term': term,
                    'artist_name': 'no result',
                    'artist_id': 'no result',
                    'followers_count': 'no result'
                }
            else:
                row = {
                    'search_term': term,
                    'artist_name': artist_data.get('name'),
                    'artist_id': artist_data.get('id'),
                    'followers_count': artist_data.get('followers_count')
                }

            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

        return df
