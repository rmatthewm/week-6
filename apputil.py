import os
from dotenv import load_dotenv
import requests

load_dotenv()
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


# Exercise 1
class Genius:
    def __init__(self, access_token):
        # store the token so other methods can use it
        self.access_token = access_token

    # Exercise 2
    def get_artist(self, search_term):
        """Return the artist information dictionary for *search_term*.

        The Genius search endpoint returns a list of song hits; the primary
        artist for the first hit is used to pick an artist ID.  That ID is
        then supplied to the ``/artists/{id}`` endpoint (see the Genius
        documentation under **Artists**).  The method returns the artist
        dictionary obtained from the JSON response.

        If there are no hits the method returns ``None``.
        """
        base = "http://api.genius.com"

        # first do a search to locate a possible artist
        search_url = f"{base}/search"
        params = {"q": search_term, "access_token": self.access_token}
        resp = requests.get(search_url, params=params)
        resp.raise_for_status()
        data = resp.json()

        hits = data.get("response", {}).get("hits", [])
        if not hits:
            # nothing found
            return None

        # grab the primary artist id from the first hit
        artist_id = hits[0]["result"]["primary_artist"]["id"]

        # now hit the artists endpoint
        artist_url = f"{base}/artists/{artist_id}"
        resp2 = requests.get(artist_url, params={"access_token": self.access_token})
        resp2.raise_for_status()
        artist_data = resp2.json()

        # return the dictionary containing the artist information
        return artist_data.get("response", {}).get("artist")

